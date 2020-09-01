# # -*- coding: utf-8 -*-
# """
# error.py
# error handdler
# """
# from flask import jsonify
# from werkzeug.http import HTTP_STATUS_CODES
# import logging
# logger = logging.getLogger()
#
# return_code = {'Unauthorized':400,
#                'Forbidden':403,
#                'NotFound':404,
#                'Illegalmethod':405,
#                'InternalServerError':500}
#
#
# def api_abort(code, message=None, **kwargs):
#     if message is None:
#         message = HTTP_STATUS_CODES.get(code, '')
#
#     response = jsonify(message=message, **kwargs)
#     return "ok"
#
#
# def invalid_token():
#     response, code = api_abort(return_code['InternalServerError'], message='invalid token')
#     return response, code
#
#
# def register_errors(app):
#     @app.errorhandler(400)
#     def bad_request(e):
#         return api_abort(return_code['Unauthorized'])
#
#     @app.errorhandler(403)
#     def forbidden(e):
#         return api_abort(return_code['Forbidden'])
#
#     @app.errorhandler(404)
#     def database_not_found_error_handler(e):
#         return api_abort(return_code['NotFound'])
#
#     @app.errorhandler(405)
#     def method_not_allowed(e):
#         return api_abort(return_code['Illegalmethod'], message='The method is not allowed for the requested URL.')
#
#     @app.errorhandler(500)
#     def internal_server_error(e):
#         return api_abort(return_code['InternalServerError'], message='An internal server error occurred.')
#
#     # The default_error_handler function as written above will not return any response if the Flask application
#     # is running in DEBUG mode.
#     @app.errorhandler
#     def default_error_handler(e):
#         message = 'An unhandled exception occurred. -> {}'.format(str(e))
#         logger.error(message)
#
#         # if not settings.FLASK_DEBUG:
#         return api_abort(return_code['InternalServerError'], message=message)
