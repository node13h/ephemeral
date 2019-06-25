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

import logging

from flask import Flask, render_template, request, make_response

from ephemeral.data import get_message, MessageNotFoundError, IncorrectPinError


application = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@application.route('/')
def hello_world():
    return render_template('root.html')


@application.route('/show/<msg_id>', methods=['POST', 'GET'])
def show(msg_id):
    if request.method == 'POST':
        try:
            message = get_message(msg_id, request.form['pin'])
        except MessageNotFoundError:
            return render_template('not_found.html', msg_id=msg_id), 404
        except IncorrectPinError:
            return render_template('pin.html')

        logger.info('SHOW {}'.format(msg_id))
        response = make_response(render_template('show.html', message=message))

        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        return response

    return render_template('pin.html')
