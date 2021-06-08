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
    int d1 = data2d.accessor().all()[0];
    int d2 = data2d.accessor().all()[1];
    int i, j, pos, pos_size;
    double d_num;
    char std_str[10];
    std::string str_end = "\n";
    int buff_size = d1 * d2 * 15;
    std::cout << "buff_size =" << buff_size << "\n";

    char * ch_buff;
    ch_buff = new char[buff_size];
    memset(ch_buff,' ',buff_size);
    pos = 0;

    std::cout << "looping thru (" << d1 << ", " << d2 << ") ... nums \n";
    for (i = 0; i < d1; i++) {
        for (j = 0; j < d2; j++) {
            d_num = double(data2d(i, j));
            pos_size = sprintf( std_str, "%.2f", d_num);
            strcpy(&ch_buff[pos], std_str);
            pos = pos + pos_size;
            if(i < d1 - 1 or j < d2 - 1){
                strcpy(&ch_buff[pos], ",");
            } else {
                strcpy(&ch_buff[pos], "\n");
            };
            pos++;
        }
    }
    std::cout << "... Loop END\n";
    std::string all_str((char *)ch_buff);
    delete ch_buff;
    return all_str;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
}
