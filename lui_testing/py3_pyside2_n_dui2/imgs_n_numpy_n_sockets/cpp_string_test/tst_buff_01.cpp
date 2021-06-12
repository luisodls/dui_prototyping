// string::copy
#include <iostream>
#include <string>

int main ()
{
    char buffer[100];
    std::fill(std::begin(buffer), std::end(buffer), ' ');
    std::string str_tmp;
    std::string str_coma = ",";
    str_tmp = std::to_string(3.14159265358);
    str_tmp.copy(&buffer[0], str_tmp.size(), 0);
    str_coma.copy(&buffer[9], 1, 0);

    str_tmp.copy(&buffer[10], str_tmp.size(), 0);
    str_coma.copy(&buffer[19], 1, 0);

    str_tmp.copy(&buffer[20], str_tmp.size(), 0);
    str_coma.copy(&buffer[29], 1, 0);

    str_tmp.copy(&buffer[30], str_tmp.size(), 0);
    str_coma.copy(&buffer[39], 1, 0);

    std::cout << "str_tmp.size() = " << str_tmp.size() << "\n";
    std::cout << "buffer contains: " << buffer << '\n';
    return 0;
}
