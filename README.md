# Melon Chart Crawler

멜론 차트 TOP100을 크롤링하는 프로그램입니다.

## 기능
- 멜론 차트 TOP100의 순위, 제목, 가수, 날짜 정보를 크롤링
- 결과를 CSV 파일로 저장

## 설치 방법
1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법
1. 프로그램 실행:
```bash
python melon_crawler.py
```

2. 실행 결과:
- 현재 날짜로 된 CSV 파일이 생성됩니다 (예: melon_top100_2024-04-07.csv)
- CSV 파일에는 순위, 제목, 가수, 날짜 정보가 포함됩니다.

## 주의사항
- 웹 크롤링 시 해당 웹사이트의 이용약관을 준수해주세요.
- 과도한 요청은 피해주세요. 