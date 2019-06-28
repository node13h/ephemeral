# Copyright (C) 2019 Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import uuid
import json
import base64

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
import redis

REDIS_HOST = os.environ.get('EPHEMERAL_REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.environ.get('EPHEMERAL_REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('EPHEMERAL_REDIS_DB', '0'))

store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class IncorrectPinError(Exception):
    pass


class MessageNotFoundError(Exception):
    pass


def pad(s):
    pad_by = AES.block_size - len(s) % AES.block_size
    return s + bytes([pad_by]) * pad_by


def unpad(s):
    return s[0:-s[-1]]


def sha256(b):
    h = SHA256.new()
    h.update(b)

    return h.digest()


def b64decode(s):
    return base64.b64decode(s.encode('latin-1'))


def b64encode(b):
    return base64.b64encode(b).decode('latin-1')


def get_message(msg_id, pin):

    try:
        msg = store[msg_id]
    except KeyError:
        raise MessageNotFoundError()

    msg = json.loads(msg)

    iv = b64decode(msg['iv'])
    key = sha256(pin.encode('utf-8'))

    c = AES.new(key, AES.MODE_CBC, iv)

    padded_utf8_body = c.decrypt(b64decode(msg['body']))

    if b64decode(msg['hash']) != sha256(padded_utf8_body):
        raise IncorrectPinError()

    # Delete only when PIN has been confirmed to be correct
    del store[msg_id]

    return unpad(padded_utf8_body).decode('utf-8')


def add_message(body, pin):
    key = sha256(pin.encode('utf-8'))

    iv = Random.new().read(AES.block_size)

    c = AES.new(key, AES.MODE_CBC, iv)

    msg_id = str(uuid.uuid4())

    msg = {}
    msg['iv'] = b64encode(iv)

    padded_utf8_body = pad(body.encode('utf-8'))

    msg['hash'] = b64encode(sha256(padded_utf8_body))
    msg['body'] = b64encode(c.encrypt(padded_utf8_body))

    store[msg_id] = json.dumps(msg)

    return msg_id
