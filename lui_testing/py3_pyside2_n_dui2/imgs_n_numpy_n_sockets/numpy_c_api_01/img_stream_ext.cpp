#include <boost/python.hpp>
#include <iostream>
#include <stdio.h>

int img_arr_2_str(int a)
{
    int b;
    printf("a =  %d \n", a);
    b = a * 2;
    printf("b =  %d \n", b);
    return b;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
}
