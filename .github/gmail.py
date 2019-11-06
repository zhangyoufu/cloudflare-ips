#!/usr/bin/env python3
import base64
import email.message
import email.policy
import google.auth.transport.requests
import google.oauth2.credentials
import html
import os
import sys

body = f'<html><body><pre>{html.escape(sys.stdin.read(), quote=False)}</pre></body></html>'

msg = email.message.EmailMessage(
    policy=email.policy.EmailPolicy(
        linesep='\r\n',
        raise_on_defect=True,
    ),
)
msg['To'] = os.environ['TO']
msg['Subject'] = os.environ['SUBJECT']
msg.set_content(body, subtype='html', cte='quoted-printable')

credentials = google.oauth2.credentials.Credentials(
    token=None,
    refresh_token=os.environ['REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
)
session = google.auth.transport.requests.AuthorizedSession(credentials)
rsp = session.post('https://www.googleapis.com/gmail/v1/users/me/messages/send',
    json={'raw': base64.urlsafe_b64encode(bytes(msg)).decode('ascii')},
    allow_redirects=False,
)
assert rsp.status_code == 200, f'{rsp.status_code} {rsp.reason}\n{rsp.text}'
