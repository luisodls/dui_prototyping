'''
low level handling info for outputs in DUI

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
'''

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from dxtbx.model.experiment_list import ExperimentListFactory
from dxtbx.model import ExperimentList, Experiment
#from dxtbx.datablock import DataBlockFactory
from dials.array_family import flex
import json


def update_all_data(experiments_path = None):
    dat = {}
    try:
        experiments = ExperimentListFactory.from_json_file(
                      experiments_path, check_format=False)

    except FileNotFoundError:
        return None

    print( "len(experiments)", len(experiments))

    # FIXME take just the first experiment. What if there are more?
    exp = experiments[0]

    print("dir(exp) = ", dir(exp), "\n")
    print("dir(exp.goniometer) = ", dir(exp.goniometer), "\n")
    print(
        "exp.goniometer.get_rotation_axis()",
        exp.goniometer.get_rotation_axis(), "\n"
    )
    print(
        "exp.goniometer.get_rotation_axis_datum()",
        exp.goniometer.get_rotation_axis_datum(), "\n"
    )

    print(
        "exp.goniometer.get_setting_rotation()",
        exp.goniometer.get_setting_rotation(), "\n"
    )

    # Get beam data
    dat["w_lambda"] = exp.beam.get_wavelength()

    # Get detector data
    # assume details for the panel the beam intersects are the same for the whole detector
    pnl_beam_intersects, (beam_x, beam_y) = \
        exp.detector.get_ray_intersection(exp.beam.get_s0())
    pnl = exp.detector[pnl_beam_intersects]
    print( "beam_x, beam_y =", beam_x, beam_y)

    dat["xb"] = beam_x
    dat["yb"] = beam_y

    dist = pnl.get_distance()

    print( "pnl_beam_intersects             ", pnl_beam_intersects)
    print( "dist                            ", dist)

    return dat

if __name__ == "__main__":
    print("Running")
    data2update = update_all_data(
        experiments_path = "/tmp/run_dui2_nodes/run1/imported.expt"
    )
    print("Data =", data2update)
