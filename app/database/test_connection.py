from sqlalchemy import text

from app.database.session import engine


def test_database_connection():
    """Test PostgreSQL database connectivity."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(result.scalar())


if __name__ == "__main__":
    test_database_connection()