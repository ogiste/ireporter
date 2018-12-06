from app.db_config import connect, create_tables
from app import create_app

connect("ireporter")
create_tables()

app = create_app("development")

if __name__ == '__main__':
    app.run()
