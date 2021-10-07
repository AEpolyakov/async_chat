import sqlite3


class Storage:
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
                    cursor.execute("SELECT * FROM clients WHERE id=(?);", (client_id, ))
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


if __name__ == '__main__':
    storage = Storage()
    # [storage.add_client(i, f'client{i}', f'info about client{i}') for i in range(4)]

    print(storage.select_by_id('clients'))
    print(storage.select_by_id('clients_history'))
