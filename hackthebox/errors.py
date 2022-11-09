class HtbException(Exception):
    """Base exception class for `hackthebox`"""

    pass


class ApiError(HtbException):
    """The API responded in an unexpected way"""


class AuthenticationException(HtbException):
    """An error authenticating to the API"""

    pass


class NotFoundException(HtbException):
    """The API returned a 404 response for this request"""

    pass


class MissingEmailException(AuthenticationException):
    """An email was not given where it was required"""

    pass


class MissingPasswordException(AuthenticationException):
    """A password was not given where it was required"""

    pass


class MissingOTPException(AuthenticationException):
    """An OTP was not given but 2FA is enabled"""

    pass


class IncorrectOTPException(AuthenticationException):
    """An OTP was given but not accepted"""

    pass


class VpnException(HtbException):
    """An error associated with the VPN"""

    pass


class CannotSwitchWithActive(VpnException):
    """Failed to switch VPN because the user has an active machine"""

    pass


class MachineException(HtbException):
    """An error associated with a machine"""

    pass


class TooManyResetAttempts(MachineException):
    """Error for too many reset attempts"""

    pass


class UnknownSolveException(HtbException):
    """An unknown solve type was passed"""

    pass


class SolveError(HtbException):
    """Exceptions for solving"""


class IncorrectFlagException(SolveError):
    """An incorrect flag was submitted"""

    pass


class UserAlreadySubmitted(SolveError):
    """Player has already completed the user flag for this box"""

    pass


class RootAlreadySubmitted(SolveError):
    """Player has already completed the root flag for this box"""


class IncorrectArgumentException(HtbException):
    """An incorrectly formatted argument was passed"""

    reason: str

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"IncorrectArgumentException(reason='{self.reason}')"

    def __init__(self, reason: str):
        self.reason = reason

    pass


class NoDockerException(HtbException):
    """A challenge was 'started' when no Docker is available"""

    pass


class NoDownloadException(HtbException):
    """A challenge was 'downloaded' when no download is available"""

    pass


class RateLimitException(HtbException):
    """An internal ratelimit to prevent spam was violated"""

    def __init__(self, message):
        print(message)
        super().__init__(message)


class CacheException(HtbException):
    """There was an issue with the token cache"""

    pass
