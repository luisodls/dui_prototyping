#include <boost/python.hpp>
//#include <iostream>
//#include <string>
#include <scitbx/array_family/flex_types.h>
//#include <boost/lexical_cast.hpp>

namespace py = boost::python;
using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;

py::list lst_bunch(flex_double& data2d)
{
    py::list data_out;
    std::string std_str = "";
    int nrow = data2d.accessor().all()[0];
    int ncol = data2d.accessor().all()[1];
    int col, row;

    std::cout << "nrow = " << nrow << "\n";
    std::cout << "ncol = " << ncol << "\n";
    for (row = 0; row < nrow; row++) {
        for (col = 0; col < ncol; col++) {
            std_str.append(
                boost::lexical_cast<std::string>(data2d(row, col))
            );
            std_str.append(",");
        }
    }
    data_out.append(std_str);

    return data_out;
}

BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("lst_bunch", lst_bunch);
}
