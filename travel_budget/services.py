"""
Функция авторизации для Google Sheets API.
# Функция авторизации для Google Drive API.
"""
import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient import discovery


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
load_dotenv()
EMAIL_USER = os.environ['ADMIN_EMAIL']

INFO = {
    'type': os.environ['TYPE'],
    'project_id': os.environ['PROJECT_ID'],
    'private_key_id': os.environ['PRIVATE_KEY_ID'],
    'private_key': os.environ['PRIVATE_KEY'],
    'client_email': os.environ['CLIENT_EMAIL'],
    'client_id': os.environ['CLIENT_ID'],
    'auth_uri': os.environ['AUTH_URI'],
    'token_uri': os.environ['TOKEN_URI'],
    'auth_provider_x509_cert_url': os.environ['AUTH_PROVIDER_X509_CERT_URL'],
    'client_x509_cert_url': os.environ['CLIENT_X509_CERT_URL'],
    'universe_domain': os.environ['UNIVERSE_DOMAIN']
}

CREDENTIALS = Credentials.from_service_account_info(
    info=INFO, scopes=SCOPES)

SHEETS_SERVICE = discovery.build('sheets', 'v4', credentials=CREDENTIALS)
DRIVE_SERVICE = discovery.build('drive', 'v3', credentials=CREDENTIALS)


def auth_sheets():
    """
    Чтобы создать экземпляр класса учётных данных (Credentials), нужно
    передать в метод from_service_account_info имя JSON-файла c учётными
    данными и список уровней доступа к API. А чтобы создать экземпляр класса
    Resource, в котором хранятся методы для работы с Google API, нужно в метод
    build модуля discovery передать название и версию API, с которым предстоит
    работать, а также созданный ранее экземпляр класса Credentials.
    """
    credentials = CREDENTIALS
    service = SHEETS_SERVICE
    return service, credentials


def auth_drive():
    """
    Чтобы создать экземпляр класса учётных данных (Credentials), нужно
    передать в метод from_service_account_info имя JSON-файла c учётными
    данными и список уровней доступа к API. А чтобы создать экземпляр класса
    Resource, в котором хранятся методы для работы с Google API, нужно в метод
    build модуля discovery передать название и версию API, с которым предстоит
    работать, а также созданный ранее экземпляр класса Credentials.
    """
    credentials = CREDENTIALS
    service = DRIVE_SERVICE
    return service, credentials
