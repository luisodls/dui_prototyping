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


py::list arange_list(py::list bbox_lst, py::list hkl_lst, int n_imgs)
{
    /*
     * This is the function that we actually need.
     *
     * from a list of shoe - box bounds
     * it generates a new list of reflections arranged
     * per image
     */
    std::cout << "n_imgs =" << n_imgs << "\n";

    int x_ini, y_ini, width, height;
    py::list img_lst, ref_box, tmp_lst, box_dat;

    //TODO make sure there is no way to avoid this loop
    for (int i = 0; i < n_imgs; i++){
        img_lst.append(py::list());
    }
    py::str local_hkl;

    for (int i = 0; i < len(bbox_lst); i++){
        ref_box = py::extract<py::list>(bbox_lst[i]);
        x_ini = py::extract<int>(ref_box[0]);
        y_ini = py::extract<int>(ref_box[2]);
        width = py::extract<int>(ref_box[1]) - py::extract<int>(ref_box[0]);
        height = py::extract<int>(ref_box[3]) - py::extract<int>(ref_box[2]);

        box_dat = py::list();
        box_dat.append(x_ini);
        box_dat.append(y_ini);
        box_dat.append(width);
        box_dat.append(height);


        if( len(hkl_lst) <= 1 ){
            local_hkl = "";
            box_dat.append(local_hkl);
        } else {
            //box_dat.append(py::extract<std::string>(hkl_lst[i]));
            local_hkl = py::extract<py::str>(hkl_lst[i]);
            if(local_hkl == "(0, 0, 0)"){
                local_hkl = "NO Index";
            }
            box_dat.append(local_hkl);
        }

        for (int idx = py::extract<int>(ref_box[4]);
             idx < py::extract<int>(ref_box[5]);
             idx++){
            tmp_lst = py::extract<py::list>(img_lst[idx]);
            tmp_lst.append(box_dat);
        }
    }

    return img_lst;
}

std::string add_elem_as_str(flex_double& data2d)
{
    std::string std_str = "";
    int nrow = data2d.accessor().all()[0];
    int ncol = data2d.accessor().all()[1];
    int col, row, tot = 0;

    std::cout << "nrow = " << nrow << "\n";
    std::cout << "ncol = " << ncol << "\n";
    for (row = 0; row < nrow; row++) {
        for (col = 0; col < ncol; col++) {
            tot = tot + data2d(row, col);
        }
    }
    std_str.append(boost::lexical_cast<std::string>(tot));
    return std_str;
}


BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("greet", greet);
    def("cadena1", cadena1);
    def("lst_bunch", lst_bunch);
    def("arange_list", arange_list, arg("bbox_lst"), arg("hkl_lst"), arg("n_imgs"));
    def("add_elem_as_str", add_elem_as_str);
}
