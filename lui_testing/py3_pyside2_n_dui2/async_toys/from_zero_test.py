import asyncio

async def say_hello():
    print("Hello...")
    await asyncio.sleep(2)  # Simulates a delay (non-blocking)
    print("World!")

async def main():
    await say_hello()  # Calling the async function

asyncio.run(main())

