# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tablica_db',
        'HOST': 'localhost',

        'USER': 'tomaszizdebski',
        'PORT': 5432
    }
}