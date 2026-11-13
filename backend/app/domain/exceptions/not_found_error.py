from app.domain.exceptions.business_error import BusinessError


class NotFoundError(BusinessError):
    """El recurso solicitado no existe."""
