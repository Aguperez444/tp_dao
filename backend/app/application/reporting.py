from datetime import date, timedelta
from app.domain.errors import BusinessError


class ReportingService:
    def __init__(self, repository):
        self.repository = repository

    def range(self, since: date, until: date):
        if until < since or until == date.max:
            raise BusinessError('El período de consulta no es válido.')
        return since.isoformat(), (until + timedelta(days=1)).isoformat()

    def generate(self, since, until, local=None):
        start, end = self.range(since, until)
        return {'desde':since.isoformat(),'hasta':until.isoformat(),'establecimiento_id':local,
                **self.repository.generate(start,end,local)}

    def stock(self,local=None):
        return self.repository.stock(local)

    def movements(self,since,until,local=None):
        start,end = self.range(since,until)
        return self.repository.movements(start,end,local)
