"""
DUI's command simple stacked widgets

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

import json, os
from server.img_uploader import flex_arr_2_json

def get_data_from_steps(uni_cmd, cmd_dict, step_list):
    return_list = []

    if uni_cmd[0] == "get_optional_command_list":
        return_list = get_cmd_opt_list()

    return return_list


class build_json_data(object):
    """
    Recursively navigates the Phil objects and creates another list
    of dictionaries with info about parameters, this new list is still
    ramified with objects hierarchy
    """
    def __init__(self, phl_obj_lst):
        self.lst_obj = []
        for single_obj in phl_obj_lst:
            nxt = self.deep_in_recurs(single_obj)
            if nxt is not None:
                self.lst_obj.append(nxt)

    def __call__(self):
        return self.lst_obj

    def deep_in_recurs(self, single_obj):
        if single_obj.name == "output":
            print(" << output >> should be handled by DUI")

        elif single_obj.is_definition:
            param_info = {
                "name"          :str(single_obj.name),
                "full_path"     :str(single_obj.full_path()),
                "short_caption" :str(single_obj.short_caption),
                "help"          :str(single_obj.help),
                "type"          :None,
                "opt_lst"       :None,
                "default"       :None
            }

            if single_obj.type.phil_type == "bool":
                param_info["type"] = "bool"
                param_info["opt_lst"] = ["True", "False", "Auto"]
                if str(single_obj.extract()) == "True":
                    param_info["default"] = 0

                elif str(single_obj.extract()) == "False":
                    param_info["default"] = 1

                else:
                    param_info["default"] = 2

            elif single_obj.type.phil_type == "choice":
                param_info["type"] = "choice"
                param_info["opt_lst"] = []
                param_info["default"] = len(single_obj.words)
                for num, opt in enumerate(single_obj.words):
                    opt = str(opt)
                    if opt[0] == "*":
                        opt = opt[1:]
                        param_info["default"] = num

                    param_info["opt_lst"].append(opt)

            else:
                param_info["type"] = "other(s)"
                param_info["default"] = str(single_obj.extract())

            return param_info

        elif single_obj.is_scope:
            param_info = {
                "name"          :str(single_obj.name),
                "full_path"     :str(single_obj.full_path()),
                "short_caption" :str(single_obj.short_caption),
                "help"          :str(single_obj.help),
                "type"          :"scope",
                "child_objects" :[]
            }
            for child in single_obj.objects:
                nxt = self.deep_in_recurs(child)
                if nxt is not None:
                    param_info["child_objects"].append(nxt)

            return param_info

        else:
            print("\n", single_obj.name,
                "\n WARNING neither definition or scope\n")

        return None

def get_cmd_opt_list():
    command_list = [
        "find_spots"                        ,
        "find_rotation_axis"                ,
        "index"                             ,
        "refine"                            ,
        "integrate"                         ,
        "symmetry"                          ,
        "scale"                             ,
        "merge"                             ,
        "cosym"                             ,
        "slice_sequence"                    ,
      "align_crystal"                          ,
      "anvil_correction"                       ,
      "assign_experiment_identifiers"          ,
      "augment_spots"                          ,
      "background"                             ,
      "check_indexing_symmetry"                ,
      "cluster_unit_cell"                      ,
      "compare_orientation_matrices"           ,
      "complete_full_sphere"                   ,
      "compute_delta_cchalf"                   ,
      "convert_to_cbf"                         ,
      "create_profile_model"                   ,
      "damage_analysis"                        ,
      "data"                                   ,
      "detect_blanks"                          ,
      "estimate_gain"                          ,
      "estimate_resolution"                    ,
      "export_best"                            ,
      "export_bitmaps"                         ,
      "filter_reflections"                     ,
      "find_bad_pixels"                        ,
      "find_hot_pixels"                        ,
      "find_shared_models"                     ,
      "find_spots_client"                      ,
      "find_spots_server"                      ,
      "frame_orientations"                     ,
      "generate_distortion_maps"               ,
      "geometry_viewer"                        ,
      "goniometer_calibration"                 ,
      "image_viewer"                           ,
      "import_xds"                             ,
      "indexed_as_integrated"                  ,
      "merge_cbf"                              ,
      "merge_reflection_lists"                 ,
      "missing_reflections"                    ,
      "model_background"                       ,
      "modify_geometry"                        ,
      "plot_Fo_vs_Fc"                          ,
      "plot_reflections"                       ,
      "plot_scan_varying_model"                ,
      "plugins"                                ,
      "powder_calibrate"                       ,
      "predict"                                ,
      "rbs"                                    ,
      "reference_profile_viewer"               ,
      "refine_error_model"                     ,
      "reflection_viewer"                      ,
      "rl_png"                                 ,
      "rlv"                                    ,
      "rs_mapper"                              ,
      "search_beam_position"                   ,
      "sequence_to_stills"                     ,
      "shadow_plot"                            ,
      "show"                                   ,
      "show_build_path"                        ,
      "show_dist_paths"                        ,
      "sort_reflections"                       ,
      "split_experiments"                      ,
      "spot_counts_per_image"                  ,
      "spot_resolution_shells"                 ,
      "stereographic_projection"               ,
      "stills_process"                         ,
      "two_theta_offset"                       ,
      "two_theta_refine"                       ,
      "unit_cell_histogram"                    ,
      "version"                                ,
    ]
    return command_list


def get_param_list(cmd_str):
    connect_dict = {
            "find_spots_params"              :phil_scope_find_spots.objects    ,
            "index_params"                   :phil_scope_index.objects         ,
            "refine_bravais_settings_params" :phil_scope_r_b_settings.objects  ,
            "refine_params"                  :phil_scope_refine.objects        ,
            "integrate_params"               :phil_scope_integrate.objects     ,
            "symmetry_params"                :phil_scope_symmetry.objects      ,
            "scale_params"                   :phil_scope_scale.objects         ,
            "combine_experiments_params"     :phil_scope_combine_params.objects,
        }

    lst_dict = build_json_data(connect_dict[cmd_str])
    lst_phil_obj = lst_dict()
    return lst_phil_obj


def iter_dict(file_path, depth_ini):
    file_name = file_path.split("/")[-1]
    local_dict = {
        "file_name": file_name, "file_path": file_path, "list_child": []
    }
    if depth_ini >= 30:
        #print("reached to deep with: ", file_path)
        local_dict["isdir"] = False

    elif os.path.isdir(file_path):
        local_dict["isdir"] = True
        depth_next = depth_ini + 1
        #print("depth_next =", depth_next)
        for new_file_name in sorted(os.listdir(file_path)):
            try:
                new_file_path = os.path.join(os.sep, file_path, new_file_name)
                local_dict["list_child"].append(iter_dict(new_file_path, depth_next))

            except PermissionError:
                local_dict["list_child"] = []
                local_dict["isdir"] = False
                break
                return local_dict

    else:
        local_dict["isdir"] = False

    return local_dict

