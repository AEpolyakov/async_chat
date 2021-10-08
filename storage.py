import sqlite3
import os


class StorageSQL:
    def __init__(self):
        self.base = 'db.sqlite'
        self._tables = []
        self._create_tables()

    def _connection(self):
        return sqlite3.connect(self.base)

    def _create_tables(self):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS clients ("
                           "id int primary key AUTOINCREMENT,"
                           "login CHAR(50),"
                           "info CHAR(100)"
                           ");")
            self._tables.append('clients')
            cursor.execute("CREATE TABLE IF NOT EXISTS clients_history ("
                           "client int REFERENCES clients(id),"
                           "last_seen_time DATETIME,"
                           "ip_address CHAR(20) NOT NULL"
                           ");")
            self._tables.append('clients_history')
            cursor.execute("CREATE TABLE IF NOT EXISTS contacts ("
                           "id int primary key AUTOINCREMENT,"
                           "id_owner int REFERENCES clients(id),"
                           "id_contact int REFERENCES clients(id)"
                           ");")
            self._tables.append('contacts')

    def insert_client(self, client_id: int, name: str, info=''):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO clients (id, login, info) VALUES (?, ?, ?)', (client_id, name, info))

    def insert_client_history(self, client_id: int, name: str, info=''):
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO clients (id, login, info) VALUES (?, ?, ?)', (client_id, name, info))

    def select_by_id(self, table: str, client_id=None):
        if self._is_valid(table):
            with self._connection() as conn:
                cursor = conn.cursor()
                if client_id is None:
                    cursor.execute(f"SELECT * FROM {table};")
                else:
                    cursor.execute("SELECT * FROM clients WHERE id=(?);", (client_id,))
                result = cursor.fetchall()
                return result

    def _is_valid(self, string):
        if string in self._tables:
            return True
        return False
        # import re
        # if re.findall(r'[\(\)\[\]\\\/\;\ ]+', string):
        #     return False
        # return True


from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base


# base = declarative_base()
#
#
# class Client(base):
#     __tablename__ = 'clients'
#     id = Column(Integer, primary_key=True)
#     login = Column(String(50))
#     info = Column(String(100))
#
#     def __init__(self, login, info):
#         self.login = login
#         self.info = info
#
#     def __repr__(self):
#         return f'client {self.login}'
#
#
# class StorageAlc:
#     def __init__(self):
#         self._create_tables()
#
#     @staticmethod
#     def _create_tables():
#         engine = create_engine('sqlite:///db.sqlite', echo=True, pool_recycle=7200)
#
#         metadata = MetaData()
#         clients_table = Table('clients', metadata,
#                               Column('id', Integer, primary_key=True),
#                               Column('login', String(50)),
#                               Column('info', String(100))
#                               )
#         metadata.create_all(engine)





if __name__ == '__main__':
    engine = create_engine('sqlite:///db.sqlite')
    metadata_obj = MetaData()

    client = Table('client', metadata_obj,
                   Column('client_id', Integer, primary_key=True),
                   Column('login', String(50)),
                   Column('info', String(100))
                   )
    # client_contacts = Table('client_contacts', metadata_obj,
    #                         Column('owner_id', Integer, ForeignKey())
    #
    # )




    # storage = StorageAlc()

    # storage = StorageSQL()
    # # [storage.add_client(i, f'client{i}', f'info about client{i}') for i in range(4)]
    #
    # print(storage.select_by_id('clients'))
    # print(storage.select_by_id('clients_history'))
