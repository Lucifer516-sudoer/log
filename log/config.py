import datetime
from platformdirs import user_data_path

APP_NAME = "CatLog"
HOME = user_data_path(
    appname=APP_NAME, version="0.0.1", appauthor="Harish@Lucifer516-sudoer"
)
DB_PATH = HOME / "DataBase" / "CatLogDB.db"
LOG_FOLDER = HOME / "Logs"

__LOG_FILE_FORMAT = "{APP_NAME}_{DATETIME}.log"


def LOG_FILE_NAME() -> str:
    return __LOG_FILE_FORMAT.format(
        APP_NAME=APP_NAME,
        DATETIME=datetime.datetime.now().strftime("%d-%B-%Y_%H-%M-%S"),
    )
