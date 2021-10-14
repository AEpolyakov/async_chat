import datetime
from sqlalchemy import create_engine, update, delete
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    info = Column(String(100))

    def __init__(self, login: str, info='no info'):
        self.login = login
        self.info = info

    def __repr__(self):
        return f'{self.id=} {self.login=} {self.info=}'


class ClientHistory(Base):
    __tablename__ = 'client_history'
    history_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    access_time = Column(DateTime)
    ip_address = Column(String(32))

    def __init__(self, client: Client, access_time: datetime, ip_address=''):
        self.client_id = client.id
        self.access_time = access_time
        self.ip_address = ip_address

    def __repr__(self):
        return f'{self.history_id} {self.client_id} {self.ip_address} {self.access_time}'


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('client.id'))
    contact_id = Column(Integer, ForeignKey('client.id'))

    def __init__(self, owner: Client, client: Client):
        self.owner_id = owner.id
        self.contact_id = client.id

    def __repr__(self):
        return f'{self.owner_id} {self.contact_id}'


class ClientContactList(Base):
    __tablename__ = 'client_contact_list'
    id = Column(Integer, primary_key=True)
    contact_login = Column(String(50))

    def __init__(self, contact_login: str):
        self.contact_login = contact_login

    def __repr__(self):
        return f'{self.contact_login}'


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True)
    message_from = Column(String(50))
    message_to = Column(String(50))
    text = Column(String(256))
    send_time = Column(DateTime)

    def __init__(self, message_from: str, message_to: str, text: str, send_time: datetime):
        self.message_from = message_from
        self.message_to = message_to
        self.text = text
        self.send_time = send_time

    def __repr__(self):
        return f'message {self.message_from} {self.message_to} {self.text[:10]} {self.send_time}'


class Storage:
    def __init__(self, base_name):
        self._engine = create_engine(f'sqlite:///{base_name}_db.sqlite')
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)

    def insert(self, Obj: Base, *args):
        with self._Session() as session:
            inserting_object = Obj(*args)
            session.add(inserting_object)
            session.commit()

    def select(self, Obj: Base, filter_by, filter_value):
        with self._Session() as session:
            result = session.query(Obj).filter(getattr(Obj, filter_by).like(filter_value))
        return result

    def delete(self, Obj: Base, filter_by, filter_value):
        with self._Session() as session:
            session.query(Obj).filter(getattr(Obj, filter_by) == filter_value).delete()
            session.commit()

    def update(self, Obj: Base, filter_by, filter_value, update_field, update_value):
        with self._Session() as session:
            session.query(Obj).filter(getattr(Obj, filter_by) == filter_value).update({update_field: update_value})
            session.commit()


if __name__ == '__main__':

    storage = Storage()
    # storage.insert(Client, 'John', 'info about John')
    # storage.insert(Client, 'Tom', 'info about Tom')
    # storage.insert(Client, 'Paul', 'info about Paul')

    # client_John = storage.select(Client, 'login', 'John').first()
    # client_Tom = storage.select(Client, 'login', 'Tom').first()
    # client_Paul = storage.select(Client, 'login', 'Paul').first()

    # storage.insert(ClientHistory, client_John, datetime.datetime.now(), '127.0.0.1:7891')
    # storage.insert(ClientHistory, client_John, datetime.datetime.now(), '127.0.0.1:7891')
    # storage.insert(ClientHistory, client_Tom, datetime.datetime.now(), '127.0.0.1:7892')
    #
    # storage.insert(ContactList, client_John, client_Tom)
    # storage.insert(ContactList, client_Tom, client_John)
    # storage.insert(ContactList, client_Tom, client_Paul)

    # print(storage.select(Client, 'login', 'John').first())
    # print(storage.select(ClientHistory, 'client_id', 1).all())
    # print(storage.select(ContactList, 'owner_id', 1).all())

    # storage.delete(Client, 'login', 'Paul')
    # storage.update(Client, 'login', 'Paul', 'info', '123updated info about Paul')
