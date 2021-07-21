#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <iomanip>

std::string img_arr_2_str()
{
    std::string std_str = "XXXXXXXXX";
    //int i, j;
    return std_str;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
}
