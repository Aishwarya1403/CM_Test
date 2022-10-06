import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.orm import relationship
import myapp

database_path = "postgresql://postgres:1@localhost:5432/revenue"
db = SQLAlchemy()


def setup_db(app, database_path= database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Mrr(db.Model):
    __tablename__ = 'mrr'

    id = Column(Integer, primary_key=True)
    month = Column(String)
    amount = Column(Integer)

    def __init__(self, month, amount):
        self.month = month
        self.amount = amount
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return{
            'month':self.month,
            'amount':self.amount
        }