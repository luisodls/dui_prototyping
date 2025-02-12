from concurrent.futures import ThreadPoolExecutor
import time

def task(name, delay):
    print(f"Hey {name}, I will greet you in {delay} seconds")
    time.sleep(delay)
    print(f"Hello {name} after {delay} seconds")

def main():
    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(task, "Peter", 1)
        future2 = executor.submit(task, "Paul", 2)
        print("############ ... test here 1")
        future1.result()
        future2.result()
        print("############ ... test here 2")

if __name__ == "__main__":
    main()
