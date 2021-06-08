// string::copy
#include <iostream>
#include <cstring>
int main ()
{
    char ch_buff[100];
    memset (ch_buff,'/',100);
    char str_tmp[25];
    int size_num, pos;
    pos = 5;
    size_num = sprintf( str_tmp, "%.2f", 3.14159);
    strcpy(&ch_buff[pos], str_tmp);
    pos = pos + size_num;

    strcpy(&ch_buff[pos], ",");
    pos++;

    size_num = sprintf( str_tmp, "%.3f", 3.14159);
    strcpy(&ch_buff[pos], str_tmp);
    pos = pos + size_num;

    strcpy(&ch_buff[pos], ",");
    pos++;

    size_num = sprintf( str_tmp, "%.4f", 987654321.12345678);
    strcpy(&ch_buff[pos], str_tmp);
    pos = pos + size_num;

    strcpy(&ch_buff[pos], ",");
    pos++;

    size_num = sprintf( str_tmp, "%.4f", 987654321012345678.12345678);
    strcpy(&ch_buff[pos], str_tmp);
    pos = pos + size_num;

    std::cout << "ch_buff contains: " << ch_buff << '\n'
              << "size_num =" << size_num << "\n";
    return 0;
}
