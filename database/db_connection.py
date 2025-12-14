import mariadb
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self.host = "localhost"
        self.user = "root"
        self.password = "admin123"
        self.database = "librarymanagement_db"
        self.port = 3306
    
    def connect(self):
        """Establish database connection"""
        try:
            if self.connection is None:
                self.connection = mariadb.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
                logger.info("Database connection established successfully")
            return True
        except mariadb.Error as e:
            logger.error(f"Error connecting to MariaDB: {e}")
            return False
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute SQL query"""
        if self.connection is None:
            if not self.connect():
                return None
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                if 'SELECT' in query.upper() or 'SHOW' in query.upper():
                    result = cursor.fetchall()
                    return result
                else:
                    return None
            else:
                self.connection.commit()
                if 'INSERT' in query.upper():
                    return cursor.lastrowid
                else:
                    return cursor.rowcount
                
        except mariadb.Error as e:
            logger.error(f"Database error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def execute_script(self, script_path):
        """Execute SQL script from file"""
        try:
            with open(script_path, 'r') as file:
                sql_script = file.read()
            
            cursor = self.connection.cursor()
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Error executing script: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")

# Singleton instance
db_instance = None

def get_db_connection():
    """Get database connection instance"""
    global db_instance
    if db_instance is None:
        db_instance = Database()
        db_instance.connect()
    return db_instance