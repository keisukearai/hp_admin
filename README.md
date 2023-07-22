# マイグレーションファイルの再作成
python manage.py makemigrations hp
# 設定クリア
python manage.py migrate --fake hp zero
# マイグレーション実施
python manage.py migrate

# データ投入
python manage.py loaddata master.json

# 管理ユーザ作成(管理画面)
python manage.py createsuperuser<br>
OWUuP+2l7v30m1o

# テーブル再作成
## mysqlログイン
mysql -u hp_admin -p

## テーブル再作成
$ use hp_db
<br>
$ drop table company;
<br>
$ drop table newscategory;
<br>
$ drop table news;
<br>
$ drop table inquiry;
<br>
$ drop table sitelink;

## サーバ
rm -rf /var/www/html/hp_admin/hp/migrations/*.py

## Windows
del /S /Q D:\vscode\hp_admin\hp\migrations\*.py<br>
del /S /Q D:\vscode\hp_admin\hp\migrations\*.pyc