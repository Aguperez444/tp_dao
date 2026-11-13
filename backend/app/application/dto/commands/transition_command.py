from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class TransitionCommand:
    responsable: str
    observacion: str = ""
    codigo_precinto: str = ""
    numero_remito: str = ""
    precinto_intacto: bool = False
    contenido_conforme: bool = False
