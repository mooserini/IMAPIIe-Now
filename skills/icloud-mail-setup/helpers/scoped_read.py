#!/usr/bin/env python3
"""Read one exact iCloud folder using a GigaMail-managed credential.

Credentials remain inside this process. No IMAP mutations or SMTP operations.
This is a constrained reader, not a sandbox against arbitrary local execution.
"""
import argparse
import email
from email import policy
from html.parser import HTMLParser
import imaplib
import json
import os
import re
import ssl
import sys

MAX_BYTES = 262144
MAX_TEXT = 24000


class MailReadError(Exception):
    pass


class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        if tag in ('p', 'div', 'br', 'li'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.hidden:
            self.hidden -= 1

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def extract(raw):
    msg = email.message_from_bytes(raw, policy=policy.default)
    body = msg.get_body(preferencelist=('plain', 'html'))
    text = ''
    if body:
        content = body.get_content()
        text = content if isinstance(content, str) else ''
        if body.get_content_type() == 'text/html':
            parser = TextOnly()
            parser.feed(text)
            text = ''.join(parser.parts)
    return {
        'subject': str(msg.get('Subject', '')),
        'from': str(msg.get('From', '')),
        'to': str(msg.get('To', '')),
        'date': str(msg.get('Date', '')),
        'message_id': str(msg.get('Message-ID', '')),
        'body_text': text[:MAX_TEXT],
        'text_truncated': len(text) > MAX_TEXT,
        'attachments_not_read': [str(p.get_filename() or '(unnamed)')
                                 for p in msg.iter_attachments()],
    }


def read_folder(account, folder, limit, skip, connect=imaplib.IMAP4_SSL,
                headers_only=False, requested_uids=None, unread_only=True):
    data = account.get('data') or {}
    if account.get('type') != 'imap':
        raise MailReadError('Requested account is not an IMAP account.')
    if (data.get('imap_host') != 'imap.mail.me.com'
            or data.get('imap_port') != 993 or data.get('insecure_tls')):
        raise MailReadError('Account is not configured for verified iCloud IMAP TLS.')
    if not account.get('email') or not data.get('password'):
        raise MailReadError('Requested account has no usable credential.')
    if not folder or any(c in folder for c in '\r\n\x00'):
        raise MailReadError('An exact folder name without control characters is required.')
    quoted = '"' + folder.replace('\\', '\\\\').replace('"', '\\"') + '"'
    conn = connect('imap.mail.me.com', 993,
                   ssl_context=ssl.create_default_context(), timeout=30)
    try:
        try:
            conn.login(account['email'], data['password'])
        except imaplib.IMAP4.error:
            raise MailReadError(
                'Apple rejected IMAP sign-in. Check the primary iCloud Mail '
                'username and app-specific password.') from None
        status, _ = conn.select(quoted, readonly=True)
        if status != 'OK':
            raise MailReadError('Exact folder could not be selected; no fallback attempted.')
        _, validity = conn.response('UIDVALIDITY')
        uidvalidity = (validity[0].decode('ascii')
                       if validity and isinstance(validity[0], bytes) else None)
        if not uidvalidity or not uidvalidity.isdecimal():
            raise MailReadError('Folder did not return a valid UIDVALIDITY.')
        status, result = conn.uid('SEARCH', None, 'UNSEEN' if unread_only else 'ALL')
        if (status != 'OK' or not result
                or (result[0] is not None and not isinstance(result[0], bytes))):
            raise MailReadError('Folder search failed; coverage is unknown.')
        # imaplib represents an empty successful SEARCH as [None] on iCloud.
        uids = (result[0] or b'').split()
        if any(not uid.isdigit() for uid in uids):
            raise MailReadError('Unread search returned invalid message identifiers.')
        uids = sorted(set(uids), key=int, reverse=True)
        if requested_uids is not None:
            if (len(requested_uids) > 200
                    or any(not isinstance(uid, str) or not uid.isdecimal()
                           for uid in requested_uids)):
                raise MailReadError('Requested UIDs must be at most 200 numeric strings.')
            wanted = {uid.encode('ascii') for uid in requested_uids}
            selected = [uid for uid in uids if uid in wanted]
        else:
            selected = uids[skip:skip + limit]
        messages, failures = [], []
        for uid in selected:
            uid_text = uid.decode('ascii')
            try:
                query = ('(FLAGS RFC822.SIZE BODY.PEEK[HEADER])' if headers_only
                         else f'(FLAGS RFC822.SIZE BODY.PEEK[]<0.{MAX_BYTES}>)')
                status, result = conn.uid('FETCH', uid_text, query)
                parts = [p for p in (result or []) if isinstance(p, tuple)
                         and len(p) == 2 and isinstance(p[1], bytes)]
                if status != 'OK' or not parts:
                    raise MailReadError('Message fetch failed.')
                _, raw = parts[0]
                # imaplib may put RFC822.SIZE after the literal in a separate
                # bytes item, rather than in the tuple's first metadata item.
                metadata = []
                for part in result:
                    value = part[0] if isinstance(part, tuple) else part
                    if isinstance(value, bytes):
                        metadata.append(value)
                size_match = re.search(rb'RFC822\.SIZE\s+(\d+)', b' '.join(metadata))
                size = int(size_match.group(1)) if size_match else None
                item = extract(raw)
                item.update(uid=uid_text, bytes_returned=len(raw),
                            message_size=size,
                            body_not_read=headers_only,
                            raw_truncated=(not headers_only
                                           and (size is None or size > len(raw))))
                messages.append(item)
            except Exception:
                # Exception strings can contain provider data or credentials.
                failures.append({'uid': uid_text, 'error': 'Unable to read message.'})
        next_skip = skip + len(selected)
        return {'account_id': account['id'], 'folder': folder,
                'uidvalidity': uidvalidity,
                'selection': 'unread' if unread_only else 'all',
                'message_total': len(uids),
                'unread_total': len(uids) if unread_only else None,
                'skip': skip, 'messages': messages, 'failures': failures,
                'next_skip': (next_skip if requested_uids is None
                              and next_skip < len(uids) else None),
                'untrusted_email_content': True}
    finally:
        try:
            conn.logout()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--account-id', required=True, type=int)
    parser.add_argument('--folder', required=True)
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--skip', type=int, default=0)
    parser.add_argument('--headers-only', action='store_true')
    parser.add_argument('--uids', help='Comma-separated UIDs from the selected folder search')
    parser.add_argument('--all-messages', action='store_true',
                        help='Read all messages in the exact folder; requires that read scope')
    args = parser.parse_args()
    if args.account_id < 1 or not 1 <= args.limit <= 200 or args.skip < 0:
        parser.error('account-id must be positive; limit 1..200; skip nonnegative')
    try:
        if not os.environ.get('GIGAMAIL_ROOT'):
            raise MailReadError('Set the explicit GIGAMAIL_ROOT used during setup.')
        if os.environ.get('GIGAMAIL_DATA_DIR') or os.environ.get('ADE_MAIL_DATA_DIR'):
            raise MailReadError('Clear mail data-directory overrides before reading.')
        from gigamail.core import accounts
        account = accounts.get_account_by_id(args.account_id)
        if not account:
            raise MailReadError('Requested account was not found; no fallback attempted.')
        output = read_folder(account, args.folder, args.limit, args.skip,
                             headers_only=args.headers_only,
                             requested_uids=args.uids.split(',') if args.uids else None,
                             unread_only=not args.all_messages)
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except MailReadError as exc:
        print(json.dumps({'error': str(exc)}))
    except Exception:
        print(json.dumps({'error': 'Mailbox read failed. Check connection and user setup; no secrets included.'}))
    return 1


if __name__ == '__main__':
    sys.exit(main())
