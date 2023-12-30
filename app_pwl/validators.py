import re

from rest_framework.serializers import ValidationError

VALID_LINK = ["youtube.com", "youtu.be"]


class LinkValidator:
    """
    Валидация текстовых полей на предмет разрешенных ссылок
    Разрешены только ссылки на youtube.com
    """
    def __init__(self, *args):  # Можно указывать несколько полей списком
        self.fields = args

    def __call__(self, value):
        val_dict = {field: dict(value).get(field) for field in self.fields}
        reg = re.compile('^(https?:\/\/)?'  # протокол
                         '([\w-]{1,32}\.[\w-]{1,32})'  # домен
                         '([^\s@]*)'  # любой не пробельный символ + @ для исключения из проверки email адресов
                         '$')
        for field, value in val_dict.items():
            if value:
                for value in value.split():
                    text = bool(reg.match(value))
                    if text:
                        if not value.lstrip("https://www.").split("/")[0] in VALID_LINK:
                            raise ValidationError(f"Invalid link: '{value}' in the '{field}' field. "
                                                  f"You can only post links to youtube.com or email")
