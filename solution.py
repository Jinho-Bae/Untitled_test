from elice_utils import EliceUtils
import urllib.request
from bs4 import BeautifulSoup

elice_utils = EliceUtils()


def main():
    print("네이버 인기검색어")

    url = "http://www.naver.com"
    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    list = []

    for naver_text in soup.find_all("span", class_="ah_k"):
        list.append(naver_text.get_text())

    print(list)


if __name__ == "__main__":
    main()
