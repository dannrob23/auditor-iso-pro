import os
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DEEPSEEK_API_KEY"] = "sk-test-fake"
os.environ["OPENAI_API_KEY"] = "sk-test-fake"
os.environ["GOOGLE_API_KEY"] = "test-fake"
os.environ["GROQ_API_KEY"] = "test-fake"
os.environ["STREAMLIT_AUTH_COOKIE"] = "test"
os.environ["COOKIE_SECRET"] = "test-secret"
os.environ["KB_REPO"] = ""


@pytest.fixture(autouse=True)
def reset_db():
    """Usa un archivo temporal para aislar tests entre sí."""
    import database
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    test_db = Path(tmp.name)

    original_db_path = database.DB_PATH
    database.DB_PATH = test_db

    database.init_db()
    yield
    database.get_conn().close()
    test_db.unlink(missing_ok=True)
    database.DB_PATH = original_db_path
