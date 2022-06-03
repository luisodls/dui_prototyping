#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <scitbx/array_family/flex_types.h>
#include <boost/lexical_cast.hpp>

namespace py = boost::python;
using scitbx::af::flex_double;
using scitbx::af::flex_grid;
using scitbx::af::flex_int;
/*
std::string build_str(flex_double& data2d)
{
    //PyEval_InitThreads();
    char std_str[15];
    std::cout << "dim 0 size =" << data2d.accessor().all()[0] << "\n" <<
                 "dim 1 size =" << data2d.accessor().all()[1] << "\n";

    int x_size = data2d.accessor().all()[0];
    int y_size = data2d.accessor().all()[1];

    int buff_size = x_size * y_size * 10;
    char ch_buff[buff_size];
    memset(ch_buff,'f',buff_size);

    pos_size = sprintf( std_str, "%.2f", d_num);


    std::string result;
    result = std::string(ch_buff, buff_size);
    return result;
}
*/


std::string slice_arr_2_str( flex_double& data2d,
                             int inv_scale,
                             int x1, int y1,
                             int x2, int y2 )
{
    int d1 = data2d.accessor().all()[0];
    int d2 = data2d.accessor().all()[1];
    int x, y, pos, pos_size, dx, dy;
    int scaled_dx, scaled_dy;

    std::cout << "\n inv_scale ="<< inv_scale << " \n";

    // verifying some variables related to array bounds
    /*
    std::cout << " x1= " << x1 << "\n y1= " << y1 <<
                "\n x2= " << x2 << "\n y2= " << y2 <<"\n";
    std::cout << " d1= " << d1 << "\n d2= " << d2 << "\n";
    */
    if(x1 >= d1 or x2 > d1 or x1 < 0 or x2 <= 0 or
       y1 >= d2 or y2 > d2 or y1 < 0 or y2 <= 0 or
       x1 > x2 or y1 > y2
    ){
        std::cout << "\n ***  array bounding error  *** \n";
        //return "Error N";
        return "Equivocadisimo";
    } else {
        std::cout << "\n ***  array bounding OK  *** \n";
    };

    double d_num;
    char std_str[15];
    dx = x2 - x1;
    dy = y2 - y1;
    //std::cout << "dx, dy  = " << dx << "," << dy << "\n";
    int buff_size = dx * dy * 15 + 30;
    /*
    std::cout << "buff_size =" << buff_size << "\n";
    std::cout << "x1, y1, x2, y2 = " << x1 << "," << y1 << "," <<
                                        x2 << "," << y2 << "," << "\n";
    */
    // creating a char buffer full of spaces
    char * ch_buff;
    ch_buff = new char[buff_size];

    memset(ch_buff,' ',buff_size);

    //pos will keep track of where to write next
    pos = 0;
    strcpy(&ch_buff[pos], "{");
    pos++;

    // writing the left side of << str_data >> field
    pos_size = sprintf( std_str, "\"str_data\":\"");
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;

    std::cout << "looping thru (" << x2 - x1 << ", " << y2 - y1
                                  << ") ... nums \n";

    // looping thru the sliced array in big jumps of size inv_scale
    int mini_x, mini_y;
    double d_tot, mini_count;
    scaled_dx = 0;

    //std::cout << "Here before loop \n";

    for (x = x1; x < x2; x += inv_scale) {
        scaled_dy = 0;
        for (y = y1; y < y2; y += inv_scale) {

            // if inv_scale is 1 there is no need to average
            // pixel intensities since is going 1 by 1
            if(inv_scale == 1){
                d_num = double(data2d(x, y));
            } else {
                d_tot = 0;
                mini_count = 0;

                // average of next [ inv_scale * inv_scale ] pixels
                //that will represent one big pixel
                for (mini_x = x;
                      mini_x < x + inv_scale and mini_x < d1;
                       mini_x++) {
                    for (mini_y = y;
                          mini_y < y + inv_scale and mini_y < d2;
                           mini_y++) {
                        d_tot = d_tot + double(data2d(mini_x, mini_y));
                        mini_count++;
                    }
                }
                d_num = d_tot / mini_count;
                /*
                in the rare case when the pointer reference  goes
                outside the array it gives a << Not A Number >> result,
                this should be replaced with a number (zero?) and print
                some log to console                 *
                 */
                if(isnan(d_num)){
                    std::cout << "some NAN in inner loop \n"
                          << "d_num = " << d_num << ", d_tot = " << d_tot
                          << ", mini_count = " << mini_count << "\n";
                    d_num = 0;
                }
            }

            // writing intensity
            pos_size = sprintf( std_str, "%.1f", d_num);
            strcpy(&ch_buff[pos], std_str);
            pos = pos + pos_size;

            // adding separator comma
            strcpy(&ch_buff[pos], ",");
            pos++;
            scaled_dy++;
        }
        scaled_dx++;
    }
    /*
    std::cout << "after loop, scaled_dx, scaled_dy ="
              << scaled_dx << ", " << scaled_dy << " \n";
    */
    // moving backwards to overwrite the last comma
    // that was written inside loop
    pos--;

    //closing quotes and adding comma
    pos_size = sprintf( std_str, "\",");
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;

    // writing the NEW << d1 >> field in JSON format, dimension #1
    pos_size = sprintf( std_str, "\"d1\":%i,", scaled_dx);
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;

    // writing the NEW << d2 >> field in JSON format, dimension #2
    pos_size = sprintf( std_str, "\"d2\":%i", scaled_dy);
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;

    //closing braces
    pos_size = sprintf( std_str, "}");
    strcpy(&ch_buff[pos], std_str);
    pos = pos + pos_size;

    //std::cout << "adding <<0>>  char to array \n";

    //finishing array with 0 char
    strcpy(&ch_buff[pos], "\0");
    pos++;

    //std::cout << " char array to std.string \n";

    std::string str_out = std::string(ch_buff, pos);
    delete[] ch_buff;
    std::cout << "done C++ \n";
    return str_out;

}


BOOST_PYTHON_MODULE(img_stream_ext)
{
    using namespace boost::python;
    //def("build_str", build_str);
    def("slice_arr_2_str", slice_arr_2_str);
}
