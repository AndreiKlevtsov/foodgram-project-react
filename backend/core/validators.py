import re

from django.core.exceptions import ValidationError

REGEX_NAME = re.compile(r'^[\w.@+-]')
REGEX_TAG = re.compile(r'^[-a-zA-Z0-9_ ]+$')
MESSAGE = 'Не соответствует допустимому формату.'


def validate_username(value):
    """
    Проверяет, что username пользователя != 'me'.
    """
    if value == 'me':
        raise ValidationError(
            f'{value} не может быть <me>.',
            params={'value': value},
        )
    if not REGEX_NAME.match(value):
        raise ValidationError(
            f'{value} {MESSAGE}',
            params={'value': value},
        )


def validate_tag_slug(value):
    """
    Проверяет, slug field модели Tag.
    """
    if REGEX_TAG.match(value):
        raise ValidationError(
            f'Тег {value} {MESSAGE}',
            params={'value': value},
        )
