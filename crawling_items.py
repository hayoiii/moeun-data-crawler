# 실행 전 path와 driver만 경로 설정 해주면 됨! (맨 밑부분에 있음)
# 검색어 바꿔가면서 실행하면 됨

import time
import socket
import os
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException

CATEGORY_CODE_DICT = {
    'TOP': 'top',
    'SOX': 'socks',
    'DR': 'dress',
    'BTM': 'bottom',
    'SH': 'shoes'
    #TODO
}

def crawling(num_code):
    global category_code
    global crawled_count
    global storage_path

    # 제페토 아이템 preview url
    url = f"https://zepeto.me/contents/preview/{category_code}_{num_code}"
    driver.get(url)

    element = driver.find_elements_by_class_name('app_install')[0]

    try:
        img_element = element.find_elements_by_tag_name('img')[0]
    except IndexError:
        print("NOT FOUND CONTENTS")
        return

    try:
        # 실제 이미지가 존재하는 url
        img_url = img_element.get_attribute('src')
        driver.get(img_url)

        # 크롤링 타겟 이미지
        img = driver.find_element_by_xpath('/html/body/img').get_attribute('src')

        # 저장하기
        filename = str(crawled_count + 1) + '_' + category_code + '_' + num_code + '.png'
        urlretrieve(img, storage_path + '/' + filename)
        crawled_count = crawled_count + 1
        print(f"SUCCESS [{filename}]")

    # except ElementClickInterceptedException:
    #     print("ㅡ ElementClickInterceptedException ㅡ")
    #     driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
    #     print("ㅡ 100만큼 스크롤 다운 및 3초 슬립 ㅡ")
    #     time.sleep(3)
    #     click_and_retrieve(index, img, len(img_list))

    except NoSuchElementException:
        print("EXCEPTION: NoSuchElementException")


    except ConnectionResetError:
        print("EXCEPTION: ConnectionResetError")
        pass

    except URLError:
        print("EXCEPTION: URLError")
        pass

    except socket.timeout:
        print("EXCEPTION: socket.timeout")
        pass

    except socket.gaierror:
        print("EXCEPTION: socket.gaierror")
        pass

    except ElementNotInteractableException:
        print("EXCEPTION: ElementNotInteractableException")
        pass

    except HTTPError:
        print("EXCEPTION: HTTPError")
        pass


# clickAndRetrieve() 과정에서 urlretrieve 이 너무 오래 걸릴 경우를 대비해 타임 아웃 지정
socket.setdefaulttimeout(30)

# 이미지들이 저장될 경로 및 폴더 이름
storage_path = "/Users/hayeong/moeun/database/contents/"

# 드라이버 경로 지정 (크롬 이용) -> 컴퓨터에 chromedriver 설치해야 함 (구글에 치면 다운 가능)
driver = webdriver.Chrome('/Users/hayeong/dev/chromedriver')

# 크롤링한 이미지 수
crawled_count = 0
# 검색어 입력 받기
category_code = input("카테고리 코드 입력 >> ")
start_num_code = input("아이템 코드 시작점 >> ")
end_num_code = input("아이템 코드 종료점 >> ")

start = int(start_num_code)
end = int(end_num_code)
total = end - start

# 카테고리 코드 별로 폴더 분기
storage_path = storage_path + '/' + category_code

os.makedirs(storage_path, exist_ok=True)

for num in range(start, end):
    print(f"== 진행중 {num} / {total}")
    crawling(str(num))

print('----------크롤링 종료----------')
print(f"총 {crawled_count}개 저장")
print('----------------------------')
