import get_info
import asyncio
import time

start_time = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(get_info.get_info("wwwwwwwwwwwwyatt"))
loop.run_until_complete(future)
dif = time.time() - start_time

print("Program ran in %.2f seconds" % dif)