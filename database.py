# app/database.py
from peewee import SqliteDatabase
from models.allmodels import create_tables

#Instância de conexão com o banco de dados
db = SqliteDatabase('levantamento.db')

create_tables()