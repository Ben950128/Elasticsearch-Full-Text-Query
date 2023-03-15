from sanic import Sanic
from dotenv import load_dotenv

app = Sanic(__name__)
load_dotenv()

# import api時會回來import此__init__.py，此時並不再重新讀取此__init__.py，會依照之前讀取的內容抓取，因此必須要先有app再import api
import api