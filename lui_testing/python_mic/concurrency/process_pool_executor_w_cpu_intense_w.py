from concurrent.futures import ProcessPoolExecutor
import time

def cpu_bound_task(n):
    result = 0
    for i in range(n):
        result += i

    return result

def task(num_in):
    print(f"Called with in {num_in} number step 1")
    gauss_numb = cpu_bound_task(num_in)
    print(f"Called with in {num_in} number step 2")
    return gauss_numb

def main():
    with ProcessPoolExecutor() as executor:
        lst_exec = []
        for num in range(60000000, 60000004):
            new_exec = executor.submit(task, int(num))
            lst_exec.append(new_exec)

        print("############ ... test here 1")

        for pos, new_exec in enumerate(lst_exec):
            result = new_exec.result()
            print(f"result({pos}) = {result}")

        print("############ ... test here 2")

if __name__ == "__main__":
    main()
