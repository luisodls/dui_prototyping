from concurrent.futures import ThreadPoolExecutor
import time

def task(name, delay):
    print(f"Hey {name}, I will greet you in {delay} seconds")
    time.sleep(delay)
    print(f"Hello {name} after {delay} seconds")

def main():
    with ThreadPoolExecutor() as executor:
        lst_exec = []
        for num in range(2, 5):
            new_exec = executor.submit(task, "num "+ str(num), int(num))
            lst_exec.append(new_exec)

        print("############ ... test here 1")
        time.sleep(3.5)
        print("############ ... test here 2")

        for new_exec in lst_exec:
            new_exec.result()

        print("############ ... test here 3")

if __name__ == "__main__":
    main()
