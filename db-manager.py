import sqlite3

db = sqlite3.connect("url.db")
cursor = db.cursor()
def table_exists(table_name: str) -> bool:
    '''
    :param table_name: Table to check if it exists
    :return: True if it exists, otherwise false
    '''
    check_exists = f"""
    SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
    """
    cursor.execute(check_exists)
    if len(cursor.fetchall()) == 0:
        return False
    else:
        return True

def create_user_table() -> bool:
    '''
    Creates the starter user table, returns true if table is created (doesn't already exist), false otherwise
    '''

    if not table_exists("users"):
        create_table = """
        CREATE TABLE users (
        uid TEXT PRIMARY KEY,
        username VARCHAR(16),
        hash TEXT,
        joinDate DATE,
        numURL SMALLINT
        );
        """
        cursor.execute(create_table)
        return True
    else:
        return False

def create_url_table() -> bool:
    '''
    Creates the starter URL table, returns true if table is created (doesn't already exist), false otherwise
    '''
    if not table_exists("urls"):
        create_table = """
        CREATE TABLE urls (
        shortURL TEXT PRIMARY KEY,
        longURL TEXT,
        creator TEXT,
        creationDate DATE,
        visitors INTEGER
        );
        """
        cursor.execute(create_table)
        return True
    else:
        return False

def create_new_user(uid:str, username: str, hash:str) -> bool:
    '''
    :param uid: Server generated UUID
    :param username: user chosen nickname
    :param hash: password hash\
    :return: Returns true if account creation was successful
    '''
    new_user = f"""
        INSERT INTO users VALUES ("{uid}","{username}","{hash}","2025-07-08",0);
        """
    try:
        cursor.execute(new_user)
        cursor.execute("COMMIT;")
        return True
    except sqlite3.IntegrityError:
        return False

def create_tables():
    create_url_table()
    create_user_table()
create_new_user("1235","Bingus","password-tee-hee")