#!/bin/sh

# 데이터베이스 준비될 때까지 대기 (옵션)
./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "DB is ready!"

# 마이그레이션만 자동 실행
echo "Running migrate..."
python manage.py migrate --noinput

# 정적 파일 수집 필요 시 활성화 (현재는 vite서버에서 화면을 전담하므로 불필요)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Gunicorn 실행
echo "Starting Gunicorn..."
exec gunicorn myproject.wsgi:application -w 4 -b 0.0.0.0:8000
