import sqlite3


def create_connection(db_file):
    """Create a database connection to the SQLite database specified by the db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


# Creating tables
def create_tables(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summoners (
                summoner_name STRING, 
                wins INT, 
                losses INT, 
                win_rate FLOAT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_id STRING,
                summoner_name STRING, 
                champion_name STRING, 
                win boolean
            )
        ''')
        print("Tables Created Sucessfully")
    except sqlite3.Error as e:
        print(f'SQL Create table error: {e}')


def insert_data_game(conn, game_id, summoner_name, champion_name, win):
    """Insert data into the 'users' table"""
    try:
        cursor = conn.cursor()

        # Assuming args are provided in pairs (name, age)
        cursor.execute("INSERT INTO games (game_id, summoner_name, champion_name, win) VALUES (?, ?, ?,?)",
                       (game_id, summoner_name, champion_name, win))
        print(f"Data inserted successfully: {game_id}, {summoner_name}, {champion_name}, {win}")

        conn.commit()
    except sqlite3.Error as e:
        print(e)


def select_game_data(conn):
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT summoner_name, sum(win) AS wins, (count(*) - sum(win)) AS losses, AVG(win) AS WL FROM games GROUP BY summoner_name")

        rows = cursor.fetchall()
        for row in rows:
            summoners = row[0]
            wins = row[1]
            losses = row[2]
            win_rate = row[3]

            cursor.execute("INSERT INTO summoners (summoner_name, wins, losses, win_rate) VALUES (?, ?, ?, ?)", (summoners, wins, losses, win_rate))

        print(f"Data inserted successfully: summoner WL")
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def close_connection(conn):
    """Close the database connection"""
    if conn:
        conn.close()
        print("Connection closed.")
