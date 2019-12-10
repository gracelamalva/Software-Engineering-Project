import sys

from app import create_app
from app.main import db

app = create_app()


def main():
    if len(sys.argv) == 2:
        print(sys.argv)

    if sys.argv[1] == 'createdb':
        db.create_all()
    # if sys.argv[1] == 'populate':
    #     populate()
    else:
        print("Run app using 'flask run'")
        print("To create a database use 'python app.py createdb")


if __name__ == "__main__":
    with app.app_context():
        main()
