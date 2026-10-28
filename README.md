# BGNEWS

국내 보드게임 업체 소식, 텀블벅 보드게임 펀딩, 해외 화제 펀딩 게임을 매일 모아 보는 정적 웹사이트입니다.

- 사이트: https://novandgigs.github.io/bgnews/
- 데이터: `data/news.json` (소식 배열), `data/meta.json` (마지막 수집 정보)
- 매일 오전 11시(KST) 예약 작업이 새 소식을 `scripts/add_news.py`로 합치고 커밋합니다.

## 소식 항목 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| id | ○ | `YYYY-MM-DD-슬러그` (영문·숫자·하이픈) |
| date | ○ | 원문 게시일 또는 펀딩 시작일 |
| collectedOn | ○ | 수집한 날 |
| company | ○ | 업체·창작자·퍼블리셔 |
| category | ○ | 신작 출시 / 선주문·펀딩 / 재입고 / 할인·이벤트 / 행사 / 기타 |
| title, summary | ○ | 제목, 1~2문장 요약 |
| section |  | domestic(국내 소식) / tumblbug / global(해외 펀딩). 없으면 platform 등으로 추정 |
| url, source, imageUrl, eventDate |  | 원문 링크, 출처명, 대표 이미지, 일정 |
| platform, fundingEnd, fundingRate, fundingAmount, backers |  | 펀딩 정보 |
| pledgePrice, shipsToKorea, delivery, koreanEdition |  | 직구 판단 정보, 한국어판 여부 |
