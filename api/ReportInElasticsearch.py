from __init__ import app
from sanic.views import HTTPMethodView
from sanic.response import json
from elasticsearch import AsyncElasticsearch
import asyncio
import aiofiles
import os
import PyPDF2

async def download_files(execute_unit, file_body, file_name):
    prefix_path = f'./upload_files/{execute_unit}/'
    if not os.path.exists(prefix_path):
        os.makedirs(prefix_path)
    async with aiofiles.open(prefix_path+file_name, 'wb') as f:
        await f.write(file_body)


# 成果報告資料
class ReportInElasticsearch(HTTPMethodView):
    async def get(self, request):
        key_ls = request.args.getlist('key')
        name = request.args.get('name')
        if key_ls == None and name == None:
            result = {'status': 'fail', 'msg': '請輸入搜尋參數'}
            return json(result, status=200, ensure_ascii=False)

        query = {'bool': {'must': []}}
        if name != None:
            match_phrase = {'match_phrase': {'file.filename': name}}
            query['bool']['must'].append(match_phrase)

        if key_ls != None:
            for key in key_ls:
                match_phrase = {'match_phrase': {'content': key}}
                query['bool']['must'].append(match_phrase)

        usename = os.getenv('ELASTICSEARCH_USERNAME')
        password = os.getenv('ELASTICSEARCH_PASSWORD')
        es = AsyncElasticsearch(hosts='http://host.docker.internal:9200', basic_auth=(usename, password))
        resp = await es.search(index='upload_files', query=query, from_=0, size=10)
        result = []
        resp_dict = dict(resp)['hits']['hits']

        for data in resp_dict:
            file_name = data['_source']['file']['filename']
            file_relative_path = data['_source']['path']['virtual']
            pdf_path = './upload_files'+ file_relative_path
            data_dict = {
                '檔案名稱': file_name,
                '檔案位置': pdf_path
            }
            result.append(data_dict)
        await es.close()
        return json(result, status=200, ensure_ascii=False)


    async def post(self, request):
        files = request.files['files']
        execute_unit = request.form['execute_unit'][0]
        tasks = []
        for file in files:
            file_name = file.name
            file_body = file.body
            tasks.append(asyncio.create_task(download_files(execute_unit, file_body, file_name)))
        await asyncio.gather(*tasks)

        result = {
            'status': 200,
            'msg': '檔案上傳成功'
        }

        return json(result, status=200, ensure_ascii=False)


# 依關鍵字取資料
class KeyWordInReport(HTTPMethodView):
    async def get(self, request):
        pdf_path = request.args.get('path')
        key_ls = request.args.getlist('key')

        # 查詢關鍵字在該PDF的第幾頁
        keyword_in_page = {key: [] for key in key_ls}
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for i in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[i]
                text = page.extract_text()
                for key in key_ls:
                    if key in text:
                        keyword_in_page[key].append(i+1)    # 頁碼是從第一頁開始，所以必須+1

        return json(keyword_in_page, status=200, ensure_ascii=False)
