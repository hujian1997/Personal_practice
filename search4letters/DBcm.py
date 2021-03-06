import mysql.connector
class UseDatabase:
    def __init__(self, config):
        self.configuration = config
    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
