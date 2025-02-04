import asyncio
from time import sleep
async def cout_nums(rep):
    for iner_rep in range(rep):
        await asyncio.sleep(0.2)
        print("rep =", rep, "iner_rep =", iner_rep)

def main():
    for rep in range(5):
        asyncio.run(cout_nums(rep))

if __name__ == "__main__":
    main()

