from multiprocessing import Process, Pipe

def func(conn, num):
    num_times_2 = num * 2
    conn.send(num_times_2)
    conn.close()

if __name__ == '__main__':
    conn01, conn02 = Pipe()
    p = Process(target=func, args=(conn02, 5))
    p.start()
    print(conn01.recv())
    p.join()
