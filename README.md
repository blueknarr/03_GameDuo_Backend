<div align="center">

# 3주차 - GameDuo

</div>



## 목차

- [개발 기간](#-개발-기간)

- [프로젝트 설명 및 분석](#-프로젝트)

- [API 사용법](#-API)

<br>  

## ⌛ 개발 기간

2022/07/11 ~ 2022/07/15

<br>

# 💻 프로젝트

### 프로젝트 설명 및 분석

- 보스레이드 PVE 콘텐츠를 위한 REST API 구현
  - 유저 생성, 조회, 보스레이드 상태 조회, 시작, 종료, 사용자 랭킹 조회
  - DRF를 통한 RESTful API 서버 개발
  - Redis SortedSet을 이용한 랭킹 시스템 구현 
  - Redis를 이용해 staticData 캐싱
  - 보스레이드 id: uuid 사용
  - EC2에 Docker-Compose로 Django + Nginx + gunicorn, MySql, Redis를 배포
  - 예외 처리
    - 한번에 한 명의 유저만 보스레이드 진행
    - 저장된 userId와 raidRecordid가 요청한 id와 일치하지 않다면 예외 처리

<br>

### 아키텍처 다이어그램

<img src="https://user-images.githubusercontent.com/44389424/182332127-4069008e-1624-40be-9803-e397a8e3deb2.JPG"/>





### Docker

<img src="https://user-images.githubusercontent.com/44389424/182345078-65a967c5-f5ff-4f43-a7e4-693bf44c474e.JPG"/>



### ERD

- tb_users: 회원 정보
- tb_raids_history: 보스레이드 상태 정보
- tb_total_score: 누적 랭킹 점수

<img src="https://user-images.githubusercontent.com/44389424/182331978-2fca1470-510f-4068-ac51-9d9cab3a9adb.JPG"/>





### API 명세서

| METHOD | URI                     | 기능                      |
| ------ | ----------------------- | ------------------------- |
| POST   | /users/                 | 회원가입                  |
| GET    | /users/<int: id>        | 유저 정보 조회            |
| GET    | /bossraid/              | 보스레이드 입장 가능 여부 |
| POST   | /bossraid/start         | 보스레이드 시작           |
| POST   | /bossraid/end           | 보스레이드 종료           |
| POST   | /bossraid/topRankerList | Top Ranking 조회          |



<br>



## API

API 사용법을 안내합니다.

### 회원가입

회원가입을 합니다. 이메일, 패스워드, 유저네임을 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를 받습니다.

#### Request

##### URL

```
POST /users/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter

| Name      | Type     | Description | Required |
| --------- | -------- | ----------- | -------- |
| email     | `String` | 이메일      | O        |
| user_name | `String` | 유저 네임   | O        |
| password  | `String` | 패스워드    | O        |

<br>

#### Response

| Name   | Type     | Description      |
| ------ | -------- | ---------------- |
| result | `String` | 등록 결과 메세지 |

<br>

### 유저 정보 조회

유저 정보를 조회합니다. userId로 `GET`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를 받습니다.

#### Request

##### URL

```
GET /users/<int:id> HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter: path

| Name | Type  | Description | Required |
| ---- | ----- | ----------- | -------- |
| id   | `int` | userId      | O        |

<br>

#### Response

| Name            | Type       | Description          |
| --------------- | ---------- | -------------------- |
| totalScore      | `Int`      | total score          |
| bossRaidHistory | `List`     | 보스레이드 정보      |
| raidRecordId    | `String`   | 보스레이드 uuid      |
| score           | `Int`      | 보스레이드 점수      |
| enterTime       | `Datetime` | 보스레이드 시작 시간 |
| endTime         | `Datetime` | 보스레이드 종료 시간 |

#### Result

##### <img src="https://user-images.githubusercontent.com/44389424/182332206-f171816b-c4e2-43ca-94a1-291792dba800.JPG"/>

<br>

### 보스 레이드 입장 가능 여부

보스 레이드 입장 가능 여부를 알려줍니다. refresh_token을 `GET`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를 받습니다.

#### Request

##### URL

```
GET /bossraid/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### <br>

#### Response

| Name          | Type     | Description                          |
| ------------- | -------- | ------------------------------------ |
| canEnter      | `String` | 입장 가능 여부                       |
| enteredUserId | `String` | 현재 보스레이드에 입장한 유저 아이디 |

#### Result

<img src="https://user-images.githubusercontent.com/44389424/182332264-516efd0d-5c8c-4136-a1cd-3ba77a103837.JPG"/>



### 보스 레이드 시작

보스 레이드 시작을 합니다. userId와 보스 레이드 level을을 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를 받습니다.

#### Request

##### URL

```
POST /bossraid/start/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter

| Name   | Type     | Description     | Required |
| ------ | -------- | --------------- | -------- |
| userId | `String` | 유저 아이디     | O        |
| level  | `String` | 보스레이드 레벨 | O        |

<br>

#### Response

| Name         | Type     | Description                |
| ------------ | -------- | -------------------------- |
| isEntered    | `String` | 현재 보스 레이드 입장 여부 |
| raidRecordId | `String` | 보스 레이드 아이디         |

#### Result

##### <img src="https://user-images.githubusercontent.com/44389424/182332312-277c9c4e-c7da-456c-8516-2cf6e6e7daf0.JPG"/>



### 보스 레이드 종료

보스 레이드 종료를 합니다. userId와 보스 레이드 아이디를 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를 받습니다.

#### Request

##### URL

```
POST /bossraid/end/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter

| Name         | Type     | Description        | Required |
| ------------ | -------- | ------------------ | -------- |
| userId       | `String` | 유저 아이디        | O        |
| raidRecordId | `String` | 보스 레이드 아이디 | O        |

<br>

#### Response

| Name   | Type     | Description      |
| ------ | -------- | ---------------- |
| result | `String` | 등록 결과 메세지 |

<br>

#### Result

##### <img src="https://user-images.githubusercontent.com/44389424/182332364-f4587939-b9c8-4a33-9a82-0f4a6db59a0b.JPG"/>






### Top Ranking 조회

보스 레이드 랭킹 목록을 조회합니다. userId를 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를 받습니다.

#### Request

##### URL

```
POST /bossraid/topRankerList/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter

| Name          | Type   | Description                                      | Required |
| ------------- | ------ | ------------------------------------------------ | -------- |
| userId | `String` | 유저 아이디 | O        |

<br>

#### Response

| Name              | Type   | Description         |
| ----------------- | ------ | ------------------- |
| topRankerInfoList | `List` | top ranking 목록    |
| myRankingInfo     | `Dict` | 현재 나의 랭킹 정보 |

#### Result

<img src="https://user-images.githubusercontent.com/44389424/182332401-cf3ed979-f46d-4ac7-a99f-d887c74a76b4.JPG"/>



## 기술 스택

> - Back-End : [![img](https://camo.githubusercontent.com/57ec2ff5dd5ad8c673b06805e02b305b5f13eba756771d734dc370536f12d41e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e20332e31302d3337373641423f7374796c653d666c6174266c6f676f3d507974686f6e266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/57ec2ff5dd5ad8c673b06805e02b305b5f13eba756771d734dc370536f12d41e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f507974686f6e20332e31302d3337373641423f7374796c653d666c6174266c6f676f3d507974686f6e266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/c408ece01574e98ceb3d78588c62385f17adae7d0fbb69a8707b03132894b478/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f20342e302e342d3039324532303f7374796c653d666c6174266c6f676f3d446a616e676f266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/c408ece01574e98ceb3d78588c62385f17adae7d0fbb69a8707b03132894b478/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f20342e302e342d3039324532303f7374796c653d666c6174266c6f676f3d446a616e676f266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/79be929c416fe51c5598caeb89f42f1456d6cf19a53dbf3153ab677c0fb9fedb/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d44524620332e31332e312d3030393238373f7374796c653d666c6174266c6f676f3d446a616e676f266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/79be929c416fe51c5598caeb89f42f1456d6cf19a53dbf3153ab677c0fb9fedb/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446a616e676f2d44524620332e31332e312d3030393238373f7374796c653d666c6174266c6f676f3d446a616e676f266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/0a168147042e3db1ec09d54b814f901ed20eff31e31c0f7df0525acc0a9b61f6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f636b65722032302e31302e31342d3234393645443f7374796c653d666c6174266c6f676f3d646f636b6572266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/0a168147042e3db1ec09d54b814f901ed20eff31e31c0f7df0525acc0a9b61f6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f636b65722032302e31302e31342d3234393645443f7374796c653d666c6174266c6f676f3d646f636b6572266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/ebd60befd49443c14417baff1700c7887f1a3c9c171612b2021a24c597e4b2ea/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f72656469732d2532334444303033312e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d7265646973266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/ebd60befd49443c14417baff1700c7887f1a3c9c171612b2021a24c597e4b2ea/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f72656469732d2532334444303033312e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d7265646973266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/edd471dded190e629043ad678016398ec885ebfefd103f9c64dadfd9b43e316d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4e67696e782d3030393633393f7374796c653d666c6174266c6f676f3d4e67696e78266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/edd471dded190e629043ad678016398ec885ebfefd103f9c64dadfd9b43e316d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4e67696e782d3030393633393f7374796c653d666c6174266c6f676f3d4e67696e78266c6f676f436f6c6f723d7768697465)
> - ETC　　　: [![img](https://camo.githubusercontent.com/8281207f240f045f9fb74d99fa7ffe64492bbd69501357e192e77978f3352920/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769742d4630353033323f7374796c653d666c61742d6261646765266c6f676f3d476974266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/8281207f240f045f9fb74d99fa7ffe64492bbd69501357e192e77978f3352920/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769742d4630353033323f7374796c653d666c61742d6261646765266c6f676f3d476974266c6f676f436f6c6f723d7768697465) [![img](https://camo.githubusercontent.com/c5282e23e8178a77185cc31077e2e1d45f95b8fec2081a2e31897f32c329cb7e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769746875622d3138313731373f7374796c653d666c61742d6261646765266c6f676f3d476974687562266c6f676f436f6c6f723d7768697465)](https://camo.githubusercontent.com/c5282e23e8178a77185cc31077e2e1d45f95b8fec2081a2e31897f32c329cb7e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769746875622d3138313731373f7374796c653d666c61742d6261646765266c6f676f3d476974687562266c6f676f436f6c6f723d7768697465) 
