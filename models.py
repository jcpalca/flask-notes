from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)



class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         nullable=False,
                         primary_key=True,
                         unique=True)

    password = db.Column(db.String(100),
                         nullable=False)

    email = db.Column(db.String(50),
                         nullable=False,
                         unique=True)

    first_name = db.Column(db.String(30),
                         nullable=False)

    last_name = db.Column(db.String(30),
                         nullable=False)
    # start_register
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username,
                    password=hashed,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate
