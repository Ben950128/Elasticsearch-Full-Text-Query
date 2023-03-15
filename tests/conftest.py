import pytest
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture
def api_prefix():
	return 'http://127.0.0.1:6685/'