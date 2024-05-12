from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from DjangoBlog.settings import ALLOWED_IMAGE_EXTENSIONS


def get_avatar_upload_path(instance, filename):
    base_path = "avatars"
    return f"{base_path}/{instance.user.username}/{filename}"


def validate_image(value):
    validator = FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
    try:
        validator(value)
        image = Image.open(value)
        image.verify()
    except Exception as ex:
        print(f"{ex.__class__}: {ex}")
        raise ValidationError("Невозможно обработать данное изображение")