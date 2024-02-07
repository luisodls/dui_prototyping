import os

def imprime_algo_mas(str_out):
    print(str_out)

def lee_un_fichero():
    abs_path = str(os.path.dirname(os.path.abspath(__file__)))
    print("abs_path =", abs_path)
    resr_path = abs_path + "/res_txt/data.txt"
    print("leyendo contenido de:", resr_path)

    fil = open(resr_path, "r")
    str_file = fil.read()
    fil.close()
    print("str from file =", str_file)


if __name__ == "__main__":
    imprime_algo_mas("Hi there #3")
    lee_un_fichero()

