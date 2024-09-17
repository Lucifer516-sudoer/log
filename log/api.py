import logging
from log.database.db import DB
from log.config import DB_PATH, LOG_FILE_NAME, LOG_FOLDER
from log.database.models import LogInfo
from log.utils.logging import (
    app_logger,
    flet_logger,
    flet_core_logger,
    configure_present_loggers,
    RichConsoleHandler,
    RichFileHandler,
)


class API:
    def __init__(self) -> None:
        self.setup_logging()
        self.db = DB(DB_PATH)

    def setup_logging(self, level: int | str = logging.DEBUG):
        console_handler = RichConsoleHandler(level=level)
        file_handler = RichFileHandler(
            level=level,
            file=LOG_FOLDER / LOG_FILE_NAME(),
        )

        configure_present_loggers(
            [
                app_logger,
                flet_logger,
                flet_core_logger,
            ],
            [
                console_handler,
                file_handler,
            ],
        )

    def add(self, data: LogInfo):
        """
        As the name suggests adds an record to the database

        Args:
            data (LogInfo): The entry object to be added
        """
        self.db.add_row(data)

    def read_all(self, data_type=LogInfo) -> list[LogInfo]:
        """
        Reads all the records from the database

        Args:
            data_type (`LogInfo`, optional): Nothing but the record info class type     . Defaults to LogInfo.

        Returns:
            list[LogInfo]: The list of log records
        """
        return [each for each in self.db.read_all(data_type)]
