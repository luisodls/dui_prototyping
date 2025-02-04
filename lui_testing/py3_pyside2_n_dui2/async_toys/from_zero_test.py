import asyncio

async def cout_nums(rep):
    for iner_rep in range(rep):
        await asyncio.sleep(0.2)
        print("rep =", rep, "iner_rep =", iner_rep)

async def main():
    lst = []
    for num in range(10):
        lst.append(cout_nums(num))

    await asyncio.gather(*lst)

if __name__ == "__main__":
    asyncio.run(main())
