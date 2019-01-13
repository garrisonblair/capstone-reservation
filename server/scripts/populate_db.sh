python manage.py makemigrations
python manage.py migrate
python manage.py loaddata apps/accounts/fixtures/users.json
python manage.py loaddata apps/accounts/fixtures/tokens.json
python manage.py loaddata apps/accounts/fixtures/privilege_categories.json
python manage.py loaddata apps/rooms/fixtures/rooms.json
