SSAFY Start Camp 챗봇 퀘스트
===========================
서울_7_배진호, https://github.com/Jinho-Bae


I. 스펙(Specification)  
----------------------------
 (1) 책 검색 기능  
  - 책의 정보(제목, 저자, 출판사, 가격, 책 소개, 저자 ) 출력
  
  - '책 이름' + "어때"  
 
 (2) 키워드 검색  
  - 키워드를 포함하는 책 이름 검색  
  
  - '키워드' + "검색"  
  
 (3) 베스트셀러, 스테디셀러, 신간 검색  
  - "베스트셀러", "스테디셀러", "신간"  
  
 (4) 책 추천  
  - 내가 읽은 책의 목록을 기반으로, 가장 많이 읽은 장르의 베스트셀러 추천
  
  - "추천"  
  
II. 대상 사용자(Users)
----------------------------
 어떤 책을 읽을지 고민하는 사람
 
III. 개발 환경(Development Environment)
----------------------------
| 환경 | 내용 | 버전 |
|:-----:| :-----: | :----: |
| 언어 | Python | 3.7 |
| IDE  | PyCharm | 2018.3.2 |
| 프레임워크  | Flask | 0.12.2 | 
|라이브러리| BeautifulSoup | 4 |
|플랫폼| Slack |  |

> ### requirements
- numpy
- click==6.7
- Flask==0.12.2
- itsdangerous==0.24
- Jinja2==2.9.6
- MarkupSafe==1.0
- pyaml==16.9.0
- PyYAML ==3.12
- requests-oauthlib==0.8.0
- requests==2.18.4
- six==1.10.0
- slackclient==1.0.2
- websocket-client==0.37.0
- Werkzeug==0.12.2
- beautifulsoup4==4.6.3
   
IV. 피드백(Feedback)
----------------------------
 - 독서 목록에 원하는 책을 추가하는 기능을 추가하고 싶었으나, 구현하지 못하였다.
 - 챗봇과 대화형으로 구현하고 싶다. (ex. 책 검색 후 > "이 책을 추가하시겠습니까?")
