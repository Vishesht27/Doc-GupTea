"""Custom Authentication & Authorization bearer to authenticate and authorize
users based on the following factors:
1. username
2.password
3.email

This utility class validates generated JWTs and grants scoped access to users
according to their roles.
"""
from docguptea.core.ConfigEnv import config
from docguptea.models import TokenPayload

from datetime import datetime

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from jose import jwt


class JWTBearer(HTTPBearer):
    """Custom bearer to validate access tokens.

    Args:
        auto_error: bool = True. Internal param to allow auto error detection.

    Raises:
        HHTTPException(403): If authentication scheme is not `Bearer`.
        HTTPException(403): If the access token is invalid or expired.
        HTTPException(403): If authorization code is invalid.
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            else:
                is_valid = JWTBearer.token_validation(credentials.credentials)
                if not is_valid:
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def token_validation(token: str) -> bool:
        """Decodes JWTs to check their validity by inspecting expiry and
         authorization code.

        Args:
            token: str. Authenticated `access_token` of the user.

        Returns:
            bool value to indicate validity of the access tokens.

        Raises:
            jwt.JWTError: If decode fails.
            ValidationError: If JWTs are not in RFC 7519 standard.
        """
        try:
            payload = jwt.decode(
                token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                return False

        except(jwt.JWTError, ValidationError):
            return False

        return True
