from __init__ import app
from .ReportInElasticsearch import ReportInElasticsearch, KeyWordInReport

# PDF全文檢索
app.add_route(ReportInElasticsearch.as_view(), '/report')

# 關鍵字檢索頁碼
app.add_route(KeyWordInReport.as_view(), '/page_number')