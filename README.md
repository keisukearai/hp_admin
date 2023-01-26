# マイグレーションファイルの再作成
python manage.py makemigrations hp
# 設定クリア
python manage.py migrate --fake hp zero
# マイグレーション実施
python manage.py migrate

# データ投入
python manage.py loaddata master.json

# 管理ユーザ作成(管理画面)
python manage.py createsuperuser
OWUuP+2l7v30m1o