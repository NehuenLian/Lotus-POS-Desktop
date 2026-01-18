import os
from contextlib import contextmanager

from src.data_access.connection import DataBaseConnection
from src.utils.config import get_database_url


@contextmanager
def session_scope():
    db_url = get_database_url()
    connection = DataBaseConnection(db_url)
    session = connection.get_session()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()