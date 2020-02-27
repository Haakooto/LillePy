import numpy as np
from numbers import Number as number


class Variable:
    pass


class parentFunction:
    def __init__(self, *init_structure):
        self.init_structure = init_structure

    def __call__(self, *args):
        print("hd")
        call_arg = args[0]

        if isinstance(call_arg, Variable):
            return self
        elif isinstance(call_arg, number):
            assert len(args) == 1, "Only takes 1 input"
            call_arg = args[0]
            init_structure_variables_replaced = self.replace_variables_with_number(
                call_arg
            )

            return self.call(init_structure_variables_replaced)

    def replace_variables_with_number(self, replacee):
        init_structure_variables_replaced = []
        for obj in self.init_structure:

            if isinstance(obj, parentFunction):
                init_structure_variables_replaced.append(obj.__call__(replacee))
            elif isinstance(obj, Variable):
                init_structure_variables_replaced.append(replacee)
            elif isinstance(obj, number):
                init_structure_variables_replaced.append(obj)

        return init_structure_variables_replaced


class add(parentFunction):
    def call(self, *args):
        res = 0
        for obj in args[0]:
            res += obj
        return res


class sub(parentFunction):
    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "sub takes two arguments a,b -> a - b"
        return args[0] - args[1]


class mul(parentFunction):
    def call(self, *args):
        args = args[0]
        res = 1
        for obj in args:
            res *= obj
        return res


class div(parentFunction):
    def call(self, *args):
        args = args[0]
        print(args)
        assert len(args) == 2, "div takes two arguments a,b -> a/b"
        return args[0] / args[1]


class cos(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "cos takes 1 argument a -> cos(a)"
        return np.cos(arg[0])


class sin(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "sin takes 1 argument a -> sin(a)"
        return np.sin(arg[0])


class ln(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "ln takes 1 argument a -> ln(a)"
        return np.log(arg[0])


class log(parentFunction):
    def call(self, *args):
        arg = args[0]
        assert len(arg) == 1, "log takes 1 argument a -> log(a)"
        return np.log10(arg[0])


class pow(parentFunction):
    def call(self, *args):
        args = args[0]
        assert len(args) == 2, "pow takes two arguments a,b -> a^b"
        try:
            return args[0] ** args[1]
        except RuntimeWarning:
            print("Imaginary numbers not yet supported")
            import sys

            sys.exit(1)


class sqrt(parentFunction):
    def call(self, *args):
        args = args[0]
        assert len(args) == 1, "pow takes one argument a -> sqrt(a)"
        try:
            return args[0] ** (1 / 2)
        except RuntimeWarning:
            print("Imaginary numbers not yet supported")
            import sys

            sys.exit(1)


class summation(parentFunction):
    def call(self, *args):
        print("df")
        # the calling of sum is as follows:
        # sum(sum_var, bottom_val, top_val, sum_func)
        args = args[0]
        assert (
            len(args) == 4
        ), "the calling of sum is as follows: sum(sum_var, bottom_val, top_val, sum_func)"
        sum_var, bottom_val, top_val, sum_func = args
        assert isinstance(sum_var, Variable), 'sum_var is not of instance "Variable"'
        assert isinstance(bottom_val, int), "bottom_val is not an integer"
        assert isinstance(top_val, int), "top_val is not an integer"
        assert isinstance(sum_func, parentFunction), "sum_func is not a function"
        res = 0
        for i in range(bottom_val, top_val + 1):
            res += sum_func(i)
        return res


if __name__ == "__main__":
    x = Variable
    n = Variable

    k = summation()
    print(k(n, 1, 100, add(1, n)))
