import get_info
import time
from pyrate_limiter import Duration, RequestRate, Limiter, BucketFullException


per_second_rate = RequestRate(19, Duration.SECOND) # 20 requests per second
minute_rate = RequestRate(99, Duration.MINUTE * 2) # 100 requests per 2 minutes
limiter = Limiter(per_second_rate, minute_rate)

start_time = time.time()
get_info.get_score("wwwwwwwwwwwwyatt", limiter)
dif = time.time() - start_time

print("Program ran in %.2f seconds" % dif)