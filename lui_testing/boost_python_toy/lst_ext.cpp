#include<boost/python.hpp>
#include <iostream>

namespace py = boost::python;

char const* greet()
{
    return "hello, world";
}

int give_int()
{
    return 5;
}

py::list square(py::list num_lst)
{
    /*
     * This example shows how to input a python list
     * and plays a bit with it
     */
    py::list points;
    int one = 1;
    int two = 2;
    int three = 3;
    points.append(one);
    points.append(two);
    points.append(three);
    points.append(num_lst);
    return points;
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
BOOST_PYTHON_MODULE(lst_ext)
{
    using namespace boost::python;
    def("greet", greet);
    def("give_int", give_int);
    def("square", square);
    def("arange_list", arange_list, arg("bbox_lst"), arg("hkl_lst"), arg("n_imgs"));
    //def("arange_list", &arange_list, arg("bbox_lst"), arg("n_imgs"));


}
