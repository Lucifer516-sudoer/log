from pathlib import Path
from sqlite3 import Connection, Cursor, connect
import time
from typing import List

from log.database.models import LogInfo
from log.utils.logging import app_logger


class DB:
    logger = app_logger.getChild("db")

    def __init__(self, db_file: Path):
        self.db_file = db_file
        autocommit_enabled = True
        check_same_thread_enabled = False

        if not self.db_file.exists():
            self.logger.warning(f"DB File: {str(self.db_file.absolute)} not found!!!")
            self.db_file.parent.mkdir(parents=True, exist_ok=True)
            self.db_file.touch()
            self.logger.debug("Created DB File")

        self._connection = connect(
            str(self.db_file.absolute()),
            autocommit=autocommit_enabled,
            check_same_thread=check_same_thread_enabled,
        )
        self._cursor = self._connection.cursor()
        self.logger.info(f"Initialized: {__class__.__name__}")
        self.logger.debug("DB Connection Meta Info:")
        self.logger.debug(f"Autocommit Enabled: {autocommit_enabled}")
        self.logger.debug(f"Check Same Thread Enabled: {check_same_thread_enabled}")
        self.logger.debug(f"DB File Location: {str(self.db_file.absolute())}")
        self.create_table(LogInfo)

    @property
    def connection(self) -> Connection:
        return self._connection

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    def create_table(self, table: type[LogInfo]):
        self.logger.info("Creating table for the DB")
        _sql = f"""
CREATE TABLE IF NOT EXISTS log_info ({','.join(['\n\t'+each.lower() for each in table.model_fields])}
)
"""
        self.logger.debug(f"{_sql}")
        start = time.perf_counter()
        self.cursor.execute(_sql)
        stop = time.perf_counter()
        self.logger.debug(f"Executed in {(stop-start):.5f} s")

    def add_row(self, row: LogInfo):
        self.logger.info("Adding row")
        _number_of_qmarks = len(row.model_fields)
        _qmarks = ""
        self.logger.debug(f"Number of Attributes: {_number_of_qmarks}")
        for i in range(_number_of_qmarks):
            _qmarks += "?, "
        _qmarks = _qmarks[:-2]
        _sql = f"""INSERT INTO log_info VALUES ({_qmarks})"""
        self.logger.debug(f"{_sql}")
        data = row.sql_data()
        start = time.perf_counter()
        self.cursor.execute(_sql, data)
        stop = time.perf_counter()
        self.logger.debug(f"Executed in {(stop-start):.5f} s")
        self.connection.commit()
        self.logger.debug("Committed to DB")

    def add_rows(self, rows: List[LogInfo]):
        self.logger.info("Adding records")
        self.logger.debug(f"Adding {len(rows)} rows")
        for each in rows:
            self.add_row(each)

    def read_all(self, row: type[LogInfo] = LogInfo):
        self.logger.info("Returning all log records")
        return row.load_sql_data(
            self.cursor.execute("""SELECT * FROM log_info""").fetchall()
        )
