import os
import redis

redis_connection_pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'),
                       port=os.getenv('REDIS_PORT'),
                       db=os.getenv('REDIS_DB'),
                       password=os.getenv('REDIS_PASSWORD'),
                       decode_responses=True,
                       encoding='KOI8-R'
                       )

redis_db = redis.Redis(connection_pool=redis_connection_pool)