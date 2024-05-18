import redis
import time

redis_cli = redis.Redis(host='localhost', port=6379, db=0)


def redis_expire(db_name, exptime):
    redis_cli.set(db_name, f'{time.ctime(time.time())}, system: {db_name}')
    redis_cli.expire(db_name, exptime)


def monitor_redis():
    while True:
        keys = redis_cli.keys('*')
        for i in keys:
            ttl = redis_cli.ttl(i)
            print(ttl)
            if ttl >= 0 and ttl <= 10:
                print(ttl, 'pwd changed')
                redis_cli.delete(i)
        time.sleep(5)

