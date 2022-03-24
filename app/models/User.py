from peewee import *
from .db import database as db


class User(Model):
    firstname = CharField()
    secondname = CharField()
    id = CharField(unique=True)

    class Meta:
        database = db
