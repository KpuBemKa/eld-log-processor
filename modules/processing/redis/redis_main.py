from threading import Lock
import redis


class SingletonMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class RedisMain(metaclass=SingletonMeta):
    redis = None
    host = "localhost"
    port = 6379

    def __init__(self):
        self.redis = redis.Redis(self.host, self.port, decode_responses=True)
        self.redis.get
        
    def set_key(self, key, value):
        self.redis.set(key, value)
        
    def get_key(self, key):
        return self.redis.get(key)

    def chanel_push(self, chanel, message):
        self.redis.publish(channel=chanel, message=message)
        return self
