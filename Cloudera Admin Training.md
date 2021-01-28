# Cloudera Administrator Training

## Introduction
* 많은 eco system들을 통합적으로 관리, 운영
* 분석 단계
    * data 가져오기
    * 저장 (landing)
    * 가공 (마트를 만들거나 summary를 만듦)
    * 분석


## Data ingest
* Apache Sqoop : RDBMS의 정보를 가져옴
* Apache Flume(없어짐) : log files
* Apache Kafka/Spark Streaming : IoT data (실시간)
* 체크할 점 : 정형/비정형, 실시간/batch
    * 정형 : sqoop (99%)
    * 실시간 : Kafka, Spark Streaming, Nifi

## Cloudera Manager
* what is CM?
Hadoop eco system들을 관리, 모니터링
* 설정 변경
* 서비스/호스트 리스타트
* 모니터링

## The Role of a Hadoop Administrator
### Planning
* 다른 부서와 친밀히 일하기
* cluster size와 용량을 계획
* 스케줄링 계획 세우기

## Cloudera Manager Service
### Service roles
* Host Monitor (서버 상태)
* Service Monitor (서비스란 eco system들)
* Event Server
* Activity Monitor
* Alert Publisher
* Reports Manager
* Navigator Audit Service (다른 것과 합쳐짐)
* Navigator Metadata Server (다른 것과 합쳐짐)
### Utility Node
* Cloudera Manager가 설치되어 있는 cluster
### Master Node
* HDFS NameNode
* Secondary Namenode : 복제만 할 뿐 HA를 위한 것은 아님
* YARN ResourceManager
### Worker Node
* HDFS DataNode
* YARN NodeManager
* Impala daemons
### Gateway Node
* application 실행 환경을 제공
* (aka.)edge node

## Configuring a Cloudera Cluster
### Terminology
* service : a set of related components
    * e.g. Spark, Hive, Impala
* role : an individual componenet of a service
    * e.g. namenode
* role Instance : a daemon
* role group : 여러 hosts들에 배포된 role들의 group (같은 설정)
    * 주로 새로운 node를 추가했을 때

## Hive & Impala
### what is Hive
* Uses a SQL-like language called HiveQL
* MapReduce 혹은 Spark jobs에 의해 실행되는 쿼리 충족
* table을 RDBMS와 같이 저장함
### internal & external
* internal : 테이블 지우면 스키마와 데이터가 지워짐
* external : 테이블 지우면 스키마만 지워짐
### Hive is Not an RDBMS
* 데이터를 UPDATE, DELETE 할 수 없음
### What is Impala
* distributed query engine
* data can be in HDFS, Kudu, Amazon S3, MS ADLS
* Impala is best for interactive, ad hoc queries
* Hive is better for large, long-running batch processes
* Hive와 metastore를 공유함 (hive에서 create table을 Impala에서 조회 가능)
### Metadata Caching
* RESRESH tablename (변경 분만)
* Invalidate meta (모든 metadata )
### Recommendations
* format : Parquet, Avaro
* Compression : Snappy
* numeric types instead of strings when possible
* ETL 작업이 끝나면 'COMPUTE STATS'

## YARN & MapReduce
* Hive는 YARN 위에서
* Impala는 YARN X
### YARN Benefits
* 다양한 workloads
* memory and CPU shared dynamically
* 예상 가능한 성능
### roles
* ResourceManager
    * master host에서 동작
    * 전체 자원 관리
* NodeManager
    * worker hosts에서 동작
    * HDFS datanode와 같이 위치
### Cluster Resource Allocation
1. ResourceManager가 한 container에게 ApplicationMaster 할당
2. ApplicationMaster가 ResourceManager로부터 추가적인 containers 요청
3. ResourceManager가 containers 할당
4. ApplicationMaster가 task를 container JVM에 분배
5. NodeManager가 container JVM을 실행시키고 자원 소모 모니터링
### MapReduce
* Key-value 쌍을 record라 함
* Map
    * mapper는 Map 작업 수행 객체
    * 일반적으로 텍스트파일에서 개행문자(줄바꿈)을 기준으로 한 줄씩 읽어들여 입력 데이터를 원하는 Key-Value 형태로 만드는 작업
    * Key-Value 형태로 값을 뽑아냈다면 결과 객체에 Key-Value를 insert
