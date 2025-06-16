import urllib.request
import urllib.parse
import urllib.error

def send_get_request(url, data):
    try:
        data = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"{url}?{data}") as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)
    except Exception as e:
        print("General Error:", e)

def send_post_request(url, data):
    try:
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data, method='POST')
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)
    except Exception as e:
        print("General Error:", e)

def send_put_request(url, data):
    try:
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data, method='PUT')
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)
    except Exception as e:
        print("General Error:", e)

def send_delete_request(url, data):
    try:
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data, method='DELETE')
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
    except urllib.error.URLError as e:
        print("URL Error:", e.reason)
    except Exception as e:
        print("General Error:", e)


# 예제 API 엔드포인트
api_url = 'https://api.bgogooma.com/'


# POST 요청 보내기
post_data = {'username': 'wee45387@gmail.com', 'password': 'wee45387'}
print("\nPOST 요청 결과:")
print(send_post_request(api_url+'v1/users/signin/', post_data))


# PUT 요청 보내기
put_data = {'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1}
print("\nPUT 요청 결과:")
print(send_put_request(api_url, put_data))

# DELETE 요청 보내기
print("\nDELETE 요청 결과:")
print(send_delete_request(api_url, {}))

# 네이버 홈페이지 URL
naver_url = "https://www.naver.com"

# send_get_request 함수를 사용하여 네이버 홈페이지에 GET 요청을 보냅니다.
naver_page_content = send_get_request(naver_url, {})

