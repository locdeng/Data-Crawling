import requests
import urllib.parse
import json
import re
from datetime import datetime
import pandas as pd
import time

# API 키 설정
client_id = "UQexrdPCeNDLPucKp9bR"
client_secret = "_9J1vxz2_q"

# CSV에서 기업명 목록 불러오기
target_companies = pd.read_csv("enterprise_df_10k_utf8_data.csv", encoding="utf-8")
target_companies_name = target_companies["기업명"].unique() 
test_company = target_companies_name[7500:8000]

# 저장할 전체 결과 리스트
all_results = []

# 각 기업명마다 요청
for company_name in test_company:
    print(f"\nSearching news for: {company_name}")
    encoded_query = urllib.parse.quote(company_name)
    
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display=10&start=1&sort=sim"
    
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "User-Agent": "Mozilla/5.0",
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            print(f" - 총 검색 결과: {data['total']}개")

            for item in data["items"]:
                # HTML 태그 제거
                title = re.sub(r"<.*?>", "", item["title"])
                original_link = item.get("originallink",'')
                description = re.sub(r"<.*?>", "", item["description"])
                pub_date = item["pubDate"]
                link = item["link"]

                all_results.append({
                    "기업명": company_name, 
                    "title": title,
                    "orginallink": original_link,
                    "link": link,
                    "description": description,
                    "pubDate": pub_date
                })
        else:
            print(f" - Error {response.status_code}: {response.reason}")

    except Exception as e:
        print(f" - Exception: {e}")
        
    time.sleep(2)

# 모든 결과 DataFrame으로 저장
if all_results:
    df = pd.DataFrame(all_results)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"naver_news_all_companies_{current_time}.csv"
    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    print(f"\n 전체 뉴스 데이터를 파일로 저장했습니다: {file_name}")
else:
    print("\n 저장할 뉴스 데이터가 없습니다.")
