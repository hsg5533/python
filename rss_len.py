import requests
import xml.etree.ElementTree as ET

# RSS 피드 URL (예제: 구글 뉴스 검색 RSS)
rss_url = "https://news.google.com/rss/search?q=인터오션&hl=ko&gl=KR&ceid=KR:ko"

# 데이터 요청 및 XML 파싱
response = requests.get(rss_url)
root = ET.fromstring(response.content)

# 'item' 태그 개수 조회
items = root.findall(".//item")
print(f"총 {len(items)}개의 뉴스 항목이 있습니다.")
