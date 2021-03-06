from tkinter import *
from custom_functions import *
from main_functions import *
from interpreter_bror import *
import write_manager as wm

# open("custom_fuctions_dir.txt", "w").close() # clear defined functions

root = Tk()
root.tk.call("wm", "iconphoto", root._w, PhotoImage(file="LAS.png"))
root.title("LAS [inDev]")


def get_input(*args):
    print(args)
    selections = ["Math mode", "Define Function", "Delete Function"]
    mode_selection = selections[listbox.curselection()[0]]

    x = Variable("x")
    input = e1.get()
    e1.delete(0, "end")

    # this makes sure that all custom functiosn get defined
    for func in wm.get_func_list():
        exec(func + '=getfunc("' + func + '")')

    if mode_selection == "Math mode":
        try:
            text.insert(END, input + "=" + str(eval(input)) + "\n")
        except NameError:
            text.insert("end", "Error: Mathfail\n", "fail")

    if mode_selection == "Define Function":

        func_name = input[: input.find("=")]
        func_def = input[input.find("=") + 1 :]
        if func_name[-3:] == "(x)":
            func_name = func_name[:-3]

        func = customFunction(func_def, name=func_name)
        was_written = func.was_written
        if was_written:
            text.insert("end", "Defined " + input + ".\n", "success")
        elif not was_written:
            text.insert(
                "end",
                'Function "' + func_name + '" not defined. Name already taken.\n',
                "fail",
            )

    if mode_selection == "Delete Function":
        func_name = input
        if func_name[-3:] == "(x)":
            func_name = func_name[:-3]
        was_deleted = delfunc(func_name)

        if was_deleted:
            text.insert("end", 'Deleted function "' + func_name + '".\n', "success")
        elif not was_deleted:
            text.insert(
                "end", 'No stored function with name "' + func_name + '".\n', "fail"
            )


def focus_in(*args):
    if e1.get() == "Enter expression":
        e1.delete(0, "end")


# main entrty widget


# button = Button(root, text='Go', command=get_e1).pack(fill='both')#(row=1, column = 1)
e1 = Entry(root, width=2, bg="snow", relief=SUNKEN)
e1.insert(0, "Enter expression")
e1.pack(fill="x")
e1.bind("<Return>", get_input)
e1.bind("<FocusIn>", focus_in)

text = Text(root, width=60,)
text.pack(side="right", pady=10)  # (row=0)


listbox = Listbox(root, width=15, height=5, relief=RIDGE)
listbox.insert(1, "Math mode")
listbox.insert(2, "Define Function")
listbox.insert(3, "Delete Function")
listbox.pack(fill="x", anchor="n", pady=10)
listbox.activate(index=0)

# tags for colorschemes
text.tag_config("success", background="snow2", foreground="green4")
text.tag_config("fail", background="snow2", foreground="red3")


root.mainloop()
root.destroy()
