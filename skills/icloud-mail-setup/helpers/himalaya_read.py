#!/usr/bin/env python3
"""Exact-folder Himalaya fallback; credentials go only through an inherited pipe."""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile

from scoped_read import MAX_BYTES, MailReadError, extract


class HimalayaReader:
    def __init__(self, binary, account):
        data = account.get('data') or {}
        if (account.get('type') != 'imap' or data.get('imap_host') != 'imap.mail.me.com'
                or data.get('imap_port') != 993 or data.get('insecure_tls')):
            raise MailReadError('Fallback requires verified iCloud IMAP TLS.')
        if not account.get('email') or not data.get('password'):
            raise MailReadError('Requested account has no usable credential.')
        if not isinstance(data['password'], str) or len(data['password'].encode('utf-8')) > 512:
            raise MailReadError('Requested account has no usable app-specific credential.')
        self.binary, self.account = binary, account

    def run(self, command, family='imap'):
        if family not in {'imap', 'message'}:
            raise MailReadError('Unsupported Himalaya command family.')
        read_fd, write_fd = os.pipe()
        try:
            # An app-specific password is small enough to fit in the pipe.
            os.write(write_fd, self.account['data']['password'].encode('utf-8'))
            os.close(write_fd)
            write_fd = None
            config = ('[accounts.triage]\n'
                      f'email = {json.dumps(self.account["email"])}\n'
                      'imap.server = "imaps://imap.mail.me.com:993"\n'
                      f'imap.sasl.login.username = {json.dumps(self.account["email"])}\n'
                      'imap.sasl.login.password.command = '
                      f'["/bin/cat", "/dev/fd/{read_fd}"]\n')
            with tempfile.TemporaryDirectory(prefix='himalaya-triage-') as temp:
                path = Path(temp) / 'config.toml'
                path.write_text(config, encoding='utf-8')
                os.chmod(path, 0o600)
                env = os.environ.copy()
                for key in ('RUST_LOG', 'RUST_BACKTRACE', 'HIMALAYA_CONFIG',
                            'ALL_PROXY', 'HTTPS_PROXY', 'all_proxy', 'https_proxy'):
                    env.pop(key, None)
                result = subprocess.run([
                    self.binary, '--config', str(path), '--account', 'triage',
                    '--json', '--log-level', 'off', family, *command,
                ], env=env, pass_fds=(read_fd,), capture_output=True, timeout=45)
                if result.returncode:
                    raise MailReadError('Himalaya connection or scoped read failed.')
                return json.loads(result.stdout)
        except (OSError, ValueError, subprocess.SubprocessError):
            raise MailReadError('Himalaya connection or scoped read failed.') from None
        finally:
            os.close(read_fd)
            if write_fd is not None:
                os.close(write_fd)

    def read(self, folder, limit=100, skip=0, headers_only=False,
             requested_uids=None, unread_only=True):
        if not folder or any(c in folder for c in '\r\n\x00'):
            raise MailReadError('An exact folder without control characters is required.')
        def validity():
            status = self.run(['status', folder])
            value = str(status['uid_validity'])
            if not value.isdecimal() or int(value) < 1:
                raise MailReadError('Folder did not return a valid UIDVALIDITY.')
            return value
        uidvalidity = validity()
        search = ['search', '--mailbox', folder]
        if unread_only:
            search.append('--unseen')
        found = self.run(search)
        if not found.get('uid_mode'):
            raise MailReadError('Himalaya search did not return UIDs.')
        uids = sorted({str(i['id']) for i in found['ids']}, key=int, reverse=True)
        if any(not u.isdecimal() or int(u) < 1 for u in uids):
            raise MailReadError('Himalaya returned invalid UIDs.')
        if requested_uids is not None:
            if any(u not in uids for u in requested_uids):
                raise MailReadError('Requested UIDs are outside the selected folder search.')
            selected = list(dict.fromkeys(requested_uids))[:limit]
        else:
            selected = uids[skip:skip + limit]
        messages, failures = [], []
        if selected:
            sequence = ','.join(selected)
            rows = self.run(['fetch', sequence, '--mailbox', folder,
                             '--envelope', '--flags', '--size'])['messages']
            metadata = {str(row['uid']): row for row in rows}
            bodies = {}
            if not headers_only:
                eligible = [u for u in selected if isinstance(metadata.get(u, {}).get('size'), int)
                            and 0 <= metadata[u]['size'] <= MAX_BYTES]
                if eligible:
                    body_rows = self.run(['fetch', ','.join(eligible), '--mailbox', folder,
                                          '--body'])['messages']
                    bodies = {str(row['uid']): row for row in body_rows}
            for uid in selected:
                try:
                    row = metadata[uid]
                    envelope = row['envelope']
                    if headers_only:
                        item = {'subject': envelope.get('subject') or '',
                                'from': ', '.join(envelope.get('from', [])),
                                'to': ', '.join(envelope.get('to', [])),
                                'date': envelope.get('date') or '',
                                'message_id': envelope.get('message_id') or '',
                                'body_text': '', 'text_truncated': False,
                                'attachments_not_read': []}
                        byte_count = 0
                    else:
                        raw = base64.b64decode(bodies[uid]['body'], validate=True)
                        if len(raw) > MAX_BYTES:
                            raise ValueError('Message exceeds bounded read')
                        item = extract(raw)
                        byte_count = len(raw)
                    item.update(uid=uid, bytes_returned=byte_count, message_size=row.get('size'),
                                body_not_read=headers_only, raw_truncated=False)
                    messages.append(item)
                except (KeyError, TypeError, ValueError):
                    failures.append({'uid': uid, 'error': 'Unable to read message within bounded scope.'})
        if validity() != uidvalidity:
            raise MailReadError('UIDVALIDITY changed during fallback; discard this scan and retry.')
        next_skip = skip + len(selected)
        return {'account_id': self.account['id'], 'folder': folder, 'uidvalidity': uidvalidity,
                'selection': 'unread' if unread_only else 'all', 'message_total': len(uids),
                'unread_total': len(uids) if unread_only else None, 'skip': skip,
                'messages': messages, 'failures': failures,
                'next_skip': next_skip if requested_uids is None and next_skip < len(uids) else None,
                'transport': 'himalaya', 'untrusted_email_content': True}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', required=True)
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--skip', type=int, default=0)
    parser.add_argument('--headers-only', action='store_true')
    parser.add_argument('--uids')
    parser.add_argument('--all-messages', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.limit <= 200 or args.skip < 0:
        parser.error('limit must be 1..200; skip must be nonnegative')
    try:
        profile = json.loads(Path(args.profile).read_text())
        mail = profile['mail']
        if args.all_messages and mail['selection'] != 'all_folder_headers':
            raise MailReadError('Profile does not authorize the standing all-folder scope.')
        os.environ['GIGAMAIL_ROOT'] = mail['gigamail_root']
        for key in ('GIGAMAIL_DATA_DIR', 'ADE_MAIL_DATA_DIR', 'ADE_ROOT'):
            os.environ.pop(key, None)
        from gigamail.core import accounts
        account = accounts.get_account_by_id(mail['account_id'])
        if not account:
            raise MailReadError('Requested account not found; no other account attempted.')
        reader = HimalayaReader(mail['fallback']['binary'], account)
        output = reader.read(mail['folder'], args.limit, args.skip, args.headers_only,
                             args.uids.split(',') if args.uids else None, not args.all_messages)
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except MailReadError as exc:
        print(json.dumps({'error': str(exc)}))
    except Exception:
        print(json.dumps({'error': 'Himalaya fallback failed; no secrets included.'}))
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
