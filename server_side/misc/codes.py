import enum


class StatusCode(enum.Flag):
    SUCCESS_OPEN_FILE = enum.auto()
    FAILED_OPEN_FILE = enum.auto()

    SUCCESS_CONNECTION = enum.auto()
    FAILED_CONNECTION = enum.auto()

    SUCCESS_VALIDATE_ADDR = enum.auto()
    FAILED_VALIDATE_ADDR = enum.auto()

    SUCCESS_UPLOAD_FILE = enum.auto()
    FAILED_UPLOAD_FILE = enum.auto()

    SUCCESS_DOWNLOAD_FILE = enum.auto()
    FAILED_DOWNLOAD_FILE = enum.auto()

    SUCCESS_START_SERVER = enum.auto()
    FAILED_START_SERVER = enum.auto()

    SUCCESS_SHUTDOWN_SERVER = enum.auto()
    FAILED_SHUTDOWN_SERVER = enum.auto()
