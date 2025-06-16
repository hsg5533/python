# 한국문화관광연구원_관광자원통계서비스
# 한국문화관광연구원_관광자원통계서비스 --> 활용신청
# 기간별 외국인방문객수와 내국인방문객수, 관광지의 주소 정보, 지역코드 정보를 제공하는 기능
# https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000366

import urllib.request
import datetime
import json
import math
#TODO1.
from openAPI.public_data.config import access_key

def get_request_url(url):
    # TODO2.
    req = urllib.request.Request(url)
    try: #TODO3
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 1]
def getTourPointVisitor(yyyymm, sido, gungu, nPagenum, nItems):
    
    end_point = "http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList"
    
    parameters = "?_type=json&serviceKey=" + access_key
    parameters += "&YM=" + yyyymm
    parameters += "&SIDO=" + urllib.parse.quote(sido)
    parameters += "&GUNGU=" + urllib.parse.quote(gungu)
    parameters += "&RES_NM=&pageNo=" + str(nPagenum)
    parameters += "&numOfRows=" + str(nItems)

    url = end_point + parameters
    print("** url ** : ", url)
    
    retData = get_request_url(url)
    
    #TODO5.
    if (retData == None):
        return None
    else:
        return json.loads(retData)

#[CODE 2]
def getTourPointData(item, yyyymm, jsonResult):
    # 응답데이터에서 각 키값을 꺼내어 변수에 할당
    # addrCd = item['addrCd']
    addrCd = 0 if 'addrCd' not in item.keys() else item['addrCd']
    gungu = '' if 'gungu' not in item.keys() else item['gungu']
    sido = '' if 'sido' not in item.keys() else item['sido']
    resNm = '' if 'resNm' not in item.keys() else item['resNm']
    rnum = 0 if 'rnum' not in item.keys() else item['rnum']
    ForNum = 0 if 'csForCnt' not in item.keys() else item['csForCnt']
    NatNum = 0 if 'csNatCnt' not in item.keys() else item['csNatCnt']
    
    # 응답 결과에서 꺼내온 값들을 json 형태로, jsonResult 리스트에 붙이기
    jsonResult.append({'yyyymm': yyyymm, 'addrCd': addrCd,
                    'gungu': gungu, 'sido': sido, 'resNm': resNm, 
                    'rnum': rnum, 'ForNum': ForNum, 'NatNum': NatNum})
    return    

def main():
    # 응답의 결과를 저장할 리스트 선언
    jsonResult = []

    sido = '서울특별시'
    gungu = ''
    nPagenum = 1
    nTotal = 0
    nItems = 100
    
    nStartYear = 2020
    nEndYear = 2024

    # 년도를 반복
    for year in range(nStartYear, nEndYear):
        #월을 반복
        for month in range(1, 13):
            #TODO4.
            # 연도와 월을 합쳐서 'YYYYMM'형태의 문자열을 생성
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            # 페이지 번호를 초기화
            nPagenum = 1

            #[CODE 3]
            while True:
                # 데이터 받아오기
                jsonData = getTourPointVisitor(yyyymm, sido, gungu, nPagenum, nItems)
                # 응답 데이터 추출
                if (jsonData['response']['header']['resultMsg'] == 'OK'):
                    nTotal = jsonData['response']['body']['totalCount']
            
                    if nTotal == 0:
                        break
                    
                    # 응답데이터에서 값을 추출하여 getTourPointData() 에 넘겨주기
                    for item in jsonData['response']['body']['items']['item']:
                        getTourPointData(item, yyyymm, jsonResult)
                    # 전체 페이지 수를 계산
                    # 전체 데이터 수를 가져와서 페이지당 아이템 수인 100으로 나누고
                    # 그 값을 올림한 결과를 nPage 변수에 할당
                    # nTotal은  jsonData에서 가져온 전체 데이터 수.
                    # nTotal은 해당 기간 동안의 관광지 데이터 총 개수를 의미
                    # 100은 한 페이지에 출력할 아이템 수
                    # nTotal을 페이지당 아이템 수로 나누어서 전체 페이지 수를 계산하고,
                    # 이 값을 올림하여 다음 페이지가 필요한 경우를 고려하여 nPage에 저장
                    nPage = math.ceil(nTotal / 100)
                    # 페이지번호가 마지막 페이지이면 반복문을 종료
                    if (nPagenum == nPage):
                        break
                    # 페이지 번호를 증가
                    nPagenum += 1
                
                else:
                    break
    
    # TODO5.
    with open("%s_관광지입장정보_%d_%d.json" % (sido, nStartYear, nEndYear-1), 'w', encoding='utf-8') as outfile:
        retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(retJson)
    print("%s_관광지입장정보_%d_%d.json SAVED" % (sido, nStartYear, nEndYear-1) )

if __name__ == '__main__':
    main() 