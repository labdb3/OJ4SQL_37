from redis import StrictRedis
import pickle as pk
redis = StrictRedis(host='localhost', port='6380', db=1)
pid = input().strip()
names = [pid+name for name in ['mysql', 'postgresql', 'opengauss']]
print(redis.delete(*names))
