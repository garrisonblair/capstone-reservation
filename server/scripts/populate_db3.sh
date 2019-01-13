python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata apps/accounts/fixtures/users.json
python manage.py loaddata apps/accounts/fixtures/tokens.json
python3 manage.py loaddata apps/accounts/fixtures/privilege_categories.json
python3 manage.py loaddata apps/rooms/fixtures/rooms.json
