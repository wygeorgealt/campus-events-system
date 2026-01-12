DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_backend',
        'NAME': 'campus_db',
        'CLIENT': {
            'host': 'mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority',
        },
    }
}