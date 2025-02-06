import sqlite3
from datetime import date

db = sqlite3.connect("url.db", check_same_thread=False)
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
        INSERT INTO users VALUES ("{uid}","{username}","{hash}","{date.today()}",0);
        """
    try:
        cursor.execute(new_user)
        cursor.execute("COMMIT;")
        return True
    except sqlite3.IntegrityError:
        return False

def create_new_url(uid:str, shortURL:str, longURL:str) -> bool:
    excluded = ["","urls","account","login"]
    #ENSURE SHORTURL HAS NO "."
    new_url = f"""
        INSERT INTO urls VALUES ("{shortURL}","{longURL}","{uid}","{date.today()}",0);
        """
    try:
        if shortURL not in excluded:
            cursor.execute(new_url)
            cursor.execute("COMMIT;")
            return True
        else:
            return False
    except sqlite3.IntegrityError:
        return False

def update_user(uid:str, username:str = None, hash:str = None, numURL:int = None):
    update = f"""
    UPDATE users
    SET 
    { (f'username = "{username}"') if username != None else ""}
    {"," if username != None and hash!=None else ""}
    { (f'hash = "{hash}"') if hash != None else ""}
    {"," if (username != None or hash!=None) and numURL !=None else ""}
    { (f'numURL = {numURL}') if numURL != None else ""}
    
    WHERE uid = "{uid}";
    """
    cursor.execute(update)
    cursor.execute("COMMIT;")

def update_url(shortURL:str, longURL: str = None, newShortURL: str = None, numVisitors: int = None):
    update = f"""
    UPDATE urls
    SET 
    {(f'longURL = "{longURL}"') if longURL != None else ""}
    {"," if longURL != None and newShortURL != None else ""}
    {(f'shortURL = "{newShortURL}"') if newShortURL != None else ""}
    {"," if (longURL != None or newShortURL != None) and numVisitors != None else ""}
    {(f'visitors = {numVisitors}') if numVisitors != None else ""}

    WHERE shortURL = "{shortURL}";
    """
    cursor.execute(update)
    cursor.execute("COMMIT;")
def delete_user(uid:str):
    delete = f"""
    DELETE FROM users
    WHERE uid = "{uid}";
    """
    cursor.execute(delete)
    cursor.execute("COMMIT;")

def delete_url(shortURL:str):
    delete = f"""
    DELETE FROM urls
    WHERE shortURL = "{shortURL}";
    """
    cursor.execute(delete)
    cursor.execute("COMMIT;")

def fetch_long_url(shortURL:str) -> str | None:
    get_url = f"""
    SELECT longURL
    FROM urls
    WHERE shortURL = "{shortURL}"
    """
    cursor.execute(get_url)
    results = cursor.fetchone()
    if results != None:
        return results[0]
    else:
        return None
def fetch_urls(uid: str) -> list[str]:
    fetch_urls = f"""
    SELECT *
    FROM urls
    WHERE creator = "{uid}"
    """
    cursor.execute(fetch_urls)
    results = cursor.fetchall()
    return results

def create_tables():
    create_url_table()
    create_user_table()