* Reduce
    * 정렬을 통해 리듀서 내부에서 같은 키를 가지는 레코드들을 한군데에 모았다면, 리듀스 함수에서 그 한군데에 모아진 레코드들을 순서대로 처리


## YARN과 Impala의 자원 분배
* Utilization report에서 YARN과 Impala 탭을 보고 판단
* resourceManager web UI : 방화벽 해제 필요

## ?
* CDH : Cloudera's Distribution for Hadoop
* cluster : 여러 대의 컴퓨터 및 서버를 묶어 고성능, 고가용성
    * node와 같은가? node들의 묶음인가? node는 host인가?
* 분석이란?
* on-premise : 원격 클라우드가 아닌 자체 전산실에서 서비스
* vendor lock in X > flexible
* HDFS
    * Native OS filesystem 위에 있는 java application
    * archiving 용으로 많이 쓺 (오래된 데이터)
    * 각 data block은 3 replication
        * 복제본이 많으면 locality가 높아지므로 조회 속도가 빨라짐
    * 작은 파일들에 대한 이슈가 고질적
        * 1 x 1GB
            * Name : 1
            * Blocks : 8
            * total items in memory : 9
        * 1000 x 1MB
            * Name : 1000
            * Blocks : 1000
            * total items in mem : 2000
    * 큰 데이터 파일을 처리하기 빠르다(각 파일은 >128MB)
    * immutable (append만 되고, update 안됨)
* NameNode
    * master 역할로써 datanode에 데이터를 분산시키고 관리하는 기능 담당
    * I/O task 지휘, datanode의 이상유무를 체크
* DataNode
    * DataNode daemon을 통해 분산 파일의 read/write 작업 수행
    * 작업 내역을 수시로 NameNode에 보고하고, 그 내역은 NameNode에 메타데이터 형식으로 저장
* HBase : NoSql (Kudu에 밀려 잘 안씀)
* Kudu
    * Cloudera에서 개발한 칼럼 기반 스토리지(columnar storage)
    * 순차 읽기와 랜덤 액세스를 모두 잘하는 플랫폼
    * Parquet는 순차 읽기에 강하나 랜덤 액세스에는 약하다.
    * HBase는 랜덤 액세스에는 강하나 순차 읽기에는 약하다.
* Object Store : AWS
* MapReduce
    * 구글에서 대용량 데이터 처리를 분산 병렬 컴퓨팅에서 처리하기 위한 목적으로 제작
    *  이 프레임워크는 함수형 프로그래밍에서 일반적으로 사용되는 Map과 Reduce라는 함수 기반
*  Spark
    *  버클리 대학의 AMPLab에서 개발되어 현재는 아파치 재단의 오픈소스로 관리되고 있는 인메모리 기반의 대용량 데이터 고속 처리 엔진으로 범용 분산 클러스터 컴퓨팅 프레임워크
*  Hive
    *  data warehousing solution
    *  RDB의 데이터베이스, 테이블과 같은 형태로 HDFS에 저장된 데이터의 구조를 정의하는 방법을 제공하며, 이 데이터를 대상으로 SQL과 유사한 HiveQL 쿼리를 이용하여 데이터를 조회하는 방법을 제공
    *  MapReduce 위에 랩핑
    *  batch
*  Impala
    *  HDFS에 저장돼 있는 데이터를 SQL을 이용해 실시간으로 분석할 수 있는 시스템
    *  MapReduce 프레임워크를 이용하지 않고 분산 질의 엔진을 이용해 분석하기 때문에 빠른 결과를 제공
    *  interactive(대화형)
*  YARN(Yet Another Resource Negotiator)
    *  분산 컴퓨팅 환경을 제공
    *  나오게 된 배경 : 여러 개의 컴퓨팅 플랫폼을 동시에 실행할 경우 각 서버의 리소스(주로 메모리)가 부족하여 정상적으로 수행되던 작업들이 다른 작업에 의해 문제가 발생하게 된다.
*  Kerberos
*  HUE (Hadoop User Experience)
    *  plugin 방식으로 hive, impala를 선택해서 실행 가능
    *  HttpFS REST API로 file system UI
*  Ansible
    *  설정 관리 툴 (OS 관리)
    *  SSH사용하여 agent 불필요(Puppet, Chef는 agent를 사용)
    *  멱등성(여러 번 적용해도 결과가 같음)
*  Parcel : service들의 묶음
    *  eco system 및 dependency들의 호환성 테스트를 통과한 세트
*  Parquet 압축 : Snappy