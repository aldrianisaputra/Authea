from database import cursor, conn
from datetime import datetime

def register(username, password):
    if not username or not password:
        return False

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO logs (username, login_time) VALUES (?, ?)", (username, waktu))
        conn.commit()
        return True

    return False

def get_logs():
    cursor.execute("SELECT username, login_time FROM logs ORDER BY login_time DESC")
    return cursor.fetchall()