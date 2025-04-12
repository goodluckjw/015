import os
import requests
import xml.etree.ElementTree as ET

def process_laws(search, replace):
    api_key = os.environ.get('API_KEY')
    if not api_key:
        return 'API 키가 설정되지 않았습니다.'
    url = f'https://www.law.go.kr/DRF/lawSearch.do?OC=laweditor&target=law&type=XML&query={search}'
    response = requests.get(url)
    if response.status_code != 200:
        return 'API 요청 실패'
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError:
        return 'XML 파싱 오류'
    result = []
    for law in root.findall('.//lawName'):
        result.append(law.text)
    return f'찾은 법령: {result}'