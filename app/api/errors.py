from flask import make_response, jsonify


class ApiError(Exception):
    """ Общее api исключение. """

    http_code = None
    api_code = None
    message = None

    errors = []

    def __init__(self, message, http_code, api_code):
        self.http_code = http_code
        self.api_code = api_code
        self.message = message

    def make_response(self):
        return make_response(jsonify({
            'message': self.message,
            'code': self.api_code
        }), self.http_code)

    def __init_subclass__(cls, **kwargs):
        """ Переписывает всевозможные коды ошибок в словарь при каждом новом наследовании. """

        cls.errors.append({
            'http_code': cls.http_code,
            'api_code': cls.api_code,
            'message': cls.message
        })

        super().__init_subclass__(**kwargs)


class AlreadyConfirmedError(ApiError):
    """ Исключение. Повторное подтверждение. """

    http_code = 400
    api_code = 1000
    message = 'Email has already been confirmed.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class InvalidLincError(ApiError):
    """ Исключение. Недействительная ссылка. """

    http_code = 400
    api_code = 1001
    message = 'Invalid link.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class InvalidTokenError(ApiError):
    """ Исключение. Недействительный токен. """

    http_code = 400
    api_code = 1002
    message = 'Invalid token.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class NotConfirmedError(ApiError):
    """ Исключение. Отсутствует подтверждение. """

    http_code = 400
    api_code = 1003
    message = 'Email not confirmed.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class WrongDataError(ApiError):
    """ Исключение. Неверные данные. """

    http_code = 400
    api_code = 1004
    message = 'Wrong username or password.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class RightsError(ApiError):
    """ Исключение. Недостаточно прав. """

    http_code = 400
    api_code = 1005
    message = 'Insufficient rights.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class NotFoundError(ApiError):
    """ Исключение. Не найдено. """

    http_code = 404
    api_code = 1006
    message = 'Not found.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class InsufficientDataError(ApiError):
    """ Исключение. Не все данные переданы. """

    http_code = 400
    api_code = 1007
    message = 'Insufficient data.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class NameUsedError(ApiError):
    """ Исключение. Переданные данные уже были испольщованы. """

    http_code = 400
    api_code = 1008
    message = 'Please use a different username.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)


class EmailUsedError(ApiError):
    """ Исключение. Переданные данные уже были испольщованы. """

    http_code = 400
    api_code = 1009
    message = 'Please use a different email.'

    def __init__(self, message=message):
        super().__init__(message, http_code=self.http_code, api_code=self.api_code)
