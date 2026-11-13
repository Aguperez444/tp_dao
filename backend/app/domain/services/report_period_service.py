from datetime import date, timedelta

from app.domain.exceptions.business_error import BusinessError


class ReportPeriodService:
    @staticmethod
    def range(since: date, until: date) -> tuple[str, str]:
        if until < since or until == date.max:
            raise BusinessError("El período de consulta no es válido.")
        return since.isoformat(), (until + timedelta(days=1)).isoformat()
