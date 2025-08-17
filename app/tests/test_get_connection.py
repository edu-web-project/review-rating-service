from config.db_config import get_connection
import pyodbc

def test_config ():
    # Test if the connection can be established
    try:
        conn = get_connection()
        assert isinstance(conn, pyodbc.Connection)
        print("✅ Connection test passed!")
        conn.close()
        return True
    except pyodbc.Error as e:
        print(f"❌ Connection failed: {e}")
        assert False, f"Connection failed: {e}"
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        assert False, f"Unexpected error: {e}"

if __name__ == "__main__":
    test_config()
print("__name__:", __name__)
print("__file__:", __file__)
print("__package__:", __package__)
print("__doc__:", __doc__)
