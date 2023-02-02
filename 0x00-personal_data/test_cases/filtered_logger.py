#!/usr/bin/env python3
"""
module obfuscates log msgs
"""

from typing import List
import re
import logging


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
        result = filter_datum(self.fields, self.REDACTION, msg,
                              self.SEPARATOR)

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
