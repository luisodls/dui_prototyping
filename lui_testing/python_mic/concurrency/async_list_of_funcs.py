import asyncio

async def say_hi(num_i):
        print("Hi there #1, inner_num =", num_i)
        await asyncio.sleep(0.333)
        print("Hi there #2, inner_num =", num_i)

async def something_2_run(num):
    print("before calling say_hi(num) ...")

    #func_lst = [say_hi(i) for i in range(num)] # same but more pythonic
    #await asyncio.gather(*func_lst)            # same but more pythonic

    func_lst = []
    for i in range(num):
        func_lst.append(say_hi(i))

    await asyncio.gather(*func_lst)
    print("... after calling say_hi(num)")

def main():
    asyncio.run(something_2_run(16))


if __name__ == "__main__":
    main()
