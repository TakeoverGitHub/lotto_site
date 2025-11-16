# 1. Python 3.10-slim 이미지 사용
FROM python:3.10-slim

# 2. 환경 변수 설정 (버퍼링 없이 로그 출력)
ENV PYTHONUNBUFFERED 1

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. 프로젝트 코드 전체 복사
COPY . .

# (참고: Gunicorn을 쓴다면 여기에 CMD 추가)
# CMD ["gunicorn", "lotto_project.wsgi:application", "--bind", "0.0.0.0:8000"]