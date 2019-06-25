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

from unittest.mock import patch

import pytest

import ephemeral.data as ed


@patch.object(ed, 'store', dict())
def test_can_get_added():
    msg = 'The quick brown fox jumps over the lazy dog'
    pin = '123789'

    msg_id = ed.add_message(msg, pin)

    assert ed.get_message(msg_id, pin) == msg


@patch.object(ed, 'store', dict())
def test_can_get_multiple():
    msg1 = 'The quick brown fox jumps over the lazy dog'
    pin1 = '123789'

    msg2 = 'The five boxing wizards jump quickly'
    pin2 = '000000'

    msg_id1 = ed.add_message(msg1, pin1)
    msg_id2 = ed.add_message(msg2, pin2)

    assert ed.get_message(msg_id1, pin1) == msg1
    assert ed.get_message(msg_id2, pin2) == msg2


@patch.object(ed, 'store', dict())
def test_unicode_supported():
    msg = 'a\xac\u1234\u20ac\U00008000'
    pin = '123789'

    msg_id = ed.add_message(msg, pin)

    assert ed.get_message(msg_id, pin) == msg


@patch.object(ed, 'store', dict())
def test_incorrect_pin_raises():
    msg_id = ed.add_message('TEST', '123456')

    with pytest.raises(ed.IncorrectPinError):
        ed.get_message(msg_id, '654321')


@patch.object(ed, 'store', dict())
def test_non_existing_id_raises():
    with pytest.raises(ed.MessageNotFoundError):
        ed.get_message('NON-EXISTING-ID', '000000')


@patch.object(ed, 'store', dict())
def test_get_twice_raises():
    msg_id = ed.add_message('TEST', '123456')

    ed.get_message(msg_id, '123456')

    with pytest.raises(ed.MessageNotFoundError):
        ed.get_message(msg_id, '123456')
