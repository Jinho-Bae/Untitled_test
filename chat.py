# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

# slack_token = "xoxb-506945780401-506946983617-zEtjGzRF2bYd6GlgWqrZrAv7"
# slack_client_id = "506945780401.507444666083"
# slack_client_secret = "f1fbbbb4959e67d3db7e594f8f388e94"
# slack_verification = "itCvYlYFa0KX3ttykjMdjSTE"
# sc = SlackClient(slack_token)


# 크롤링 함수 구현하기
def _crawl_naver_keywords(text):
    # 여기에 함수를 구현해봅시다.
    if "베스트셀러" in text:
        url = "http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=06"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        keywords = ["> *베스트셀러*"]
        for book in soup.find_all("td", class_="goodsTxtInfo"):
            title = book.find("p").find("a")
            aupu = book.find("div", class_="aupu")
            atags = aupu.find_all("a")
            price = book.find("span", class_="priceB")

            if len(atags) == 2:
                keywords.append(title.get_text().strip() + " | " + atags[0].get_text().strip() + " | " + atags[
                    1].get_text().strip() + " | " + price.get_text().strip())
            elif len(atags) == 3:
                keywords.append(title.get_text().strip() + " | " +
                                atags[0].get_text().strip() + " 저, " + atags[1].get_text().strip() + "역 | " + atags[
                                    2].get_text().strip() + " | " + price.get_text().strip())

    if "스테디셀러" in text:
        url = 'http://www.yes24.com/24/category/bestseller?CategoryNumber=001&sumgb=03'
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
        keywords = ["> *스테디셀러*"]

        information = {}  # 제목:작가,출판사,출판년도

        for i in soup.find_all('td', class_="goodsTxtInfo"):

            # print(i.find('a').get_text().strip())
            price = i.find('span', class_="priceB").get_text()
            for j in i.find_all('div', class_="aupu"):
                artist, publisher, year = j.get_text().replace('\n', '').replace('  ', '').replace('\r', '').split('|')

                if '/' in artist:
                    # print(artist)
                    artist = artist.replace('/', ', ')
                information[i.find('a').get_text().strip()] = [artist, publisher.strip(), year, price]

        for name, info in information.items():
            keywords.append(name + " | " + info[0] + " | " + info[1] + " | " + info[3])

    if "신간" in text:
        url = "http://www.yes24.com/24/Category/NewProduct"
        req = urllib.request.Request(url)

        sourcecode = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(sourcecode, "html.parser")

        keywords = ["> *신간 예약 판매 BEST*"]
        title, author, publisher, price = [], [], [], []

        # for i in soup.find_all("div", class_="goods_info"):
        for data in soup.find_all("p", class_="goods_name"):
            title.append(data.get_text().strip())
            if len(title) >= 10:
                break
            # print(data.get_text().strip())
        for data_1 in soup.find_all("span", class_="goods_auth"):
            author.append(data_1.get_text().strip())
            if len(author) >= 10:
                break
            # print(data_1.get_text().strip())
        for data_2 in soup.find_all("span", class_="goods_pub"):
            publisher.append(data_2.get_text().strip())
            if len(publisher) >= 10:
                break
                # print(data_2.get_text().strip())
        for data_3 in soup.find_all("p", class_="goods_price"):
            price.append(data_3.get_text().strip())
            if len(price) >= 10:
                break
                # print(data_2.get_text().strip())
        for a in range(len(title)):
            keywords.append(title[a] + " | " + author[a] + " | " + publisher[a] + " | " + price[a])

    # else
    #    keywords = [ "베스트셀러, 스테디셀러, 신간 중 하나로 입력하세요" ]

    # 한글 지원을 위해 앞에 unicode u를 붙혀준다.
    return u'\n'.join(keywords)


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        keywords = _crawl_naver_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
