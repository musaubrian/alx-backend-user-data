#!/usr/bin/env python3
"""
module obfuscates log messages
"""

from typing import List
import re


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
