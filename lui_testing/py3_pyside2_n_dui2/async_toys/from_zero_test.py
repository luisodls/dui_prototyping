
import asyncio

async def cout_nums(rep):
    for iner_rep in range(rep):
        await asyncio.sleep(0.2)
        print("rep =", rep, "iner_rep =", iner_rep)

async def main():
    await asyncio.gather(
        cout_nums(0),
        cout_nums(1),
        cout_nums(2),
        cout_nums(3),
        cout_nums(4)
    )

if __name__ == "__main__":
    asyncio.run(main())
