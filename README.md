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

## Set up the project

### If you have installed postgres locally:

- Start postgres

- Create `.env` from `.env.template`:

Run:

```
cp .env .env.template
```

Change `SQL_USER`, `SQL_PASSWORD` parameters in .env file according to your credentials in postgres

- Run migrate and createsuperuser

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

### For production (Postgres and Project in docker-compose):

- Create .env file
- Add the same values to `SQL_USER` and `POSTGRES_USER`
- Add the same values to `SQL_PASSWORD` and `POSTGRES_PASSWORD`
- Set `SQL_HOST` to `db`
- In `DJANGO_ALLOWED_HOSTS` use the production hostname
- In `CSRF_TRUSTED_ORIGINS` use the protocol+production hostname (eg: https://backend.donat-pool.io)
- Set `DEBUG` to 0 and generate new `SECRET_KEY`

- Run `docker-compose up -d --build`

- Create django admin:
`docker exec -ti donat-pool-backend sh`
`python3 manage.py createsuperuser`

- Set up nginx with the following config:

```
server {
    listen 80;
	listen [::]:80;
    index index.html index.htm index.nginx-debian.html;
    server_name backend.donat-pool.io;

    location / {
            proxy_pass http://0.0.0.0:8000/;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
    }
    
    location /static/{
	   autoindex on;
	   alias /shared/donat-pool/donat-pool-backend/static/;
    }
}
```

- Set up let's encrypt SSL:

`sudo certbot --nginx -d testnet.donat-pool.io`
