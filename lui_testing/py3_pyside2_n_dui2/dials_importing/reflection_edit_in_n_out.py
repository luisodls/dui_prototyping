# LIBTBX_PRE_DISPATCHER_INCLUDE_SH export PHENIX_GUI_ENVIRONMENT=1

from __future__ import annotations

import dials.util
import libtbx.phil
from dials.array_family import flex

help_message = """

This program is used to remove reflections from a reflection list

Example for invoking from CLI:

dials.reflection_remove observations.refl 5,8,9,15

"""

def in_table(data_in_one):
    if isinstance(data_in_one, flex.reflection_table):
        table = data_in_one
        print("entered reflection Table")

    else:
        print("NOT entered reflection Table")


class Script:
    """The debugging visualization program."""

    def __init__(self):
        """Initialise the script."""
        from dials.util.options import ArgumentParser

        usage = "dials.reflection_remove [options] reflection.refl"

        # Create the parser
        self.parser = ArgumentParser(
            usage=usage, epilog=help_message, read_reflections=True
        )

    def run(self, args=None):

        from dials.util.options import flatten_reflections
        #from dials.viewer.viewer_interface import extract_n_show

        # Parse the command line
        params, options = self.parser.parse_args(args, show_diff_phil=True)
        table = flatten_reflections(params.input.reflections)
        if len(table) == 0:
            self.parser.print_help()
            return

        #extract_n_show(table[0])
        in_table(table[0])

@dials.util.show_mail_handle_errors()
def run(args=None):
    script = Script()
    script.run(args)


if __name__ == "__main__":
    run()



##########################################################################

# The phil scope
phil_scope = libtbx.phil.parse(
    """
    output {
        reflections = refined.refl
            .type = str
            .help = "The filename for reflections with updated predictions"

        log = dials.refine.log
            .type = str

    }
    """
)
