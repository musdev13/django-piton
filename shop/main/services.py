import uuid
from pathlib import Path

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import User

MAX_AVATAR_SIZE = 5 * 1024 * 1024
ALLOWED_AVATAR_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def _process_avatar(avatar_file):
    if avatar_file is None:
        return None, None

    ext = Path(avatar_file.name).suffix.lower()
    if ext not in ALLOWED_AVATAR_EXTENSIONS:
        return None, 'unsupported image format'
    if avatar_file.size > MAX_AVATAR_SIZE:
        return None, 'image too large (max 5 MB)'

    try:
        width, height = get_image_dimensions(avatar_file)
    except Exception:
        return None, 'invalid image file'
    if not width or not height:
        return None, 'invalid image file'

    avatar_file.name = f'{uuid.uuid4().hex}{ext}'
    return avatar_file, None


def create_user(*, username, email, password, first_name='', last_name='', birth_date=None, avatar=None):
    if not username:
        raise ValidationError('username is required')
    if not email:
        raise ValidationError('email is required')
    if not password:
        raise ValidationError('password is required')
    if User.objects.filter(username=username).exists():
        raise ValidationError('username already taken')
    if User.objects.filter(email=email).exists():
        raise ValidationError('email already registered')

    avatar_file, avatar_error = _process_avatar(avatar)
    if avatar_error:
        raise ValidationError(avatar_error)

    user = User(
        username=username,
        email=email,
        first_name=first_name or '',
        last_name=last_name or '',
        birth_date=birth_date,
        password_hash=make_password(password),
        avatar=avatar_file,
    )
    user.save()
    return user
