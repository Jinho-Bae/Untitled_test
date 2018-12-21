import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template
import csv
import operator
import collections
from collections import Counter

# elice_utils = EliceUtils()


def main():
    # URL 데이터를 가져올 사이트 url 입력
    url = "http://www.yes24.com/24/goods/66997133"
    # csv_save(url)
    genre_recommendation()
    # URL 주소에 있는 HTML 코드를 soup에 저장합니다.


def csv_save(url):

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
    keywords = []
    book = []

    for data in soup.find_all("div", class_="basicListType communtyHide"):
        # print(data.get_text())
        data = data.get_text()
        data = data.split('>')
        for i in data:
            keywords.append(i.strip())
    book.append(keywords[1])
    # 제목
    for data in soup.find_all("h2", class_="gd_name"):
        book.append(data.get_text())
    # 저자
    for data in soup.find_all("span", class_="gd_auth"):
        book.append(data.get_text().strip())
    # 출판사
    for data in soup.find_all("span", class_="gd_pub"):
        book.append(data.get_text().strip())
    # print(book)

    f = open('output.txt', 'w')
    for i in book:
        data = "%s," % i
        f.write(data)
        # print(data)
    f.write('\n')
    for i in book:
        data = "%s," % i
        f.write(data)
        # print(data)
    f.write('\n')
    f.close()
    # print(book)

    # csv 쓰기
    # f = open('output.csv', 'w', encoding='utf-8', newline='')
    # wr = csv.writer(f)
    # wr.writerow(book)
    # f.close()


    # 장르 추천
def genre_recommendation():
    genre = []

    f = open('output.txt', 'r', encoding='UTF8')
    rdr = f.readlines()
    for line in rdr:
        a = line.split(',')
        genre.append(a[0])
        print(line)
    # print(rdr)
    f.close()
    # print(genre)

    # f = open('output.csv', 'r', encoding='utf-8')
    # rdr = csv.reader(f)
    # for line in rdr:
    #     genre.append(line[0])
    #     # print(line)
    # f.close()


    # genre dict
    Counter(genre)  # dict로 담는다 / sort는 안됨
    # print(Counter(genre))
    # od = collections.OrderedDict(sorted(Counter(genre).items()))
    # for k, v in od.items():
    #     print (k, v)
    sort = sorted(Counter(genre).items(), key=operator.itemgetter(1), reverse=True)  # sorted해서 tuple에 담자
    print(sort)
    a = list(sort)
    print(a[0][0])

    # print(b[0])     # 추천 장르(제일 많이 읽은 장르)
    return a[0][0]


1



if __name__ == "__main__":
    main()