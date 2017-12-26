from tkinter import *
from tkinter import messagebox
from random import shuffle
from calculations import Variant10

info = {
    "Student": "Oleksandr Korienev",
    "Group": "IV-72",
    "Number_in_list": 10
}
A = {}
B = {}
C = {}
universal_set = {}

def go_to_root(event):
    """hiding all Toplevel windows, root on top """
    win2.withdraw()
    win3.withdraw()
    root.tkraise()


def go_to_win2(event):
    """Shows window 2"""
    win3.withdraw()
    win2.deiconify()
    win2.tkraise()


def go_to_win3(event):
    """Shows window 3"""
    win2.withdraw()
    win3.deiconify()
    win3.tkraise()


def get_info(event):
    """shows messagebox with information about student"""
    a = messagebox.showinfo("Student", "{},student of {} group, number in group list: {}".format(info["Student"],
                            info["Group"], info["Number_in_list"]))


def print_calculations_result(event):
    calculation_obj = Variant10(A, B, C, universal_set)
    result = messagebox.showinfo("Result", "{}".format(calculation_obj.step_5_d_final()))


def generate_random_sets(event):
    """Generating sets for application calculations"""
    try:
        size_a = int(amount1.get())
        size_b = int(amount2.get())
        size_c = int(amount3.get())
        gen_range = (int(range_start.get()), int(range_end.get()))
        gen_A = [i for i in range(*gen_range)]
        shuffle(gen_A)
        gen_B = [i for i in range(*gen_range)]
        shuffle(gen_B)
        gen_C = [i for i in range(*gen_range)]
        shuffle(gen_C)
        global A
        global B
        global C
        global universal_set
        A = {gen_A.pop() for i in range(size_a)}
        B = {gen_B.pop() for i in range(size_b)}
        C = {gen_C.pop() for i in range(size_c)}
        universal_set = [i for i in range(min(min(A), min(B), min(C)), max(max(A), max(B), max(C)) + 1)]
        print(size_a, A, size_b, B, size_c, C)

    except ValueError:
        status["text"] = "Error occured, try again"
    except IndexError:
        status["text"] = "Size and Range of generating are not compatible"
    else:
        status["text"] = "Sets generated"
        collection_status["text"] = "Sets are not collected"


def get_sets_from_input(event):
    """strings typed in text fields are transformed into sets"""
    try:
        global A
        global B
        global C
        global universal_set
        A = set_A.get(1.0, END).split()
        A = {int(i) for i in A}
        assert len(A) > 0
        B = set_B.get(1.0, END).split()
        B = {int(i) for i in B}
        assert len(B) > 0
        C = set_C.get(1.0, END).split()
        C = {int(i) for i in C}
        assert len(C) > 0
        universal_set = [i for i in range(min(min(A), min(B), min(C)), max(max(A), max(B), max(C)) + 1)]
    except AssertionError:
        collection_status["text"] = "Sets are empty"
    except ValueError:
        collection_status["text"] = "All elements should be numbers"
    else:
        collection_status["text"] = "sets collected"
        status["text"] = "Sets are not generated"


class MyButton:
    """default class for buttons, not derived class"""
    def __init__(self, parent, button_grid=(1, 1), text="Empty", color=("AntiqueWhite", "LavenderBlush4",),
                 width=20, height=5, font="arial 14"):
        self.but = Button(parent)
        self.but["text"] = text
        self.but["bg"] = color[0]
        self.but["fg"] = color[1]
        self.but["font"] = font
        self.but["width"] = width
        self.but["height"] = height
        self.but.grid(row=button_grid[0], column=button_grid[1])


# main window (Tk)
root = Tk()
root.geometry("670x600")
root["bg"] = "RosyBrown"
root.resizable(False, False)
# navigation frame
nav_frame_1 = Frame(root)
to_root = MyButton(parent=nav_frame_1, text="window 1")
to_root.but.bind("<Button-1>", go_to_root)
to_win2 = MyButton(parent=nav_frame_1, text="window 2", button_grid=(1, 2))
to_win2.but.bind("<Button-1>", go_to_win2)
to_win3 = MyButton(parent=nav_frame_1, text="window 3", button_grid=(1, 3))
to_win3.but.bind("<Button-1>", go_to_win3)
nav_frame_1.grid(row=0, column=1)

