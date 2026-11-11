class BusinessError(ValueError):
    """Una operación contradice una regla del negocio."""


class NotFoundError(BusinessError):
    """El recurso solicitado no existe."""
