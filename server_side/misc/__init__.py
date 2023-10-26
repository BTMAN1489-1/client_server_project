from .codes import StatusCode
from .log_message import LOG_MESSAGE


def validate_address(host: str, port: str):
    try:
        int(port)
    except ValueError:
        return StatusCode.FAILED_VALIDATE_ADDR
    else:
        return StatusCode.SUCCESS_VALIDATE_ADDR


def validate_pathname(pathname):
    try:
        with open(pathname, 'r'):
            pass
    except IOError:
        return StatusCode.FAILED_OPEN_FILE
    else:
        return StatusCode.SUCCESS_OPEN_FILE


def create_log(status_code: StatusCode, /, **kwargs):
    pattern = "--{root}:{level}:{message}"
    root = ''
    message = ''
    level = ''
    match status_code:
        case StatusCode.SUCCESS_CONNECTION as key:
            port = kwargs["port"]
            host = kwargs["host"]
            level = "INFO"
            root = "CLIENT"
            message = LOG_MESSAGE[key].format(host=host, port=port)

        case StatusCode.FAILED_CONNECTION as key:
            port = kwargs["port"]
            host = kwargs["host"]
            level = "ERROR"
            root = "CLIENT"
            message = LOG_MESSAGE[key].format(host=host, port=port)

        case StatusCode.SUCCESS_START_SERVER as key:
            port = kwargs["port"]
            host = kwargs["host"]
            level = "INFO"
            root = "SERVER"
            message = LOG_MESSAGE[key].format(host=host, port=port)

        case StatusCode.FAILED_START_SERVER as key:
            port = kwargs["port"]
            host = kwargs["host"]
            level = "ERROR"
            root = "SERVER"
            message = LOG_MESSAGE[key].format(host=host, port=port)

        case StatusCode.SUCCESS_OPEN_FILE as key:
            pathname = kwargs["pathname"]
            level = "INFO"
            root = "CLIENT"
            message = LOG_MESSAGE[key].format(pathname=pathname)
        case StatusCode.FAILED_OPEN_FILE as key:
            pathname = kwargs["pathname"]
            level = "ERROR"
            root = "CLIENT"
            message = LOG_MESSAGE[key].format(pathname=pathname)

        case StatusCode.SUCCESS_UPLOAD_FILE as key:
            pathname = kwargs["pathname"]
            port = kwargs["port"]
            host = kwargs["host"]
            level = "INFO"
            root = "CLIENT"
            message = LOG_MESSAGE[key].format(pathname=pathname, port=port, host=host)

        case StatusCode.FAILED_UPLOAD_FILE as key:
            pathname = kwargs["pathname"]
            port = kwargs["port"]
            host = kwargs["host"]
            level = "ERROR"
            root = "CLIENT"
            message = LOG_MESSAGE[key].format(pathname=pathname, port=port, host=host)

        case StatusCode.SUCCESS_SHUTDOWN_SERVER as key:
            port = kwargs["port"]
            host = kwargs["host"]
            level = "INFO"
            root = "SERVER"
            message = LOG_MESSAGE[key].format(host=host, port=port)
        case StatusCode.FAILED_SHUTDOWN_SERVER as key:
            port = kwargs["port"]
            host = kwargs["host"]
            level = "ERROR"
            root = "SERVER"
            message = LOG_MESSAGE[key].format(host=host, port=port)

        case StatusCode.SUCCESS_DOWNLOAD_FILE as key:
            pathname = kwargs["pathname"]
            port = kwargs["port"]
            host = kwargs["host"]
            level = "INFO"
            root = "SERVER"
            message = LOG_MESSAGE[key].format(pathname=pathname, port=port, host=host)
        case StatusCode.FAILED_DOWNLOAD_FILE as key:
            pathname = kwargs["pathname"]
            port = kwargs["port"]
            host = kwargs["host"]
            level = "ERROR"
            root = "SERVER"
            message = LOG_MESSAGE[key].format(pathname=pathname, port=port, host=host)

        case StatusCode.SUCCESS_VALIDATE_ADDR as key:
            level = "INFO"
            root = "CLIENT"
            message = LOG_MESSAGE[key]
        case StatusCode.FAILED_VALIDATE_ADDR as key:
            level = "ERROR"
            root = "CLIENT"
            message = LOG_MESSAGE[key]

    return message, pattern.format(root=root, level=level, message=message)
