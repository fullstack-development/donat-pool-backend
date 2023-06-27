# donat-pool-backend

- Create virtual env:

```
python3 -m venv env
source env/bin/activate 
```

- Install dependencies:

```
sudo apt install python3-dev libpq-dev

pip install -r requirements.txt
```

- Start postgres:

Export `POSTGRES_USER` and `POSTGRES_PASSWORD` for DB connection.

```
docker-compose up -d`
```

- Create local settings:

Run:

```
cp settings.py local_settings.py
```

And change DATABASE parameters in `local_settings.py` using credentials from the previous step

- Migrate

```
python manage.py migrate
```
