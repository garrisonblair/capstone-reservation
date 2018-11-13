python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata apps/accounts/fixtures/users.json
python3 manage.py loaddata apps/accounts/fixtures/accounts.json
python3 manage.py loaddata apps/accounts/fixtures/privilege_categories.json
python3 manage.py loaddata apps/rooms/fixtures/rooms.json
