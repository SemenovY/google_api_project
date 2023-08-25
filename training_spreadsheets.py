"""
Чтобы ваша программа могла создавать и управлять таблицами через Google API,
она должна уметь авторизовываться в сервисном аккаунте.
Теперь можно создавать функцию авторизации, которая из JSON-файла достанет все
данные сервисного аккаунта и позволит вашему приложению использовать
Google API.
Функция должна возвращать экземпляры классов Credentials и Resource.
В Credentials содержатся учётные данные сервисного аккаунта,
а в Resource — методы для работы с Google API.
"""
# Новый импорт.
import os

from dotenv import load_dotenv
# класс Credentials из пакета google.oauth2.service_account для работы с
# учётными данными вашего сервисного аккаунта.
from google.oauth2.service_account import Credentials

# модуль discovery из пакета googleapiclient для взаимодействия приложения
# с API; за это отвечает объект класса Resource;
from googleapiclient import discovery

SCOPES = [
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive",
]

load_dotenv()

# Не забудьте добавить свой электронный адрес в файл .env.
EMAIL_USER = os.environ['GOOGLE_EMAIL']

info = {
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

# функция авторизации
def auth():
    """
    Чтобы создать экземпляр класса учётных данных (Credentials), нужно
    передать в метод from_service_account_file имя JSON-файла c учётными
    данными и список уровней доступа к API. А чтобы создать экземпляр класса
    Resource, в котором хранятся методы для работы с Google API, нужно в метод
    build модуля discovery передать название и версию API, с которым предстоит
    работать, а также созданный ранее экземпляр класса Credentials.
    """
    # Создаём экземпляр класса Credentials.
    credentials = Credentials.from_service_account_info(
                  info=info, scopes=SCOPES
    )
    # Создаём экземпляр класса Resource.
    service = discovery.build("sheets", "v4", credentials=credentials)
    return service, credentials


def create_spreadsheet(service):
    """
    функцию, которая будет создавать документ (spreadsheet)
    и возвращать его ID. Такая функция должна принимать объект класса
    Resource, в вашей программе он содержится в переменной service.
    """
    # Первый шаг — сформировать тело spreadsheet.
    spreadsheet_body = {
        # Свойства документа
        "properties": {
            "title": "Бюджет путешествий",
            "locale": "ru_RU"
        },
        # Второй шаг — описать свойства первого листа (sheet) документа
        # Свойства листов документа.
        "sheets": [{
            "properties": {
                "sheetType": "GRID",
                "sheetId": 0,
                "title": "Отпуск 2077",
                "gridProperties": {
                    "rowCount": 100,
                    "columnCount": 100
                }
            }
        }]
    }

    # request = service.spreadsheets().create(body=spreadsheet_body)
    # response = request.execute()
    # spreadsheet_id = response["spreadsheetId"]
    # print("https://docs.google.com/spreadsheets/d/" + spreadsheet_id)
    # return spreadsheet_id
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheetId = response["spreadsheetId"]
    print("https://docs.google.com/spreadsheets/d/" + spreadsheetId)
    return spreadsheetId





def set_user_permissions(spreadsheetId, credentials):
    permissions_body = {"type": "user",  # Тип учетных данных.
                        "role": "writer",  # Права доступа для учётной записи.
                        "emailAddress": EMAIL_USER}  # Ваш личный
    # гугл-аккаунт.

    # Создаётся экземпляр класса Resource для Google Drive API.
    drive_service = discovery.build("drive", "v3", credentials=credentials)

    # Формируется и сразу выполняется запрос на выдачу прав вашему аккаунту.
    drive_service.permissions().create(
        sendNotificationEmail=False,
        fileId=spreadsheetId,
        body=permissions_body,
        fields='id'
    ).execute()

# Новая функция! Тут обновляются данные документа.
def spreadsheet_update_values(service, spreadsheetId):
    # Данные для заполнения: выводятся в таблице сверху вниз, слева направо.
    table_values = [
        ['Бюджет путешествий'],
        ['Весь бюджет', '5000'],
        ['Все расходы', '=SUM(E7:E30)'],
        ['Остаток', '=B2-B3'],
        ['Расходы'],
        ['Описание', 'Тип', 'Кол-во', 'Цена', 'Стоимость'],
        ['Перелет', 'Транспорт', '2', '400', '=C7*D7']
    ]

    # Тело запроса.
    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    # Формирование запроса к Google Sheets API.
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range='Отпуск 2077!A1:F20',
        valueInputOption='USER_ENTERED',
        body=request_body
    )
    # Выполнение запроса.
    request.execute()



# Вызов функций.
service, credentials = auth()
spreadsheetId = create_spreadsheet(service)
set_user_permissions(spreadsheetId, credentials)
spreadsheet_update_values(service, spreadsheetId)

# =^..^=______/
# kaonashi
