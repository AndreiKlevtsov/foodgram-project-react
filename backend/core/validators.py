import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Проверяет, что username пользователя != 'me'.
    """
    regex = r'^[\w.@+-]'
    if value == 'me':
        raise ValidationError(
            (f'{value} не может быть <me>.'),
            params={'value': value},
        )
    if not re.match(regex, value):
        raise ValidationError(
            (f'{value} не соотвествует допустимому формату.'),
            params={'value': value},
        )


def validate_tag_slug(value):
    """
    Проверяет, slug field модели Tag.
    """
    regex = r'^[-a-zA-Z0-9_]+$'
    if not re.match(regex, value):
        raise ValidationError(
            (f'{value} не соотвествует допустимому формату.'),
            params={'value': value},
        )
