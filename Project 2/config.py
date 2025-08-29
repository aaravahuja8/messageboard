import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    @staticmethod
    def init_app(app):
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = "28Y$RH@DND2$23%9D$J2Q@WN@3DH2%I"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
