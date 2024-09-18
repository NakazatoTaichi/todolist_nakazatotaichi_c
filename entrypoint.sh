#!/bin/sh

# データベースが起動するまで待機
if [ "$DB_HOST" = "deploydb" ]
then
    echo "Waiting for MySQL..."

    while ! nc -z deploydb 3306; do
        sleep 0.1
    done

    echo "MySQL started"
fi

# マイグレーションの実行
python manage.py migrate

# Gunicornでアプリケーションを起動
exec "$@"
