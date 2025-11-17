# lotto_site
opensw-basic lotto_site

# Django & Docker 기반 로또 웹 사이트

본 프로젝트는 Django와 Docker를 이용하여 구현한 로또 구매 및 추첨 웹 사이트입니다. (프로젝트 제출용)

## 프로젝트 개요

사용자는 로또 구매(수동/자동) 및 당첨 확인이 가능하며, 관리자는 별도의 Admin 페이지에서 회차 생성, 로또 추첨, 당첨자 확인, 판매 실적 조회를 할 수 있습니다.

---

## 사용 기술 (Tech Stack)

* **Backend:** Python, Django
* **Database:** PostgreSQL
* **Infrastructure:** Docker, Docker Compose

---

## 실행 방법 (How to Run)

본 프로젝트는 Docker Compose를 통해 모든 환경이 자동 구성됩니다. 로컬에 Docker Desktop이 설치되어 있어야 합니다.

1.  **프로젝트 클론 (Clone)**
    ```bash
    git clone [https://github.com/TakeoverGitHub/lotto_site.git](https://github.com/TakeoverGitHub/lotto_site.git)
    cd lotto_site
    ```

2.  **Docker 컨테이너 빌드 및 실행**
    (최초 1회 `build`가 필요할 수 있습니다)
    ```bash
    docker-compose build
    docker-compose up -d
    ```

3.  **데이터베이스 마이그레이션 (DB 테이블 생성)**
    서버가 켜진 후, 새 터미널에서 아래 명령어를 실행해야 합니다.
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **관리자(Admin) 계정 생성**
    아래 명령어를 실행하고, 안내에 따라 ID와 비밀번호를 생성합니다.
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5.  **접속**
    * **관리자 페이지:** `http://localhost:8000/admin/`
    * **사용자 로그인:** `http://localhost:8000/accounts/login/`
    * **로또 메인:** `http://localhost:8000/lotto/` (로그인 후)

---

## 주요 기능

### 사용자 기능

* 회원 로그인 및 로그아웃
* 로또 구매 (자동 번호 생성)
* 로또 구매 (수동 번호 6개 입력)
* 내 당첨 결과 확인

### 관리자 기능 (`/admin` 페이지)

* **회차 관리:** 새로운 로또 회차(Round) 생성
* **판매 실적:** 회차별 판매된 티켓 수 실시간 확인
* **추첨 진행:** (Action) 선택한 회차의 당첨 번호를 자동으로 추첨
* **당첨자 확인:** (Action) 추첨 완료 후, 해당 회차의 모든 티켓 등수를 자동 계산하여 저장
