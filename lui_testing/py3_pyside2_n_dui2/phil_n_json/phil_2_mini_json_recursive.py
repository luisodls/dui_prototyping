import json
import libtbx.phil

from dials.command_line.find_spots import phil_scope as phil_scope_find_spots
from dials.command_line.index import working_phil as phil_scope_index
from dials.command_line.refine import working_phil as phil_scope_refine
from dials.command_line.integrate import phil_scope as phil_scope_integrate

from dials.command_line.scale import phil_scope as phil_scope_scale
from dials.command_line.symmetry import phil_scope as phil_scope_symmetry

from dials.command_line.refine_bravais_settings import (
    phil_scope as phil_scope_r_b_settings,
)
from dials.command_line.combine_experiments import (
    phil_scope as phil_scope_combine_params
)

class build_json_data(object):
    """
    Recursively navigates the Phil objects in a way that the final
    self.lst_obj is a lineal list without ramifications, then another list
    is created with the info about parameters
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



class tree_2_lineal(object):
    """
    Recursively navigates the Phil objects in a way that the final
    self.lst_obj is a lineal list without ramifications, then another list
    is created with the info about parameters
    """
    def __init__(self, phl_obj_lst):
        self.lst_obj = []
        self.deep_in_recurs(phl_obj_lst)

    def __call__(self):
        return self.lst_obj

    def deep_in_recurs(self, phl_obj_lst):
        for single_obj in phl_obj_lst:
            single_obj["indent"] = int(str(single_obj["full_path"]).count("."))
            if single_obj["name"] == "output":
                print(" << output >> should be handled by DUI")

            elif single_obj["type"] == "scope":
                self.lst_obj.append(single_obj)
                self.deep_in_recurs(single_obj["child_objects"])


            else:
                self.lst_obj.append(single_obj)



if __name__ == "__main__":
    lst_dict = build_json_data(phil_scope_find_spots.objects)
    #lst_dict = build_json_data(phil_scope_index.objects)
    #lst_dict = build_json_data(phil_scope_integrate.objects)
    #lst_dict = build_json_data(phil_scope_r_b_settings.objects)
    #lst_dict = build_json_data(phil_scope_refine.objects)
    #lst_dict = build_json_data(phil_scope_scale.objects)
    #lst_dict = build_json_data(phil_scope_symmetry.objects)

    lst_phil_obj = lst_dict()

    json_str = json.dumps(lst_phil_obj, indent = 4)
    #print(json_str, "\n\n")
    new_lst = json.loads(json_str)

    lin_lst = tree_2_lineal(new_lst)
    new_lin_lst = lin_lst()
    #print(new_lin_lst)


    for data_info in new_lin_lst:
        par_str = "    " * data_info["indent"]
        par_str += data_info["name"]
        try:
            default = data_info["default"]
            if(
                (data_info["type"] == "bool" or data_info["type"] == "choice")
                and default is not None
            ):
                par_str += "  =  " + str(data_info["opt_lst"][default])

            else:
                par_str += "  =  " + str(data_info["default"])

        except KeyError:
            pass

        print(par_str)
