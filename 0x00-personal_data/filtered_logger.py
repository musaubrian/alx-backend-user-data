#!/usr/bin/env python3
"""
module obfuscates log msgs
"""

from typing import List
import re
import os
import logging
import mysql.connector


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        msg = logging.Formatter(self.FORMAT).format(record)
        result = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)

        return result


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    returns the log message obfuscated
    ---
    Args::
        fields: a list of strings representing all fields to obfuscated
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
            all fields in the log line (message)
    """

    for field in fields:
        expression = "(?<={}=)(.*?)(?={})".format(field, separator)
        message = re.sub(expression, redaction, message)

    return message


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object.
    """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(stream_handler)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    db_connection = mysql.connector.connection(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )

    return db_connection


def main() -> None:
    """
    retrieve all rows in the users table
    and display each row under a filtered format
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    fields = []
    result = []

    for field in cursor.description:
        fields.append(field[0] + "=")

    log = get_logger()

    for row in cursor:
        for i in range(len(fields)):
            result.append(fields[i] + str(row[i]) + ";")
        log.info(" ".join(result))
        result = []

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
