#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <iomanip>
#include <scitbx/array_family/flex_types.h>
#include <charconv>
#include <stdlib.h>
#include <new>

namespace py = boost::python;
using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;

std::string img_arr_2_str(flex_double& data2d)

{
    /*
     * Here we generate a very long string
     * that contains and entire JSON file
     * with the dimensions (d1, d2) and
     * the array in "str_data"
     */
    int d1 = data2d.accessor().all()[0];
    int d2 = data2d.accessor().all()[1];
    int i, j, pos, pos_size;
    double d_num;
    char std_str[15];
    int buff_size = d1 * d2 * 15 + 30;
    std::cout << "buff_size =" << buff_size << "\n";
    // creating a char buffer full of spaces
    char * ch_buff;
    ch_buff = new char[buff_size];
    memset(ch_buff,' ',buff_size);
    //pos will keep track of where to write next
    pos = 0;
    // first writing in memory string, starting with << { >>
    strcpy(&ch_buff[pos], "{");
    pos++;
    // writing the << d1 >> field in JSON format, dimension #1
    pos_size = sprintf( std_str, "\"d1\":%i,", d1);
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;
    // writing the << d2 >> field in JSON format, dimension #2
    pos_size = sprintf( std_str, "\"d2\":%i,", d2);
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;
    // writing the left side of << str_data >> field
    pos_size = sprintf( std_str, "\"str_data\":\"");
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;

    // all pixel intensities should be written with a loop
    std::cout << "looping thru (" << d1 << ", " << d2 << ") ... nums \n";
    for (i = 0; i < d1; i++) {
        for (j = 0; j < d2; j++) {
            // writing intensity
            d_num = double(data2d(i, j));
            pos_size = sprintf( std_str, "%.2f", d_num);
            strcpy(&ch_buff[pos], std_str);
            pos = pos + pos_size;
            // writing coma
            strcpy(&ch_buff[pos], ",");
            pos++;
        }
    }
    std::cout << "... Loop END\n";

    // moving backwards to overwrite last coma
    pos--;
    // closing both: quotes and braces
    pos_size = sprintf( std_str, "\"}");
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;
    // passing all char buffer to a std::string to returning it
    std::string all_str((char *)ch_buff);
    // clearing memory
    delete ch_buff;
    return all_str;
}

std::string num_2_str(int a)
{
    std::string all_str("Hi there");
    int x[10];
    try
    {
        for (int i = 0; i < a; i++) {
            x[i]= i * 2;
        }
    }
    catch(std::exception& e)
    {
        std::cerr << "Exception caught : " << e.what() << std::endl;
    }

    for (int i = 0; i < a; i++) {
        std::cout << " x[" << i << "] =" << x[i] << "\n";
    };
    return all_str;

}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
    def("num_2_str", num_2_str);
}
