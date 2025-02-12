import asyncio
import time

async def say_hi(num_i):
        print("Hi there #1, inner_num =", num_i)
        await asyncio.sleep(1)
        print("Hi there #2, inner_num =", num_i)

async def something_2_run(num):
    print("before calling say_hi(num) ...")
    lst_co_rout = []
    for i in range(num):
        new_co_rout = asyncio.create_task(say_hi(i))
        lst_co_rout.append(new_co_rout)

    print("... after calling say_hi(num)")

    for co_rout in lst_co_rout:
        await co_rout

def main():
    asyncio.run(something_2_run(5))


if __name__ == "__main__":
    main()
