import io
import zipfile
from xml.sax.saxutils import escape

from fastapi.testclient import TestClient
from app.main import create_app
from app.sources import chapters_from_text, extract_text

def make_docx(text):
    w = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    xml = '<w:document xmlns:w="'+w+'"><w:body><w:p><w:r><w:t>'+escape(text)+'</w:t></w:r></w:p></w:body></w:document>'
    f = io.BytesIO()
    with zipfile.ZipFile(f, 'w') as z:
        z.writestr('word/document.xml', xml)
    return f.getvalue()

def test_extract_txt_docx_and_chapter_detection():
    assert extract_text('Chương 1\nXin chào'.encode(), '.txt') == 'Chương 1\nXin chào'
    assert extract_text(make_docx('Đoạn truyện'), '.docx') == 'Đoạn truyện'
    parts = chapters_from_text('Lời tựa\nChương 1: Khởi đầu\nA\nChương 2\nB')
    assert [c['heading'] for c in parts] == ['Lời mở đầu', 'Chương 1: Khởi đầu', 'Chương 2']

def test_local_source_upload_scoped_and_rights(tmp_path):
    client = TestClient(create_app(tmp_path / 'studio.db'))
    p1 = client.post('/api/projects', json={'title': 'A', 'rights_status': 'owned'}).json()['id']
    p2 = client.post('/api/projects', json={'title': 'B', 'rights_status': 'owned'}).json()['id']
    unknown = client.post('/api/projects', json={'title': 'C'}).json()['id']
    payload = {'file': ('story.txt', 'Chương 1\nA\nChương 2\nB'.encode('utf-8'), 'text/plain')}
    assert client.post(f'/api/projects/{p1}/sources', files=payload, data={'confirm_rights': 'false'}).status_code == 422
    assert client.post(f'/api/projects/{unknown}/sources', files=payload, data={'confirm_rights': 'true'}).status_code == 409
    result = client.post(f'/api/projects/{p1}/sources', files=payload, data={'confirm_rights': 'true'})
    assert result.status_code == 201, result.text
    item = result.json()
    assert item['segment_count'] == 2
    assert client.post(f'/api/projects/{p1}/sources', files=payload, data={'confirm_rights': 'true'}).status_code == 409
    assert len(client.get(f'/api/projects/{p1}/sources').json()) == 1
    assert client.get(f'/api/projects/{p2}/sources').json() == []
    assert client.get(f'/api/projects/{p2}/sources/{item["id"]}').status_code == 404
    part = client.get(f'/api/projects/{p1}/sources/{item["id"]}/segments/2')
    assert part.status_code == 200 and 'Chương 2' in part.json()['content']
    assert client.get(f'/api/projects/{p1}/sources/{item["id"]}/segments/3').status_code == 404

def test_bad_file_and_unrecognized_text(tmp_path):
    client = TestClient(create_app(tmp_path / 'studio.db'))
    pid = client.post('/api/projects', json={'title':'test','rights_status':'owned'}).json()['id']
    base = f'/api/projects/{pid}/sources'
    assert client.post(base,files={'file':('evil.exe',b'whatever')},data={'confirm_rights':'true'}).status_code == 415
    assert client.post(base,files={'file':('bad.docx',b'not zip')},data={'confirm_rights':'true'}).status_code == 422
    assert client.post(base,files={'file':('blank.txt',b' \n ')},data={'confirm_rights':'true'}).status_code == 422
