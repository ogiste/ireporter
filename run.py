from app.db_config import connect, create_tables
from app import create_app
import os

FLASK_CONFIG_ENV = os.getenv("FLASK_CONFIG_ENV")
app = create_app(FLASK_CONFIG_ENV)

if __name__ == '__main__':
    app.run()
