from lobe.settings.common import *

SECRET_KEY = 'CHANGE_THIS'
SECURITY_PASSWORD_SALT = 'SOME_SALT'

RECAPTCHA_PUBLIC_KEY = '6Lcan7IUAAAAACXrZazA4OeWJ2ZAC1DdxgNK8wUX'
RECAPTCHA_PRIVATE_KEY = '6Lcan7IUAAAAANSmBbECrHlpz5EzSqNVX4uDiwH4'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/lobe_dev_db_4'

TAL_API_TOKEN = 'ak_JLedkaWqqORPpYByLXeZjMG4JN0rQkwZ4zn6zg28WmvE57oK9badDAlV12PY5Xo0'

DEBUG = True
FLASK_DEBUG = True