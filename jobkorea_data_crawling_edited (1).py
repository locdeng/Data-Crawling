import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import time


def get_value_by_key_index(soup, label_text):
    key_tags = soup.select("table.table-basic-infomation-primary > tbody > tr.field > th.field-label")
    value_cells = soup.select("table.table-basic-infomation-primary > tbody > tr.field > td.field-value")

    key_list = [th.get_text(strip=True) for th in key_tags]
    value_list = []
    
    # value_cells에서 값을 추출하는 부분
    # 각 value는 <td> 태그 내부의 div.value-container 안에 위치함
    # div.value-container는 다음 두 가지 구조를 가질 수 있음:
    #   - 단일 값: div.value-container > div.value
    #   - 복수 값 (nested list): div.value-container > div.values > div.value
    # 따라서 두 구조 모두 처리할 수 있도록 조건 분기 필요
    for td in value_cells:
        values_container = td.select("div.value-container > div.values > div.value")
        if values_container:
            value = [v.get_text(strip=True) for v in values_container]
            value_list.append(value)
        else:
            value = td.select_one("div.value-container > div.value")
            value_text = value.get_text(strip=True) if value else ""
            value_list.append(value_text)

    try:
        index = key_list.index(label_text)
        value = value_list[index]
        if isinstance(value, list):
            value = ", ".join(value) # 리스트를 쉼표로 구분된 문자열로 변환
        return str(value)
    except ValueError:
        # print(f"Label '{label_text}' not found in key_list")
        return ""
    except IndexError:
        # print(f"Value not found for index {index}")
        return ""


def get_jobkorea_data(corp_name_list, page_no=1):
    jobkorea_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    for corp_name in corp_name_list:
        url = f"https://www.jobkorea.co.kr/Search/?stext={corp_name}&tabType=corp&Page_No={page_no}"
        response = get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        flex_containers = soup.find_all(
            "div",
            class_="Flex_display_flex__i0l0hl2 Flex_direction_row__i0l0hl3 Flex_justify_space-between__i0l0hlf",
        )
        print(f"[{corp_name}] Found {len(flex_containers)} flex containers.")

        for container in flex_containers:
            inner_flex = container.find(
                "div",
                class_="Flex_display_flex__i0l0hl2 Flex_gap_space12__i0l0hls Flex_direction_row__i0l0hl3",
            )
            if not inner_flex:
                continue

            spans = inner_flex.find_all("span", class_="Typography_variant_size14__344nw27")
            if len(spans) >= 3:
                if len(spans) == 3:
                    corp_type = spans[0].get_text(strip=True) # 기업형태
                    corp_location = spans[1].get_text(strip=True) # 지역
                    corp_industry = spans[2].get_text(strip=True) # 업종
                else: 
                    corp_type = spans[1].get_text(strip=True) # 기업형태
                    corp_location = spans[2].get_text(strip=True) # 지역
                    corp_industry = spans[3].get_text(strip=True) # 업종
            else:
                print(f"[{corp_name}] Not enough span elements: {len(spans)} found.")
                continue

            capital = sales = ceo = foundation_date = ""
            parent = container.find_parent(
                "div",
                class_="Flex_display_flex__i0l0hl2 Flex_gap_space4__i0l0hly Flex_direction_column__i0l0hl4"
            )
            if parent:
                a_tag = parent.find("a", href=True)
                if a_tag:
                    detail_response = get(a_tag['href'], headers=headers)
                    print("link:", a_tag['href'])
                    if detail_response.status_code == 200:
                        detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                        capital = get_value_by_key_index(detail_soup, "자본금")
                        print("자본금: ", capital)
                        sales = get_value_by_key_index(detail_soup, "매출액")
                        print("매출액: ", sales)
                        ceo = get_value_by_key_index(detail_soup, "대표자")
                        print("대표자: ", ceo)
                        foundation_date = get_value_by_key_index(detail_soup, "설립일")
                        print("설립일: ", foundation_date)
                        
                        print(f"Extracted Data: {corp_name}, {corp_type}, {corp_location}, {corp_industry}")
                    else:
                        print(f"[{corp_name}] Failed to fetch detail page: {detail_response.status_code}")
            else:
                print(f"[{corp_name}] Parent container for detail link not found.")

            jobkorea_data.append({
                "기업명": corp_name,
                "기업유형": corp_type,
                "지역": corp_location,
                "업종": corp_industry,
                "자본금": capital,
                "매출액": sales,
                "대표자": ceo,
                "설립일": foundation_date,
                "기업 URL": a_tag['href'] if parent and a_tag else ""
            })

            time.sleep(3)

    return pd.DataFrame(jobkorea_data)


if __name__ == "__main__":
    corp_name_list = pd.read_csv("enterprise_df_10k_utf8_data.csv")["기업명"].unique().tolist()
    print(corp_name_list[7500:8000])
    # corp_name_list = ['삼성전자']
    # print("Crawling data for companies from index 7500 to 8000...")
    test_data = get_jobkorea_data(corp_name_list[7500:8000])

    test_data.to_csv("jobkorea_data_17.csv", index=False, encoding="utf-8-sig")
   