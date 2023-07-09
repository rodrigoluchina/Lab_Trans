from peewee import *

# Instância de conexão com o banco de dados
db = SqliteDatabase('levantamento.db')


class Result(Model):
    id = AutoField()
    name = CharField()
    km = DoubleField()
    distance = DoubleField()
    highway = IntegerField()
    item = CharField()

    class Meta:
        database = db
        db_table = 'results'

class Video(Model):
    name = CharField()
    km_ini = DoubleField()
    km_final = DoubleField()

    class Meta:
        database = db

class Rodovia(Model):
    rodovia = CharField()
    km_ini = DoubleField()
    km_final = DoubleField()

    class Meta:
        database = db

class View(Model):
    highway = IntegerField()
    km = DoubleField()
    buraco = IntegerField()
    remendo = IntegerField()
    Trinca = IntegerField()
    placa = IntegerField()
    drenagem = IntegerField()
    
    class Meta:
        database = db
        view_table = 'views'

class Controle(Model):
    file_name = CharField(unique=True)

    class Meta:
        database = db
        controle_table = 'controle'



def create_tables():
    with db:
        db.create_tables([Result,Video,Rodovia,Controle,View])
