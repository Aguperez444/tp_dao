from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.unit_of_work.unit_of_work_impl import (
    SqlAlchemyUnitOfWork,
)


def uow_factory(
    sessions: sessionmaker[Session], write: bool = False
) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(sessions, write)
