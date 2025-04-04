import jwt
import json
import redis
import uuid
from datetime import datetime, timedelta

class CachedTokens:
    def __init__(self, access_uid, refresh_uid):
        self.AccessUID = access_uid
        self.RefreshUID = refresh_uid


class TokenService:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def generate_token_pair(self, user_id, expire_access_minutes, expire_refresh_minutes, access_secret, refresh_secret):
        access_token, access_uid, exp_access = self.create_token(user_id, expire_access_minutes, access_secret)
        refresh_token, refresh_uid, _, exp_refresh = self.create_token(user_id, expire_refresh_minutes, refresh_secret)

        cached_tokens = CachedTokens(access_uid, refresh_uid)
        cache_json = json.dumps(cached_tokens)

        key = f"token-{user_id}"
        self.redis_client.set(key, cache_json)

        return access_token, refresh_token, exp_access, exp_refresh

    def create_token(self, user_id, expire_minutes, secret):
        exp = datetime.utcnow() + timedelta(minutes=expire_minutes)
        uid = str(uuid.uuid4())

        token = jwt.encode(
            {
                'id': user_id,
                'uid': uid,
                'exp': exp,
            },
            secret,
            algorithm='HS256',
        )

        return token, uid, exp.timestamp()


# Example usage:
user_id = 1
expire_access_minutes = 30
expire_refresh_minutes = 1440  # 24 hours
access_secret_key = 'your_access_secret_key'
refresh_secret_key = 'your_refresh_secret_key'

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
token_service = TokenService(redis_client)

access_token, refresh_token, exp_access, exp_refresh = token_service.generate_token_pair(
    user_id, expire_access_minutes, expire_refresh_minutes, access_secret_key, refresh_secret_key
)

print("Access Token:", access_token)
print("Refresh Token:", refresh_token)
print("Access Token Expiration Time:", exp_access)
print("Refresh Token Expiration Time:", exp_refresh)
