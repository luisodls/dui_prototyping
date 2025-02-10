#!/usr/bin/env python3
# countasync.py

import asyncio
import time

async def count(num_in):
    print("num_in =", num_in, ", start")
    await asyncio.sleep(1)
    #time.sleep(1) # Luiso's testing hack
    print("num_in =", num_in, ", end")

async def main():
    await asyncio.gather(count(1), count(2), count(3))

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
