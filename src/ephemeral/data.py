# Copyright (C) 2019-2023 Sergej Alikov <sergej.alikov@gmail.com>

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

import base64
import hashlib
import json
import os
import uuid

import redis
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

REDIS_HOST = os.environ.get("EPHEMERAL_REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("EPHEMERAL_REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("EPHEMERAL_REDIS_DB", "0"))

store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class MessageNotFoundError(Exception):
    pass


def sha256(b):
    h = hashlib.sha256()
    h.update(b)

    return h.digest()


def b64decode(s):
    return base64.b64decode(s.encode("latin-1"))


def b64encode(b):
    return base64.b64encode(b).decode("latin-1")


def get_message(msg_id, pin):
    try:
        msg = store[msg_id]
    except KeyError:
        raise MessageNotFoundError()

    msg = json.loads(msg)

    iv = b64decode(msg["iv"])
    key = sha256(pin.encode("utf-8"))

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    unpadder = padding.PKCS7(128).unpadder()
    padded_data = decryptor.update(b64decode(msg["body"])) + decryptor.finalize()
    utf8_body = unpadder.update(padded_data) + unpadder.finalize()

    del store[msg_id]

    return utf8_body.decode("utf-8")


def add_message(body, pin):
    key = sha256(pin.encode("utf-8"))

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    msg_id = str(uuid.uuid4())

    msg = {}
    msg["iv"] = b64encode(iv)

    utf8_body = body.encode("utf-8")
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(utf8_body)

    msg["body"] = b64encode(
        encryptor.update(padded_data + padder.finalize()) + encryptor.finalize()
    )

    store[msg_id] = json.dumps(msg)

    return msg_id
