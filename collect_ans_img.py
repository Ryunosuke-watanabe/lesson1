from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
import time
from var import List

driver = webdriver.Chrome("./driver/chromedriver")

feel = List.img_list

for item in feel:
    time.sleep(1)
    driver.get("https://www.google.co.jp/imghp?hl=ja&tab=wi&ogbl")
    driver.find_element_by_name("q").send_keys(item,Keys.ENTER)
    # 現在のページのurlを変数に入れる
    current_url = driver.current_url
    html = requests.get(current_url)
    bs = BeautifulSoup(html.text, "lxml")
    images = bs.find_all("img", limit=10+1)
    # imgフォルダの作成
    if not os.path.isdir("img/ans"):
        os.makedirs("img/ans")
    # 取得した画像をループして保存
    for i,img in enumerate(images, start=1):
        src = img.get("src")
        try:
            responce = requests.get(src)
            with open("img/ans/"+item + "{}.jpg".format(i-1), "wb") as f:
                f.write(responce.content)
        except requests.exceptions.MissingSchema:
            pass
    
driver.quit()