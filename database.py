import mysql.connector
import os
from dotenv import load_dotenv

"""
Este codigo contem as funcoes para se conectar ao banco de dados e conslutar a placa detectada,
retornando uma mensagem positiva ou negativa
"""

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do banco de dados
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect_db():
    """Estabelece a conexão com o MySQL e imprime mensagens de status."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=int(DB_PORT) 
        )
        print(f"✅ Conectado ao banco de dados: {DB_NAME} em {DB_HOST}:{DB_PORT}")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        return None

def verificar_placa(placa):
    """Verifica se a placa está cadastrada no banco."""
    conn = connect_db()
    if conn is None:
        print("❌ Falha ao conectar ao banco. Não foi possível verificar a placa.")
        return False

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT placa FROM placas WHERE placa = %s;", (placa,))
            result = cur.fetchone()
            if result:
                print(f"✅ Placa encontrada no banco: {placa} (Cancela aberta!)")
                return True
            else:
                print(f"🚫 Placa {placa} **NÃO** encontrada no banco.")
                return False
    except Exception as e:
        print(f"❌ Erro ao consultar banco de dados: {e}")
        return False
    finally:
        conn.close()
        print("🔌 Conexão com o banco fechada.")

if __name__ == "__main__":
    connect_db()  # Teste a conexão
    verificar_placa("ABC1D23")  # Teste com uma placa fictícia
