"""
JADN Exceptions
"""


class SchemaException(Exception):
    """
    Base JADN Schema Exception
    """


class DuplicateError(SchemaException):
    """
    JADN field/type duplicated in id/name
    """


class FormatError(SchemaException):
    """
    JADN Syntax Error
    """


class OptionError(SchemaException):
    """
    JADN Field/Type option Error
    """


class ValidationError(SchemaException):
    """
    JADN message validation Error
    """
