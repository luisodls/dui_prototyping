#!/usr/bin/env python3
# countasync.py

import asyncio
import time

async def count(num_in):
    print("num_in =", num_in, ", start")
    await asyncio.sleep(1)
    #time.sleep(1) # Luiso's testing hack
    print("num_in =", num_in, ", end")

async def run_all():
    await asyncio.gather(count(1), count(2))
    await asyncio.gather(count(3), count(4))

def run_cycle(n):
    for i in range(3):
        asyncio.run(count(i))

def main():
    s = time.perf_counter()
    asyncio.run(run_all())
    #run_cycle(3)
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")

if __name__ == "__main__":
    main()
