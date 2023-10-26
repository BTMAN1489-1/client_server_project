from .codes import StatusCode


LOG_MESSAGE = {
    StatusCode.SUCCESS_OPEN_FILE: "Successful opening of file {pathname}",
    StatusCode.FAILED_OPEN_FILE: "Failed opening of file {pathname}",

    StatusCode.SUCCESS_CONNECTION: "Successful connection to address ({host}:{port})",
    StatusCode.FAILED_CONNECTION: "Failed to connect to address ({host}:{port})",

    StatusCode.SUCCESS_VALIDATE_ADDR: "Successful address validation",
    StatusCode.FAILED_VALIDATE_ADDR: "Failed address validation",

    StatusCode.SUCCESS_UPLOAD_FILE: "Successful uploading of file {pathname} to address ({host}:{port})",
    StatusCode.FAILED_UPLOAD_FILE: "Failed uploading of file {pathname} to address ({host}:{port})"

}
