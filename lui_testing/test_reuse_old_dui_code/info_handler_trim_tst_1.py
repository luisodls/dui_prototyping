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

class InfoData(object):
    def __init__(self):

        self.a = None
        self.b = None
        self.c = None
        self.alpha = None
        self.beta = None
        self.gamma = None
        self.spg_group = None

        self.r1 = None
        self.r2 = None
        self.r3 = None

        self.xb = None
        self.yb = None
        self.dd = None

        self.w_lambda =None

        self.img_ran1 = None
        self.img_ran2 = None
        self.oscil1 = None
        self.oscil2 = None
        self.e_time = None

        self.n_pans = None
        self.x_px_size = None
        self.y_px_size = None
        self.gain = None
        self.max_res = None

        self.n_strng = None
        self.n_index = None
        self.n_refnd = None
        self.n_integ_sum = None
        self.n_integ_prf = None

        self.tmpl_str = None

def update_all_data(experiments_path = None):
    dat = InfoData()

    if(experiments_path != None):
        try:
            experiments = ExperimentListFactory.from_json_file(
                          experiments_path, check_format=False)
        except:
            try:
                # FIXME here only take the first datablock. What if there are more?
                datablock = ExperimentListFactory.from_serialized_format(experiments_path, check_format=False)[0]

                # FIXME here only take the first model from each
                beam = datablock.unique_beams()[0]
                detector = datablock.unique_detectors()[0]
                scan = datablock.unique_scans()[0]

                # build a pseudo ExperimentList (with empty crystals)
                experiments=ExperimentList()
                experiments.append(Experiment(
                    beam=beam, detector=detector, scan=scan))

            except ValueError:
                print( "failed to read json file")
                return dat

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
        dat.w_lambda = exp.beam.get_wavelength()

        # Get detector data
        # assume details for the panel the beam intersects are the same for the whole detector
        pnl_beam_intersects, (beam_x, beam_y) = \
            exp.detector.get_ray_intersection(exp.beam.get_s0())
        pnl = exp.detector[pnl_beam_intersects]
        print( "beam_x, beam_y =", beam_x, beam_y)
        print("pnl =", pnl)
        dat.xb = beam_x
        dat.yb = beam_y

        dist = pnl.get_distance()

        print( "pnl_beam_intersects             ", pnl_beam_intersects)
        print( "dist                            ", dist)

        dat.dd = dist

        dat.n_pans = len(exp.detector)
        dat.x_px_size, dat.y_px_size = pnl.get_pixel_size()
        dat.gain = pnl.get_gain()
        dat.max_res = exp.detector.get_max_resolution(exp.beam.get_s0())

    return dat

if __name__ == "__main__":
    print("Running")
    data2update = update_all_data(
        experiments_path = "/tmp/run_dui2_nodes/run1/imported.expt"
    )
    print("Data(xb, yb) =", data2update.xb, data2update.yb)
