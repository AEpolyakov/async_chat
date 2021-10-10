import sqlite3
import os
import datetime



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
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()


class Client(base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    info = Column(String(100))

    def __init__(self, login, info):
        self.login = login
        self.info = info

    def __repr__(self):
        return f'client {self.login}'


class ClientHistory(base):
    __tablename__ = 'clients_history'
    client_id = Column(ForeignKey(Client.id))
    access_time = Column(DateTime)
    ip_address = Column(String(32))

    def __init__(self, client, access_time, ip_address):
        self.client_id = client.id
        self.access_time = access_time
        self.ip_address = ip_address

    def __repr__(self):
        return f'client {self.client_id}'


if __name__ == '__main__':
    engine = create_engine('sqlite:///db.sqlite')

    base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker()

    Session.configure(bind=engine)

    session = Session()



    client1 = Client('vasya', 'no info about vasya')
    client1_entry1 = ClientHistory(client1, datetime.datetime(2021, 10, 10, 19, 17), '192.168.142.4')
    client1_entry2 = ClientHistory(client1, datetime.datetime(2021, 10, 10, 19, 18), '192.168.142.4')

    session.add_all([client1_entry1, client1_entry2])

    # print(client1)
    # session.add(client1)
    # user_from_session = session.query(Client).filter_by(login='vasya').first()

    session.commit()
