"""
utility file
"""
from django.http import JsonResponse


def get_token(post_data):
    if 'app_token' in post_data:
        return post_data['app_token']
    else:
        return False


def get_error_res(message, status):
    return JsonResponse({'result': 'Error', 'message': message}, status=status)


def get_success_res(message, status=200):
    return JsonResponse({'result': 'Success', 'message': message}, status=status)
