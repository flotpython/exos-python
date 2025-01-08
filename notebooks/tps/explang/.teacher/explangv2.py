"""
A small expressions language, with variables
"""

# https://docs.python.org/3/library/operator.html
# typically neg looks like
# neg = lambda x: -x
# and add is like
# add = lambda x, y: x + y

from operator import neg, add, sub, mul, truediv


class Expression:
    """
    the root of all expression classes
    useful for type checking - search for isinstance below

    in this second version we take advantage of this class to factorize
    this type-checking oriented snippet
    """

    def check_is_expression(self, expression):
        classname = self.__class__.__name__
        if not isinstance(expression, Expression):
            raise TypeError(f"passing a non-Expression object in {classname} is not supported")


class Atom(Expression):
    """
    a class to implement an atomic value,
    like an int, a float, a str, ...

    in order to be able to use this,
    child classes need to provide self.implementation_type
    that should be a Python class - like typically int or float
    or similar whose constructor expects one arg
    """
    def __init__(self, value):
        # convert the argument into the specific class implementation type
        self.value = self.implementation_type(value)

    def eval(self, env):
        return self.value



class Unary(Expression):
    """
    the mother of all unary operators

    in order to be able to use this,
    child classes need to provide self.operation
    which is expected to be a 1-parameter function
    """
    def __init__(self, operand):
        self.check_is_expression(operand)
        self.operand = operand

    def eval(self, env):
        """
        just apply the class-defined attribute 'operation'
        to the (evaluation of the) operand
        """
        try:
            return self.operation(self.operand.eval(env))
        except AttributeError:
            classname = self.__class__.__name__
            print(f"WARNING - class {classname} lacks the attribute 'operation'")



# we can factor true binary (minus and divide) with n-ary (plus and mult)
# if we're a little careful about how we do the evaluation

class MultiAry(Expression):
    """
    the mother of all binary or n-ary operators

    in order to be able to use this,
    child classes need to provide self.operation
    which is expected to be a 2-parameter function

    also they must provide a self.arg_checker
    a function that accepts the number of parameters
    as an argument, and returns a bool
    """
    def __init__(self, *children):
        nargs = len(children)
        classname = self.__class__.__name__
        if not self.arg_checker(nargs):
            raise TypeError(f"passing {nargs} arguments in {classname} is not supported")
        for child in children:
            self.check_is_expression(child)
        self.children = children

    def eval(self, env):
        # the try/except is just for making debugging easier
        try:
            left, right, *remaining = self.children
            result = self.operation(left.eval(env), right.eval(env))
            # for n-ary
            for other in remaining:
                result = self.operation(result, other.eval(env))
            return result
        except AttributeError:
            classname = self.__class__.__name__
            print(f"WARNING - class {classname} lacks the attribute 'operation'")


## we can now define the 2 big families
# using any of these 2 approaches
class Binary(MultiAry):
    @staticmethod
    def arg_checker(nargs):
        return nargs == 2

class Nary(MultiAry):
    arg_checker = lambda self, nargs: nargs >= 2



# and with all that in place the code for adding new operators becomes

class Integer(Atom):
    implementation_type = int

class Float(Atom):
    implementation_type = float


class Negative(Unary):
    operation = neg


# here too we can use several approaches to define the operation

class Plus(Nary):
    # a static method (no need for self then)
    @staticmethod
    def operation(x, y):
        return x + y

class Multiply(Nary):
    # a regular method, but then it needs to declare self
    # which is not needed
    def operation(self, x, y):
        return x * y


class Minus(Binary):
    # it could even be a lambda, but must take 3 args
    operation = lambda self, x, y: x - y

class Divide(Binary):
    # or pick from the operator module
    # and frankly it's kind of odd that this works,
    # because it takes 2 parameters !
    operation = truediv


# and the new guys

class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        """
        the value of a variable is stored in the environment
        """
        return env[self.name]


class Expressions(Expression):
    # make sure there is at least one expression
    def __init__(self, mandatory, *others):
        self.children = (mandatory, *others)
        for child in self.children:
            self.check_is_expression(child)

    def eval(self, env):
        """
        evaluate the whole suite, and return the result of the last one
        """
        for child in self.children:
            result = child.eval(env)
        return result


class Assignment(Expression):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
        self.check_is_expression(expr)

    def eval(self, env):
        """
        assigning means storing the new value in the environment
        """
        result = self.expr.eval(env)
        env[self.name] = result
        return result
