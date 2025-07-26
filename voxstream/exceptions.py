"""Custom exceptions for VoxStream"""

class VoxStreamError(Exception):
    """Base exception for VoxStream errors"""
    pass

class ConnectionError(VoxStreamError):
    """Raised when connection fails"""
    pass

class AuthenticationError(VoxStreamError):
    """Raised when authentication fails"""
    pass

class SessionError(VoxStreamError):
    """Raised when session operations fail"""
    pass

class AudioError(VoxStreamError):
    """Raised when audio processing fails"""
    pass

class StreamError(VoxStreamError):
    """Raised when stream operations fail"""
    pass

class ProcessingError(VoxStreamError):
    """Raised when stream processing fails"""
    pass

class ConfigurationError(VoxStreamError):
    """Raised when configuration is invalid"""
    pass

class RateLimitError(VoxStreamError):
    """Raised when rate limits are exceeded"""
    pass

class APIError(VoxStreamError):
    """Raised when the API returns an error"""
    
    def __init__(self, message: str, error_code: str = None, error_type: str = None):
        super().__init__(message)
        self.error_code = error_code
        self.error_type = error_type