#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <scitbx/array_family/flex_types.h>
#include <boost/lexical_cast.hpp>

namespace py = boost::python;
using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;
using scitbx::af::flex_bool;
std::string build_str(flex_double& data2d)
{
    char std_str[15];
    std::cout << "dim 0 size =" << data2d.accessor().all()[0] << "\n" <<
                 "dim 1 size =" << data2d.accessor().all()[1] << "\n";

    int x_size = data2d.accessor().all()[0];
    int y_size = data2d.accessor().all()[1];

    int buff_size = x_size * y_size * 10;
    char ch_buff[buff_size];
    memset(ch_buff,'f',buff_size);

    std::string result;
    result = std::string(ch_buff, buff_size);
    return result;
}

std::string mask_arr_2_str(flex_bool& data2d)
{
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
            d_num = bool(data2d(i, j));
            if(d_num == true){
                strcpy(&ch_buff[pos], "1");
            } else {
                strcpy(&ch_buff[pos], "0");
            }
            pos++;
        }
    }
    std::cout << "... Loop END\n";

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

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("build_str", build_str);
    def("mask_arr_2_str", mask_arr_2_str);
}
