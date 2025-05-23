import sys
def prin_lst(lst, curr):
    print("__________________________listing:")
    lst_stp = []
    for uni in lst:
        stp_str = str(uni.lin_num) + " comm: " + str(uni.command)

        try:
            stp_str += " prev: " + str(uni.prev_step.lin_num)

        except:
            stp_str += " prev: None"

        stp_str += " nxt: "
        try:
            for nxt_uni in uni.next_step_list:

                stp_str += "  " + str(nxt_uni.lin_num)

        except:
            stp_str += "empty"

        if curr == uni.lin_num:
            stp_str += "                           <<< here I am <<<"

        lst_stp.append(stp_str)

    print(lst_stp)
    return lst_stp


def build_dict_list(lst, curr):
    print(" - - - - - building list:")
    lst_stp = []
    for uni in lst:
        step_dict = {
            "lin_num":uni.lin_num,
            "command":str(uni.command[0])
        }

        try:
            step_dict["prev_step"] = int(uni.prev_step.lin_num)

        except:
            step_dict["prev_step"] = None

        nxt_lst = []
        try:
            for nxt_uni in uni.next_step_list:
                nxt_lst.append(int(nxt_uni.lin_num))

        except:
            pass

        step_dict["nxt"] = nxt_lst

        if( curr == uni.lin_num ):
            step_dict["here"] = True

        else:
            step_dict["here"] = False

        lst_stp.append(step_dict)

    print(lst_stp)
    return lst_stp

class show_tree(object):
    def __init__(self, uni_controler):
        self.lst_nodes = []
        self.build_recursive_list(
            step = uni_controler.step_list[0],
            curr = uni_controler.current, indent = 1
        )

        for node in self.lst_nodes:
            col = node["indent"] * 5 + 7
            for row_num in range(node["parent_row"] + 2, node["my_row"]):
                str_2_cp_from = str(self.lst_nodes[row_num]["lin2print"])
                new_str = str_2_cp_from[:col] + "|" + str_2_cp_from[col + 1:]
                self.lst_nodes[row_num]["lin2print"] = new_str

        for node in self.lst_nodes:
            print(node["lin2print"])

    def build_recursive_list(
        self, step = None, curr = None, indent = 1, parent_row = 0
    ):
        if step.success == True:
            stp_prn = " T "

        elif step.success == False:
            stp_prn = " F "

        else:
            stp_prn = " N "

        str_lin_num = "{:3}".format(step.lin_num)

        #stp_prn += str_lin_num + "     " * indent + " └──"
        stp_prn += str_lin_num + "     " * indent + " \__"
        try:
            stp_prn += str(step.command)

        except:
            stp_prn += "None"

        if step.lin_num == curr:
            stp_prn += "            <<< here "

        my_row = len(self.lst_nodes)

        step_node = {
            "indent":indent, "lin2print":stp_prn,
            "my_row":my_row, "parent_row":parent_row,
        }
        self.lst_nodes.append(step_node)

        try:
            for line in step.next_step_list:
                self.build_recursive_list(
                    step = line, curr = curr,
                    indent = indent + 1, parent_row = my_row
                )

        except:
            #print("last indent =", indent)
            pass


class uni_step(object):
    def __init__(self, prev_step):
        self.lin_num = 0
        self.next_step_list = []
        self.prev_step = prev_step
        self.command = [None]
        self.success = True

    def __call__(self, cmd_lst):
        if cmd_lst[0] == "fail":
            #testing virtual failed step
            print("\n FAILED \n")
            self.command = cmd_lst
            self.success = False

        else:
            self.command = cmd_lst
            self.success = True


class runner(object):
    ctrl_com_lst = ["goto", "fail", "slist"]
    def __init__(self):
        self.step_list = [uni_step(None)]
        self.bigger_lin = 0
        self.current = self.bigger_lin

    def run(self, command):
        print("command =", command)
        cmd_lst = command.split()
        print("__________________________________\n << running >>", cmd_lst)
        try:
            if cmd_lst[0] == "goto":
                self.goto(int(cmd_lst[1]))

            elif cmd_lst[0] == "slist":
                self.slist()

            elif cmd_lst[0].isdigit():
                print("Should go to line", int(cmd_lst[0]))
                self.goto(int(cmd_lst[0]))
                if len(cmd_lst) > 1:
                    self.exec_step(cmd_lst[1:])

            else:
                self.exec_step(cmd_lst)

        except IndexError:
            print("\n empty command \n")

    def exec_step(self, cmd_lst):
        print("self.current =", self.current)
        if self.step_list[self.current].success == True:
            self.create_step(self.step_list[self.current])
            self.step_list[self.current](cmd_lst)

        else:
            print("cannot run from failed step")

    def create_step(self, prev_step):
        new_step = uni_step(prev_step)
        self.bigger_lin += 1
        new_step.lin_num = self.bigger_lin
        self.step_list[self.current].next_step_list.append(new_step)
        self.step_list.append(new_step)
        self.goto(new_step.lin_num)

    def goto_prev(self):
        print("forking")
        try:
            self.goto(self.step_list[self.current].prev_step.lin_num)

        except:
            print("can NOT fork <None> node ")

    def goto(self, new_lin):
        if new_lin <= self.bigger_lin:
            self.current = new_lin

    def slist(self):
        print("printing in steps list mode: \n")
        prin_lst(self.step_list, self.current)


if __name__ == "__main__":
    uni_controler = runner()
    command = ""
    while command.strip() != 'exit':
        # printing new list of steps
        prin_lst(uni_controler.step_list, uni_controler.current)

        # showing tree
        print("________ showing steps tree:")
        show_tree(uni_controler)

        try:
            command = str(input(">>> "))

        except:
            print(" ...tweak key pressed ... quitting")
            sys.exit(0)

        uni_controler.run(command)

