from flask import make_response, jsonify


class ApiError(Exception):
    """ Общее api исключение. """

    def __init__(self, message, http_code, api_code):
        self.http_code = http_code
        self.api_code = api_code
        self.message = message

    def make_response(self):
        return make_response(jsonify({
            # 'status': self.api_code,
            'message': self.message,
            'code': self.api_code
        }), self.http_code)


class AlreadyConfirmedError(ApiError):
    """ Исключение. Повторное подтверждение. """

    def __init__(self, message='Email has already been confirmed.'):
        super().__init__(message, http_code=400, api_code=1000)


class InvalidLincError(ApiError):
    """ Исключение. Недействительная ссылка. """

    def __init__(self, message='Invalid link.'):
        super().__init__(message, http_code=400, api_code=1001)


class InvalidTokenError(ApiError):
    """ Исключение. Недействительный токен. """

    def __init__(self, message='Invalid token.'):
        super().__init__(message, http_code=400, api_code=1002)


class NotConfirmedError(ApiError):
    """ Исключение. Отсутствует подтверждение. """

    def __init__(self, message='Email not confirmed.'):
        super().__init__(message, http_code=400, api_code=1003)


class WrongDataError(ApiError):
    """ Исключение. Неверные данные. """

    def __init__(self, message='Wrong username or password.'):
        super().__init__(message, http_code=400, api_code=1004)


class RightsError(ApiError):
    """ Исключение. Недостаточно прав. """

    def __init__(self, message='Insufficient rights.'):
        super().__init__(message, http_code=400, api_code=1005)


class NotFoundError(ApiError):
    """ Исключение. Не найдено. """

    def __init__(self, message='Not found.'):
        super().__init__(message, http_code=404, api_code=1006)


class InsufficientDataError(ApiError):
    """ Исключение. Не все данные переданы. """

    def __init__(self, message='Insufficient data.'):
        super().__init__(message, http_code=400, api_code=1007)


class NameUsedError(ApiError):
    """ Исключение. Переданные данные уже были испольщованы. """

    def __init__(self, message='Please use a different username.'):
        super().__init__(message, http_code=400, api_code=1008)


class EmailUsedError(ApiError):
    """ Исключение. Переданные данные уже были испольщованы. """

    def __init__(self, message='Please use a different email.'):
        super().__init__(message, http_code=400, api_code=1009)
