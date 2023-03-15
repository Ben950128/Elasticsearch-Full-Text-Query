# Elasticsearch-Full-Text-Query-API
## 配置Elasticsearch及FSCrawler
配置如https://github.com/Ben950128/ELK-FSCrawler<span>所示。
> **Warning**  
> 啟動FSCrawler時記得把volume路徑修改，例如: ~/docker/docker-elk/tmp/docs路徑改到upload_files
## API
* GET /report?key=""&name="" $\rightarrow$ 可透過關鍵字或是檔案名稱進行全文檢索。
* POST /report $\rightarrow$ 可上傳檔案至upload_files資料夾，供FSCrawler上傳至Elasticsearch。
* GET /page_number?key=""&path="" $\rightarrow$ 搜尋關鍵字在該檔案的第幾頁出現，檔案的path可由上述的GET /report得到。