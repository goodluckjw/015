import requests
import xml.etree.ElementTree as ET
import time
import os

API_KEY = os.environ.get("LAW_API_KEY", "your_api_key_here")
OC = "chetera"  # 사용자의 OC 값 (이메일 앞부분)

def get_law_list():
    url = f"http://open.law.go.kr/LSO/openApi/lawSearch.do?OC={OC}&type=XML&key={API_KEY}&page=1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            laws = []
            for law in root.findall('.//law'):
                law_id = law.find('lawId').text
                law_name = law.find('lawNm').text
                laws.append({"id": law_id, "name": law_name})
            return laws
        else:
            print(f"API 요청 실패: {response.status_code}")
            return None
    except Exception as e:
        print(f"법률 목록 가져오기 오류: {str(e)}")
        return None

def search_law_content(law_id, search_word):
    url = f"http://open.law.go.kr/LSO/openApi/lawContent.do?OC={OC}&type=XML&key={API_KEY}&lawId={law_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            matches = []
            for article in root.findall('.//article'):
                article_num = article.find('articleNo').text if article.find('articleNo') is not None else ""
                content = article.find('content').text if article.find('content') is not None else ""
                if search_word in content:
                    matches.append({
                        "type": "article",
                        "number": article_num,
                        "content": content
                    })
            return matches
        else:
            print(f"법률 내용 API 요청 실패: {response.status_code}")
            return None
    except Exception as e:
        print(f"법률 내용 검색 오류: {str(e)}")
        return None

def generate_amendment_sentence(law_name, article_info, search_word, replace_word):
    article_num = article_info["number"]
    amendment = f"{law_name} 제{article_num}조 중 \"{search_word}\"를 \"{replace_word}\"로 한다."
    return amendment

def process_laws(search_word, replace_word):
    result = {}
    laws = get_law_list()
    if laws is None:
        return None
    for law in laws:
        law_id = law["id"]
        law_name = law["name"]
        time.sleep(0.5)
        matches = search_law_content(law_id, search_word)
        if matches is None:
            continue
        if matches:
            result[law_name] = []
            for match in matches:
                amendment = generate_amendment_sentence(law_name, match, search_word, replace_word)
                result[law_name].append(amendment)
    return result
