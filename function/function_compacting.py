from main_functions import *
from Variable import Variable
from parentFunction import parentFunction


class Compaction:
    # the idea behind the compaction class is that there will be several different types of
    # ways to compact a function. Some may require special attention to the additions,
    # some to the trigonometric, etc. Different types of compactions with different
    # 'settings' will therefore allow for exactly this
    def __init__(self, init_function):
        assert isinstance(
            init_function, parentFunction
        ), f'excpected type "parentFunction", got {type(init_function)}'
        self.init_function = init_function
        self.init_structure = init_function.init_structure

    def join_add_elements(self):
        same_func_dict = {}
        new_init_structure = self.init_structure[:]
        for i, obj1 in enumerate(new_init_structure):
            for obj2 in self.init_structure[i:]:
                if check_if_equal_functions(obj1, obj2):
                    if obj1 not in same_func_dict:
                        same_func_dict[obj1] = 1
                    else:
                        same_func_dict[obj1] += 1

                    del new_init_structure[i]
        for thing, num in same_func_dict.items():
            new_init_structure.append(mul(num, thing))
        self.init_function.init_structure = new_init_structure

    def join_mul_elements(self):
        same_func_dict = {}
        new_init_structure = self.init_structure[:]
        for i, obj1 in enumerate(new_init_structure):
            for obj2 in self.init_structure[i:]:
                if check_if_equal_functions(obj1, obj2):
                    if obj1 not in same_func_dict:
                        same_func_dict[obj1] = 1
                    else:
                        same_func_dict[obj1] += 1

                    del new_init_structure[i]
        for thing, num in same_func_dict.items():
            new_init_structure.append(pow(thing, num))
        self.init_function.init_structure = new_init_structure
        print(new_init_structure, new_init_structure[-1])


def check_if_equal_functions(func1, func2):
    if isinstance(func1, parentFunction) == isinstance(func2, parentFunction) == True:
        # there are several ways to a funct|ion can be equal
        # the first if if they are literally the same instance of a class:
        if func1 == func2:
            return True
        # the second case is if the function is of the same class and has same
        # init_structur(e but are different instances)

        if (func1.__class__ == func2.__class__) and (
            func1.init_structure == func2.init_structure
        ):
            return True

    # we need more tests here

    # if all fails, we return a negative
    return False


if __name__ == "__main__":
    x = Variable("x")
    j = mul(2, sin(x), sin(x))
    c = Compaction(j)

    c.join_mul_elements()
    print(j)
