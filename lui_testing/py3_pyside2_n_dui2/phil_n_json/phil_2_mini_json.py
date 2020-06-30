import libtbx.phil
from dials.command_line.find_spots import phil_scope as phil_scope_find_spots


class tree_2_lineal(object):
    """
    Recursively navigates the Phil objects in a way that the final
    self.lst_obj is a lineal list without ramifications, this final list
    will be used later to generate a dynamic GUI
    """
    def __init__(self, phl_obj):
        self.lst_obj = []
        self.deep_in_rec(phl_obj)

    def __call__(self):
        return self.lst_obj

    def deep_in_rec(self, phl_obj):

        for single_obj in phl_obj:
            if single_obj.is_definition:
                param_info = {
                    "name"          :str(single_obj.name),
                    "full_path"     :str(single_obj.full_path()),
                    "short_caption" :str(single_obj.short_caption),
                    "help"          :str(single_obj.help),
                    "indent"        :int(str(single_obj.full_path()).count(".")),
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
                    param_info["type"] = "number(s)"
                    param_info["default"] = ""

                self.lst_obj.append(param_info)


            elif single_obj.is_scope:
                if single_obj.name != "output":
                    param_info = {
                        "name"          :str(single_obj.name),
                        "full_path"     :str(single_obj.full_path()),
                        "short_caption" :str(single_obj.short_caption),
                        "help"          :str(single_obj.help),
                        "indent"        :int(str(single_obj.full_path()).count(".")),
                        "type"          :"scope"
                    }
                    self.lst_obj.append(param_info)
                    self.deep_in_rec(single_obj.objects)

                else:
                    print(
                        'The ', single_obj.name,
                        ' set of parameters is automatically handled by DUI Cloud',
                    )

            else:
                print(
                    "\n _____________ <<< WARNING neither definition or scope\n"
                )


if __name__ == "__main__":
    print("hi")
    lst_obj = tree_2_lineal(phil_scope_find_spots.objects)
    lst_phil_obj = lst_obj()

    for phl_obj in lst_phil_obj:
        #print(phl_obj, "\n")
        par_str = "   " * phl_obj["indent"]
        par_str += phl_obj["name"]
        try:
            par_str += "    " + str(phl_obj["default"])

        except KeyError:
            pass

        print(par_str)

