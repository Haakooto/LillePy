import numpy as np
from interpreter_bror import listed_nest_remover
from main_functions2 import add, parentFunction


class Interpreter:
    """
    class for turning an arbitrary str to function
    """

    symb_type = {"number": 1, "variable": 2, "operator": 3}
    operator_list = ["+", "-", "*", "/"]

    def __init__(self, expr):
        self.original = expr
        self.expr = expr.replace(" ", "")

        self.classify()
        self.reformat_expression()

    def classify(self):
        """
        makes two lists, one with each symbol in str, one with type of symbol
        """
        constructor = []
        constructor_type = []

        # Classify each symbol in expr as number, operator or letter
        for symb in self.expr:
            if symb in self.operator_list:
                constructor_type.append(self.symb_type["operator"])
            else:
                try:
                    float(symb)
                    constructor_type.append(self.symb_type["number"])
                except ValueError:
                    constructor_type.append(self.symb_type["variable"])
            constructor.append(symb)

        self.constructor = constructor
        self.constructor_type = constructor_type

    def reformat_expression(self):
        """
        finds cocurrent symbols of same type, merge them, so "1, 2" becomes 12
        """

        def merge_and_del(here):
            self.constructor[here] += self.constructor[here + 1]
            del self.constructor[here + 1]
            del self.constructor_type[here + 1]

        here = 0
        typ = lambda idx: self.constructor_type[here + idx]
        while True:
            try:
                value = typ(0) * typ(1)
            except IndexError:
                break
            else:
                if value == 1:  # two numbers
                    merge_and_del(here)
                elif value == 2:  # number and variable
                    here += 1
                    self.constructor.insert(here, "*")
                    self.constructor_type.insert(here, self.symb_type["operator"])
                elif value == 3:  # number and operator
                    here += 1
                elif value == 4:  # two variables
                    merge_and_del(here)
                elif value == 6:  # number and operator
                    here += 1
                elif value == 9:  # two operators
                    self.check_valid_double_operator()

        # go from str to int where possible
        for i in range(len(self.constructor)):
            if self.constructor_type[i] == 1:
                self.constructor[i] = int(self.constructor[i])

    def check_valid_double_operator(self):
        """For symbols like **, ==, !="""
        pass

    # def add_variables(self):
    #     vars = np.asarray(self.constructor)[
    #         np.where(np.asarray(self.constructor_type) == 2)
    #     ]
    #     self.base._add_variables(vars)

    def split_at_add_old(self):
        final_list = []

        here = -1
        while True:
            here += 1
            try:
                symb = self.constructor[here]
            except IndexError:
                break

            if isinstance(symb, parentFunction):
                pass

            if symb == "(":
                parenthesis_count = 0
                there = 0
                while True:
                    other = self.constructor[here + there]
                    if other == "(":
                        parenthesis_count += 1
                    elif other == ")" and parenthesis_count == 0:
                        self.cut_out_inner_func(here, there)
                        break
                    elif other == ")":
                        parenthesis_count -= 1
                    there += 1

            elif symb == "+":
                final_list.append([])

    def split_at_add(self):
        constructor = np.asarray(self.constructor, dtype=object)
        final = []

        plus = np.where(constructor == "+")[0]
        # print(plus)
        if plus.size > 0:

            final.append(list(constructor[0 : plus[0]]))
            for p in range(len(plus)):
                try:
                    final.append(list(constructor[plus[p] + 1 : plus[p + 1]]))
                except IndexError:
                    final.append(list(constructor[plus[-1] + 1 :]))
                # if p == 0:
                #     final.append(list(constructor[0 : plus[0]]))
                #     final.append(list(constructor[plus[0] + 1 : plus[1]]))
                # elif p == len(plus) - 1:
                #     final.append(list(constructor[plus[p] + 1 :]))
                # else:
                #     final.append(list(constructor[plus[p] + 1 : plus[p + 1]]))
        return add(listed_nest_remover(final))

        # for here, symb in enumerate(self.constructor):
        #     if symb == "(":
        #         parenthesis_count = 0
        #         for there, sy in enumerate(self.constructor[here:]):
        #             if sy == "(":
        #                 parenthesis_count += 1
        #             elif sy == ")" and parenthesis_count == 0:
        #                 self.cut_out_inner_func(here, there)
        #             elif sy == ")":
        #                 parenthesis_count -= 1

        #     elif symb == "+":
        #         print(here)
        #         tmp_list = []
        #         sy = self.constructor[0]
        #         while sy != "+":
        #             tmp_list.append(sy)
        #             del self.constructor[0]
        #             sy = self.constructor[0]
        #         final_list.append(tmp_list)
        #         print(tmp_list)
        #         print(self.constructor)

        # print(final_list)
        # self.final = add(final_list)


expression = "1*2+3*4"
# expression = "211vs*3+53*lpets*ts+1+x+2+3+4"
# expression = "1+2+3"

I = Interpreter(expression)
print(I.constructor)
a = I.split_at_add()
print(a)
# print(I.constructor_type)

