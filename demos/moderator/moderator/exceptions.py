import json
from aiohttp import web


class AdminRESTError(web.HTTPError):
    status_code = 500
    error = 'Unknown Error'

    def __init__(self, message=None, status_code=None, **kwargs):

        if status_code is not None:
            self.status_code = status_code

        super().__init__(reason=message)
        if not message:
            message = self.error

        msg_dict = {'error': message}

        if kwargs:
            msg_dict['error_details'] = kwargs

        self.text = json.dumps(msg_dict)
        self.content_type = 'application/json'


class ObjectNotFound(AdminRESTError):
    status_code = 404
    error = 'Object not found'


class JsonValidaitonError(AdminRESTError):
    status_code = 400
    error = 'Invalid json payload'
