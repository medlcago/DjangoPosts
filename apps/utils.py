from typing import TYPE_CHECKING

from PIL import Image
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile

from DjangoPosts.settings import ALLOWED_IMAGE_EXTENSIONS, AVATARS_BASE_PATH

if TYPE_CHECKING:
    from apps.users.models import Profile


def set_attrs(class_: Model, data: dict, validate: bool = True) -> dict | None:
    for key, value in data.items():
        setattr(class_, key, value)
    if validate:
        return full_clean(class_)


def full_clean(class_: Model) -> dict | None:
    try:
        class_.full_clean()
    except ValidationError as ex:
        error_dict = ex.message_dict
        errors = {field: messages for field, messages in error_dict.items()}
        return errors


def get_avatar_upload_path(instance: "Profile", filename: str) -> str:
    return AVATARS_BASE_PATH.format(username=instance.user.username, filename=filename)


def validate_image(value: ImageFieldFile) -> None:
    validator = FileExtensionValidator(allowed_extensions=ALLOWED_IMAGE_EXTENSIONS)
    try:
        validator(value)
        image = Image.open(value)
        image.verify()
    except Exception as ex:
        print(f"{ex.__class__}: {ex}")
        raise ValidationError("Невозможно обработать данное изображение")
