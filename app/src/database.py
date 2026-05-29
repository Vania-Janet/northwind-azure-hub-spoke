import config


def _get_connection():
    if not config.AZURE_SQL_SERVER:
        return None
    try:
        import pymssql
        return pymssql.connect(
            server=config.AZURE_SQL_SERVER,
            user=config.AZURE_SQL_USER,
            password=config.AZURE_SQL_PASSWORD,
            database=config.AZURE_SQL_DATABASE,
            timeout=5,
        )
    except Exception:
        return None


def ensure_table():
    conn = _get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'chat_history')
            CREATE TABLE chat_history (
                id          INT IDENTITY PRIMARY KEY,
                user_id     NVARCHAR(255) NOT NULL,
                department  NVARCHAR(50)  NOT NULL,
                role        NVARCHAR(20)  NOT NULL,
                content     NVARCHAR(MAX) NOT NULL,
                created_at  DATETIME      DEFAULT GETDATE()
            )
        """)
        conn.commit()
    finally:
        conn.close()


def save_message(user_id: str, department: str, role: str, content: str):
    conn = _get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_id, department, role, content) VALUES (?, ?, ?, ?)",
            user_id, department, role, content,
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def get_history(user_id: str, limit: int = 20) -> list:
    conn = _get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, content FROM (
                SELECT TOP (?) role, content, created_at
                FROM chat_history
                WHERE user_id = ?
                ORDER BY created_at DESC
            ) sub
            ORDER BY created_at ASC
        """, limit, user_id)
        return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    except Exception:
        return []
    finally:
        conn.close()
