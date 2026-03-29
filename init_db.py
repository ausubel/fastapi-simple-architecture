import os
import sqlite3
from pathlib import Path
from app.presentation.dependencies.deps import get_db_client

def init_db():
    print("Inicializando la base de datos...")
    
    # Obtener el cliente actual (Postgres o SQLite basado en la variable de entorno actual)
    db = get_db_client()
    
    # Leer el esquema SQL
    schema_path = Path(__file__).resolve().parent / "docs" / "database" / "schema_postgres.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Si estamos corriendo SQLite (comportamiento por defecto), ajustamos la sintaxis de Postgres
    is_sqlite = "sqlite" in db.__class__.__name__.lower()
    if is_sqlite:
        sql = sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        sql = sql.replace("BOOLEAN", "INTEGER")
        
    try:
        if is_sqlite:
            # SQLite requiere usar executescript para bloques que tienen múltiples sentencias
            db.conn.executescript(sql)
            db.conn.commit()
        else:
            # En Postgres / psycopg2 basta con correr todo el bloque junto
            cur = db.conn.cursor()
            cur.execute(sql)
            db.conn.commit()
            cur.close()
            
        print("¡Base de datos inicializada correctamente! 🚀")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        db.conn.rollback()

if __name__ == "__main__":
    init_db()