# sets_params frame
sets_params = Frame(root)
params_help = Label(sets_params, text="random configuration", font="Arial 14")
amount1 = Entry(sets_params, width=2, font="Arial 14")
label1 = Label(sets_params, text="A: ", font="Arial 14")
amount2 = Entry(sets_params, width=2, font="Arial 14")
label2 = Label(sets_params, text="B: ", font="Arial 14")
amount3 = Entry(sets_params, width=2, font="Arial 14")
label3 = Label(sets_params, text="C: ", font="Arial 14")
label4 = Label(sets_params, text="From", font="Arial 14")
range_start = Entry(sets_params, width=3, font="Arial 14")
label5 = Label(sets_params, text="To", font="Arial 14")
range_end = Entry(sets_params, width=3, font="Arial 14")
sets_generate = MyButton(parent=sets_params, text="GENERATE", width=16, height=1)
status = Label(sets_params, text="Sets are not generated", font="Arial 14")
sets_generate.but.bind("<Button-1>", generate_random_sets)
params_help.grid(row=0, column=0)
label1.grid(row=0, column=1)
amount1.grid(row=0, column=2)
label2.grid(row=0, column=3)
amount2.grid(row=0, column=4)
label3.grid(row=0, column=5)
amount3.grid(row=0, column=6)
label4.grid(row=0, column=7)
range_start.grid(row=0, column=8)
label5.grid(row=0, column=9)
range_end.grid(row=0, column=10)
sets_generate.but.grid(row=0, column=12)
status.grid(row=1, column=0, columnspan=13)
sets_params.grid(row=1, column=1, sticky="w")
# input sets
input_set = Frame(root)
set_A = Text(input_set, width=20, height=2, wrap=WORD, font="Arial 14")
set_B = Text(input_set, width=20, height=2, wrap=WORD, font="Arial 14")
set_C = Text(input_set, width=21, height=2, wrap=WORD, font="Arial 14")
set_A.grid(row=0, column=1)
set_B.grid(row=0, column=2)
set_C.grid(row=0, column=3)
help_box = Label(input_set, text="Numbers should be divided by \" \"", font="Arial 14")
help_box.grid(row=1, column=1, columnspan=2, sticky="w")
collect = MyButton(parent=input_set, text="Collect", height=1, width=20)
collect.but.bind("<Button-1>", get_sets_from_input)
collect.but.grid(row=2, column=1)
collection_status = Label(input_set, text="No sets collected", font="Arial 14")
collection_status.grid(row=3, column=1, columnspan=2, sticky="w")
input_set.grid(row=2, column=1, sticky="w")
# result of calculations
get_result = MyButton(parent=root, text="RESULT", height=2)
get_result.but.bind("<Button-1>", print_calculations_result)
get_result.but.grid(row=3, column=1, sticky="w")
# info button
whoami = MyButton(parent=root, height=1, text="Student")
whoami.but.grid(row=5, column=1, sticky="w")
whoami.but.bind("<Button-1>", get_info)

# second window(Toplevel)
win2 = Toplevel(root)
# navigation frame
nav_frame_2 = Frame(win2)
to_root = MyButton(parent=nav_frame_2, text="window 1")
to_root.but.bind("<Button-1>", go_to_root)
to_win2 = MyButton(parent=nav_frame_2, text="window 2", button_grid=(1, 2))
to_win2.but.bind("<Button-1>", go_to_win2)
to_win3 = MyButton(parent=nav_frame_2, text="window 3", button_grid=(1, 3))
to_win3.but.bind("<Button-1>", go_to_win3)
nav_frame_2.grid(row=0, column=1)

# third window (Toplevel)
win3 = Toplevel(root)
# navigation frame
nav_frame_3 = Frame(win3)
to_root = MyButton(parent=nav_frame_3, text="window 1")
to_root.but.bind("<Button-1>", go_to_root)
to_win2 = MyButton(parent=nav_frame_3, text="window 2", button_grid=(1, 2))
to_win2.but.bind("<Button-1>", go_to_win2)
to_win3 = MyButton(parent=nav_frame_3, text="window 3", button_grid=(1, 3))
to_win3.but.bind("<Button-1>", go_to_win3)
nav_frame_3.grid(row=0, column=1)

# start of a program
win2.withdraw()
win3.withdraw()
root.mainloop()

