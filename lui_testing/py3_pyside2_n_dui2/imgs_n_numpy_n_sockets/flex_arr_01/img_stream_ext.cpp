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

    std::ostringstream tmp_stream;
    tmp_stream << std::fixed;
    tmp_stream << std::setprecision(2);
    std::cout << "looping thru an array of: (" << d1 << ", " << d2 << ")\n";
    for (i = 0; i < d1; i++) {
        for (j = 0; j < d2; j++) {
            tmp_stream.str("");
            tmp_stream.clear();
            tmp_stream << data2d(i, j);
            std_str.append(tmp_stream.str());
            std_str.append(",");
        }
    }

    std::cout << "loop ended\n";
    return std_str;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
}
