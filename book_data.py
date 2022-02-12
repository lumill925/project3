#교보문고 연간 베스트셀러에서 분야 종합을 카테고리의 페이지 수와 제목, 가격을 크롤링
#연간 데이터(2021.01.01~2021.12.31)
from numpy import genfromtxt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time

def save_csv(df):
    df.to_csv('(101-200).csv',mode ='w',encoding='utf-8')


# 책 제목, 작가, 줄거리, 가격, 평점 
# label : 장르
browser = webdriver.Chrome("D:\chromedriver.exe")
title_list = []
author_list = []
content_list = []
price_list = []
grade_list = []
genre_list = []
page_number = 101
category_address = '001001046011' 
run = True
while run:
    #처음 접속해서 받아오는 정보 -> 각 책 상세정보에 들어가기 위한 url, 가격 정보, pagination
    browser.get(f'http://www.yes24.com/24/category/display/{category_address}?fetchsize=40&pagenumber={str(page_number)}')
    time.sleep(3)
    #pagination
    page_list = browser.find_element_by_css_selector('#cateSubWrap > div.cateSubRgt > div:nth-child(4) > div.cCont_sortBot > span.cCont_sortLft > div')
    pages = page_list.find_elements_by_tag_name('a')
    last_page = 200
    print(last_page)
    
    
    book_list = browser.find_elements_by_css_selector('div > div.goods_info > div.goods_name > a:nth-child(2)')
    # price_items = browser.find_elements_by_css_selector('#category_layout > tbody > tr:nth-child(1) > td.goodsTxtInfo > p:nth-child(3) > span.priceB')
    # price_list = [price.get_attribute('innerHTML') for price in price_items]
    # print(price_list)
    #한 페이지 안에 있는 도서들 상세정보 가져오기
    for url in book_list:
        print(url.get_attribute('href'))
        response = requests.get(url.get_attribute('href'))
        soup = BeautifulSoup(response.text,'html.parser')
        
        #책의 상세정보(제목, 작가, 줄거리, 평점, 장르(label))
       
        #가격
        # try:
        #     price = soup.select_one('#total_order_scrollbar > span').get_text()
        #     #total_order_price_scrollbar
        #     price_list.append(price)
        # except AttributeError:
        #     price_list.append(None)
        #     pass
        if soup.select_one('#total_order_price_scrollbar') == None:
            continue
        else: price_list.append(soup.select_one('#total_order_price_scrollbar').get_text())

        #print(soup.select_one('#total_order_scrollbar > span').get_text())
       
        #제목        
        if soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2') == None:
            continue
        else: title_list.append(soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2').get_text())
        
        print(soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > div > h2').get_text())
       
        #작가
        if soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth') == None:
            continue
        else: author_list.append(soup.select_one('#yDetailTopWrap > div.topColRgt > div.gd_infoTop > span.gd_pubArea > span.gd_auth').get_text())
       
        #줄거리
        try:
            content = (soup.select_one('#infoset_introduce > .infoSetCont_wrap').get_text())
            content_list.append(content)
        except AttributeError:
            content_list.append(None)
            pass
        #print(soup.select_one('#infoset_introduce > .infoSetCont_wrap').get_text())

        #평점
        #1-추리/미스터리 2-공포/스릴러 3-판타지 4-무협 5-SF 6-역사 7-로맨스

        if soup.select_one('#spanGdRating > a > em') == None :
            continue
        else :
            grade_list.append(soup.select_one('#spanGdRating > a > em').get_text())   
        
        if soup.select_one('#infoset_goodsCate > div.infoSetCont_wrap > dl > dd > ul > li > a:nth-child(8)') == None :
            continue
        else :
            genre_list.append(soup.select_one('#infoset_goodsCate > div.infoSetCont_wrap > dl > dd > ul > li > a:nth-child(8)').get_text())

        #print(soup.select_one('#infoset_goodsCate > div.infoSetCont_wrap > dl > dd > ul > li:nth-child(1) > a:nth-child(8)').get_text())
    
    #마지막페이지 확인
    if int(last_page) == page_number : 
        run = False
    else :
        page_number += 1

    print(len(title_list),len(author_list),len(content_list),len(price_list),len(grade_list),len(genre_list))

#book_df = pd.DataFrame({'title':title_list,'author':author_list,'content':content_list,'price':price_list,'grade':grade_list,'genre':genre_list})
book_dict = {'title':title_list,
             'author':author_list,
             'content':content_list,
             'price':price_list,
             'grade':grade_list,
             'genre':genre_list
             }

book_df = pd.DataFrame.from_dict(book_dict, orient='index')
book_df = book_df.transpose()
browser.close()
print(book_df)
save_csv(book_df)

