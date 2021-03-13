#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <cmath>
/*
#include <scitbx/array_family/boost_python/utils.h>
#include <scitbx/array_family/boost_python/flex_fwd.h>
#include <scitbx/array_family/shared.h>
*/
#include <scitbx/array_family/flex_types.h>

namespace py = boost::python;

using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;

char const* greet()
{
    return "hello, world";
}

py::list lst_bunch(flex_double& data2d)
{
    py::list data_out;
    std::cout << "\n ================= Hi ============== \n";

    /*
     * This example shows how play with strings and lists

    py::list data_out;
    py::str py_str;

    int four = 4;
    std::string std_str1, std_str2, std_str3, std_str_sum;

    data_out.append(num_lst);
    data_out.append(four);

    std_str1 = "cadena tst uno ";
    std_str2 = "cadena tst dos ";
    std_str3 = "cadena tst tres ";

    std_str_sum = std_str1;
    std_str_sum.append(std_str2);
    std_str_sum.append(std_str3);

    std::cout << "\n std_str_sum = " << std_str_sum << "\n";

    std::cout << "\n std_str1 = " << std_str1 << "\n";
    std::cout << "\n std_str2 = " << std_str2 << "\n";
    std::cout << "\n std_str3 = " << std_str3 << "\n";

    py_str = "1 2 3 4";

    data_out.append(py_str);
    data_out.append(std_str_sum);
    */

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
BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    def("greet", greet);
    def("lst_bunch", lst_bunch);
    def("arange_list", arange_list, arg("bbox_lst"), arg("hkl_lst"), arg("n_imgs"));
}
