from redis import Redis
# import redis


from modules.singleton_meta import SingletonMeta

class RedisMain(metaclass=SingletonMeta):
    redis: Redis
    host = "localhost"
    port = 6379

    def __init__(self):
        self.redis = Redis(self.host, self.port, decode_responses=True)
        
    def set_key(self, key, value):
        self.redis.set(key, value)
        
    def get_key(self, key):
        return self.redis.get(key)

    def chanel_push(self, chanel, message):
        self.redis.publish(channel=chanel, message=message)
        return self
