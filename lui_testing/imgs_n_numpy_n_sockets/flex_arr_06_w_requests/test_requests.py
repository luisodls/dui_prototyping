"""
DUI2's server connecting test

Author: Luis Fuentes-Montero (Luiso)
With strong help from DIALS and CCP4 teams

copyright (c) CCP4 - DLS
"""

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import sys, json
import requests
import time

if __name__ == "__main__":
    my_cmd = {"nod_lst":[1], "cmd_lst":["gi 6"]}

    start_tm = time.time()
    req_get = requests.get(
        'http://localhost:8080/', stream = True, params = my_cmd
    )

    while True:
        tmp_dat = req_get.raw.readline()
        line_str = str(tmp_dat.decode('utf-8'))

        if line_str[-7:] == '/*EOF*/':
            print('/*EOF*/ received')
            break

        else:
            #print(line_str[:-1])
            print(line_str[0:65])
            print(line_str[-65:])


    end_tm = time.time()
    print("request took ", end_tm - start_tm)

