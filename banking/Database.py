import _sqlite3


class Database:
    database_file = 'card.s3db'

    def __init__(self):
        self.conn = _sqlite3.connect(self.database_file)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, execute_data):
        self.cur.execute(execute_data)
        self.commit()

    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS card ("
                         "id INTEGER PRIMARY KEY,"
                         "number TEXT,"
                         "pin TEXT,"
                         "balance INTEGER DEFAULT 0);")
        self.commit()

    def commit(self):
        self.conn.commit()

    def show_result(self):
        return self.cur.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
