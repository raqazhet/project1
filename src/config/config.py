import os

MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_DB = f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:27017'

# Token details 
JWT_KEY = os.environ.get('JWT_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRES_HOURS = int(os.environ.get('REFRESH_TOKEN_EXPIRES_HOURS'))


##Redis conf
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_DB = int(os.environ.get('REDIS_DB'))
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT'))

##AWS conf 
AWS_ENDPOIN_URL = os.environ.get('AWS_ENDPOIN_URL')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
