# NEEL: clothing brand store (Django + SQL)

## Run locally
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations shop
python manage.py migrate
python manage.py seed              # sample products
python manage.py createsuperuser   # for /admin/
python manage.py runserver
```
Open http://127.0.0.1:8000 (store) and http://127.0.0.1:8000/admin/ (products, stock, orders).

## Use PostgreSQL or MySQL
Install the driver in requirements.txt, then set `DB_ENGINE=postgres` (or `mysql`) with `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

## Go live
Set `DJANGO_DEBUG=0`, a long random `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS=yourdomain.com`, run `python manage.py collectstatic`, and serve with gunicorn behind nginx (or add WhiteNoise).

## Make it yours
Rename the brand in `shop/templates/shop/base.html`, edit colours at the top of `shop/static/css/style.css`, and add product photos by pasting an image URL in the product's admin page.
