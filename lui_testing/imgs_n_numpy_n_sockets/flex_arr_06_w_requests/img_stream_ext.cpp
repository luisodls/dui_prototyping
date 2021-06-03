#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <iomanip>
#include <scitbx/array_family/flex_types.h>

namespace py = boost::python;
using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;

std::string img_arr_2_str(flex_double& data2d)
{
    std::string std_str = "";
    int d1 = data2d.accessor().all()[0];
    int d2 = data2d.accessor().all()[1];
    int i, j;

    std::stringstream full_stream;
    full_stream << std::fixed;
    full_stream.str("");
    full_stream.clear();

    std::stringstream stream_array;
    stream_array << std::fixed;
    stream_array << std::setprecision(2);
    stream_array.str("");
    stream_array.clear();

    full_stream << "{ " << std::quoted("d1") << ": " << d1;
    full_stream << ", " << std::quoted("d2") << ": " << d2;
    full_stream << ", " << std::quoted("str_data") << ": ";

    std::cout << "looping thru an array of: (" << d1 << ", " << d2 << ") ...\n";
    for (i = 0; i < d1; i++) {
        for (j = 0; j < d2; j++) {
            stream_array << data2d(i, j);
            if(i < d1 - 1 or j < d2 - 1){
                stream_array << ",";
            };
        }
    }
    full_stream << std::quoted(stream_array.str()) << " }";
    std_str = full_stream.str();
    std::cout << "... loop ended\n";
    return std_str;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
}
