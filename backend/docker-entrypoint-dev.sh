#!/bin/sh

python manage.py makemigrations
python manage.py migrate

./wait-for-it.sh db:5432 -- python manage.py runserver 0.0.0.0:8000

# # 왜 make-migrations와 migrate를 구분하는 것인가?
# # 1. makemigrations: 모델 변경사항을 감지하여 마이그레이션 파일 생성
# # 2. migrate: 생성된 마이그레이션 파일을 실제 DB에 적용
# # 파일 생성 후 바로 migrate를 자동화 하지 않는 이유는?
# # 1. 개발자가 수동으로 확인 후 적용할 수 있도록 하기 위함
# # 2. DB에 적용하기 전에 마이그레이션 파일을 검토할 수 있는 기회를 제공
# # 3. 마이그레이션 파일이 잘못 생성되었을 경우, DB에 적용하기 전에 수정할 수 있도록 하기 위함
# # 개발용 엔트리포인트: db 대기 없이 바로 실행


# #!/bin/shb
# # 개발용 엔트리포인트: db 대기 없이 바로 실행

# # 개발자가 원하면 수동으로 실행할 수 있게 로그만 출력
# echo "🚀 개발 서버 시작. DB 마이그레이션은 수동 실행하세요."
# echo "👉 예: docker-compose exec backend python manage.py migrate"

# # Django 개발서버 실행
# python manage.py runserver 0.0.0.0:8000