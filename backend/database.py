import mysql.connector.pooling
from backend.config import db_config, pool_setting

class Database:
    def __init__(self, db_config, pool_setting):
        self.config = db_config
        self.pool_setting = pool_setting
        self.pool = self.create_pool()

    def create_pool(self):
        pool = mysql.connector.pooling.MySQLConnectionPool(pool_name=self.pool_setting['pool_name'],
                                                                    pool_size=self.pool_setting['pool_size'],
                                                                    **self.config)
        print("Database connection pool created.")
        return pool


    def close(self, conn, cursor):

        cursor.close()
        conn.close()

    def execute_query(self, query, params=None, commit=False):

        connection = self.pool.get_connection()
        cursor = connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if commit:
            connection.commit()
            self.close(connection, cursor)
            return None

        else:
            res = cursor.fetchall()
            self.close(connection, cursor)
            return res

db = Database(db_config,pool_setting)