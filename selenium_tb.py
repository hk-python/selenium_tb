from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from selenium.webdriver.common.action_chains import ActionChains
from pyquery import PyQuery as pq
from lxml import etree
from bs4 import BeautifulSoup
import time
import pymongo


chrome_option=webdriver.ChromeOptions()
chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
profile_directory = r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'  #添加浏览器本地配置文件
chrome_option.add_argument(profile_directory)
chrome_option.add_argument('disable-infobars')
browser=webdriver.Chrome(options=chrome_option)
browser.maximize_window()
wait=WebDriverWait(browser,10)
KEYWORD='小米'
url='https://www.taobao.com/'

def soso():
    browser.get(url)
    sou=wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#q')
        ))
    sousub=wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')
        ))
    sou.send_keys(KEYWORD)
    sousub.click()
    time.sleep(2)

    print("正在爬取第1页！！！")
    xinxi()
    main()
def xinxi():
    try:
        time.sleep(2)
        html = browser.page_source
        soup=BeautifulSoup(html,'lxml')
        i=0
        for item in soup.select('#mainsrp-itemlist > div > div > div > div'):
            if item.select('img.J_ItemPic')[0].attrs['src'] == "":
                img=item.select('img.J_ItemPic')[0].attrs['data-src']
            else:
                img =item.select('img.J_ItemPic')[0].attrs['src']
            price=item.select('div.price.g_price.g_price-highlight > strong')[0].text
            deal=item.select('div.deal-cnt')[0].text
            title=item.select('a.J_ClickStat')[1].text
            try:
                shop=item.select('a.shopname > span')[1].text
            except Exception:
                shop="null"
            product={
                "img":img,
                "price":price,
                "deal":deal,
                "title":title,
                "shop":shop,
            }
            print(product)
            save_mongo(product)
            i += 1
            print(i)
            print('****************************************************************************************************************************')
    except Exception:
        xinxi()

def main():
    for page in range(2,101):
        next_page(page)
def next_page(page):
    print("正在爬取第", page, "页！！！")

    try:
        if page > 1:
            next = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(3)')
            ))
            next.click()
            # sub.click()
            # try:
            #     browser.switch_to.frame('ks-component985')
            #     yanzheng = wait.until(EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, '#nc_1_n1z')
            #     ))
            #     if yanzheng:
            #         # browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            #         ActionChains(browser).drag_and_drop_by_offset(yanzheng, 400, 0).perform()
            #         sub.click()
            # except:
            #     pass
        time.sleep(5)
        xinxi()
    except TimeoutException:
        next_page(page)

def save_mongo(result):
    MONGO_URL='localhost'
    MONGO_DB='tb'
    MONGO_COLLECTION='product'
    client=pymongo.MongoClient(MONGO_URL)
    db=client[MONGO_DB]
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到Mongodb成功！')
    except Exception:
        print('存储到Mongodb失败!')


if __name__=="__main__":
    soso()

