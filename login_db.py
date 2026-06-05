import sqlite3

# 1. Connect ke database (otomatis buat kalau belum ada)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# 2. Buat tabel
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# 3. Tambah user (REGISTER)
def register(username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("User berhasil didaftarkan!")

# 4. Login
def login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    
    if result:
        print("Login berhasil! 🎉")
    else:
        print("Login gagal 😭")

# 5. TESTING
register("admin", "1234")
login("admin", "1234")   # harus berhasil
login("admin", "salah")  # harus gagal