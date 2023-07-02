import json

from docguptea.models import GeneralResponse, TokenSchema


class InvalidCredentialsException(Exception):
    def __init__(self, token_result: GeneralResponse):
        self.token_result = token_result
        self.set_statuses()
        super(InvalidCredentialsException, self).__init__()

    def set_statuses(self):
        self.token_result.status = 'login_failed'

    def __repr__(self):
        return json.dumps(self.token_result)

class ExistingUserException(Exception):
    def __init__(self, response_result: GeneralResponse):
        self.response_result = response_result
        self.set_statuses()
        super(ExistingUserException, self).__init__()

    def set_statuses(self):
        self.response_result.status = f'failed'
        self.response_result.message.append(f'user with this AADHAR Number already has an account')
        self.response_result.message[0] = 'authenticated'

    def __repr__(self):
        return json.dumps(self.response_result)