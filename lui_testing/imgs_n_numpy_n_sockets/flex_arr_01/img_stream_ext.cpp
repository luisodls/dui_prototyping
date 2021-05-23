#include <boost/python.hpp>
//#include <iostream>
//#include <string>
#include <scitbx/array_family/flex_types.h>
//#include <boost/lexical_cast.hpp>

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

    std::cout << "d1 = " << d1 << "\n";
    std::cout << "d2 = " << d2 << "\n";
    for (i = 0; i < d1; i++) {
        for (j = 0; j < d2; j++) {
            std_str.append(
                boost::lexical_cast<std::string>(data2d(i, j))
            );
            /* TODO
             * consider in the future to replace the next if
             * with a removal of the final coma outside the loop
            */
            if(i < d1 - 1 or j < d2 - 1){
                std_str.append(",");
            }
        }
    }
    return std_str;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("img_arr_2_str", img_arr_2_str);
}
