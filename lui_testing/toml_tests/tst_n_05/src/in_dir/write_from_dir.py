import os

def imprime_algo_mas(str_out):
    print(str_out)

def lee_un_fichero():
    print("os.path.dirname(os.path.abspath(__file__))", os.path.dirname(os.path.abspath(__file__) ) )

    print("leyendo")


if __name__ == "__main__":
    imprime_algo_mas("Hi there #3")
    lee_un_fichero()

