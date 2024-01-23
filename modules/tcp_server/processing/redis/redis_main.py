import redis


class RedisMain:
    redis = None
    host = "localhost"
    port = 6379

    def __init__(self):
        self.redis = redis.Redis(self.host, self.port, decode_responses=True)

    def chanel_push(self, chanel, message):
        self.redis.publish(channel=chanel, message=message)
        return self
