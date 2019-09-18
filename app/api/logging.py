from app import app
from flask import request, g
from functools import wraps


def logging_request(logging_rr=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if logging_rr:
                app.logger.info({'request': request.get_json() or {}})
            app.logger.info({
                'user_id': g.current_user.id if 'current_user' in g and g.current_user else None
            })

            response = func(*args, **kwargs)

            if logging_rr:
                app.logger.info({'response': response.get_json() or {}})

            return response
        return wrapper
    return decorator


# def logging_request(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         app.logger.info({'request': request.get_json() or {}})
#         app.logger.info({
#             'user_id': g.current_user.id if 'current_user' in g and g.current_user else None
#         })
#
#         response = func(*args, **kwargs)
#
#         app.logger.info({'response': response.get_json() or {}})
#         return response
#
#     return wrapper
