class ArtifactError(ValueError):
    code = "ARTIFACT_ERROR"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ArtifactNotFoundError(ArtifactError):
    code = "ARTIFACT_PARENT_NOT_FOUND"


class ArtifactInvalidTypeError(ArtifactError):
    code = "ARTIFACT_INVALID_TYPE"


class ArtifactInvalidEntrypointError(ArtifactError):
    code = "ARTIFACT_INVALID_ENTRYPOINT"


class ArtifactPathEscapeError(ArtifactError):
    code = "ARTIFACT_PATH_ESCAPE"


class ArtifactUnsupportedExtensionError(ArtifactError):
    code = "ARTIFACT_UNSUPPORTED_EXTENSION"


class ArtifactFileTooLargeError(ArtifactError):
    code = "ARTIFACT_FILE_TOO_LARGE"


class ArtifactChecksumMismatchError(ArtifactError):
    code = "ARTIFACT_CHECKSUM_MISMATCH"
