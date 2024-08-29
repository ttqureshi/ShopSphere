from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin

from .utils.jwt_helper import decode_jwt
import jwt
import re

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        for header in request.headers:
            print(header)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = decode_jwt(token)
                if payload is None:
                    return JsonResponse({'error': 'Invalid or expired token'}, status=401)
                
                request.user_id = payload['user_id']
            except IndexError:
                return JsonResponse({'error': 'Token not provided'}, status=401)
        else:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
        

# patterns = [
#     r'^/$',
#     r'^/products(/.*)?$',
#     r'^/users/register/$',
#     r'^/users/login/$',
#     r'^/users/logout/$',
#     r'^/users/add-to-cart(/.*)?$',
#     r'^/admin(/.*)?$'
# ]
# if any(re.match(pattern, request.path) for pattern in patterns)



##########################################
#             STACK OVERFLOW             #
##########################################
# https://stackoverflow.com/questions/45266728/how-add-authenticate-middleware-jwt-django

# coding=utf-8
# import jwt
# import traceback

# from django.utils.functional import SimpleLazyObject
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth.models import AnonymousUser, User
# from django.conf import LazySettings
# from django.contrib.auth.middleware import get_user

# settings = LazySettings()


# class JWTAuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

#     @staticmethod
#     def get_jwt_user(request):

#         user_jwt = get_user(request)
#         print(type(user_jwt))
#         print(user_jwt.is_authenticated)
#         if user_jwt.is_authenticated:
#             return user_jwt
#         token = request.META.get('HTTP_AUTHORIZATION', None)
#         print(f"token: {token}")

#         user_jwt = AnonymousUser()
#         if token is not None:
#             try:
#                 user_jwt = jwt.decode(
#                     token,
#                     settings.WP_JWT_TOKEN,
#                 )
#                 user_jwt = User.objects.get(
#                     id=user_jwt['data']['user']['id']
#                 )
#             except Exception as e: # NoQA
#                 traceback.print_exc()
#         return user_jwt