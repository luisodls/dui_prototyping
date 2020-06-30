import libtbx.phil
from dials.command_line.find_spots import phil_scope as phil_scope_find_spots

class ScopeData(object):
    """
    class conceived to store only data related to the scope Phil object
    """
    pass


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
                self.lst_obj.append(single_obj)
                print("single_obj.full_path(): ", single_obj.full_path())

            elif single_obj.is_scope:
                if single_obj.name != "output":
                    scope_info = ScopeData()
                    scope_info.name = str(single_obj.name)
                    scope_info.f_path = str(single_obj.full_path())
                    scope_info.i_m_scope = True
                    scope_info.short_caption = single_obj.short_caption
                    scope_info.help = single_obj.help

                    print("scope_info.f_path =", scope_info.f_path)
                    scope_info.indent = scope_info.f_path.count(".")
                    print("scope_info.f_path.count('.') =", scope_info.indent)

                    self.lst_obj.append(scope_info)
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

