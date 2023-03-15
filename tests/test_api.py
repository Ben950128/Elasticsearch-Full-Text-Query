import requests
import os

class TestAPIFunctions:
    def test_post_report(self, api_prefix):
        url = api_prefix + 'report'
        filepath = './asset/退後.pdf'
        files=[('files',('退後.pdf',open(filepath, 'rb')))]
        form_data = {
            'category':'周杰倫'
        }
        response = requests.post(url, data=form_data, files=files)
        data = response.json()
        assert response.status_code == 200
        assert data == {
            'status': 200,
            'msg': '檔案上傳成功'
        }
        assert os.path.exists('../src/upload_files/周杰倫/退後.pdf')

        
    def test_get_report(self, api_prefix):
        url = api_prefix + 'report?key=愛情'
        response = requests.get(url)
        data = response.json()
        assert response.status_code == 200
        assert isinstance(data, list)
        assert data == [
            {
                "檔案名稱": "退後.pdf",
                "檔案位置": "./upload_files/周杰倫/退後.pdf"
            }
        ]


    def test_get_page_nunber(self, api_prefix):
        url = api_prefix + 'page_number?key=愛情&key=天空&path=./upload_files/周杰倫/退後.pdf'
        response = requests.get(url)
        data = response.json()
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert data == {
            '愛情': [1, 2],
            '天空': [1]
        }