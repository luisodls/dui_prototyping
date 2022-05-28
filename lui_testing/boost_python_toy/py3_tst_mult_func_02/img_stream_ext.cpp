#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <scitbx/array_family/flex_types.h>
#include <boost/lexical_cast.hpp>

namespace py = boost::python;
using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;

char const* greet()
{
    return "hello, world";
}

std::string cadena1()
{
    std::string std_str = "Aa Bb";
    return std_str;
}

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

    //std::cout << "ch_buff =" << ch_buff << "\n";
    result = std::string(ch_buff, buff_size);
    //std::cout << "result =" << result << "\n";

    return result;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("greet", greet);
    def("cadena1", cadena1);
    def("build_str", build_str);
}
