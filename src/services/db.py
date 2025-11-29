import psycopg2
from psycopg2 import sql


class PostgresService:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        """Connect to the configured database. If the database does not exist,
        attempt to create it by connecting to the default 'postgres' database
        and issuing CREATE DATABASE, then reconnect.
        """
        try:
            self.conn = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                dbname=self.config['dbname']
            )
            return self.conn
        except psycopg2.OperationalError as e:
            msg = str(e)
            if 'does not exist' in msg or 'database "' in msg and 'does not exist' in msg:
                # Connect to default 'postgres' database to create the target database
                tmp_conn = psycopg2.connect(
                    host=self.config['host'],
                    port=self.config['port'],
                    user=self.config['user'],
                    password=self.config['password'],
                    dbname='postgres'
                )
                tmp_conn.autocommit = True
                cur = tmp_conn.cursor()
                cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(self.config['dbname'])))
                cur.close()
                tmp_conn.close()

                # Try connecting again to the newly created database
                self.conn = psycopg2.connect(
                    host=self.config['host'],
                    port=self.config['port'],
                    user=self.config['user'],
                    password=self.config['password'],
                    dbname=self.config['dbname']
                )
                return self.conn
            else:
                raise

    def close(self):
        if self.conn:
            self.conn.close()
