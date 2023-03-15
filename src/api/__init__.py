from __init__ import app
from .ReportInElasticsearch import ReportInElasticsearch, KeywordInWhichPage

# PDF全文檢索
app.add_route(ReportInElasticsearch.as_view(), '/report')

# 關鍵字檢索頁碼
app.add_route(KeywordInWhichPage.as_view(), '/page_number')