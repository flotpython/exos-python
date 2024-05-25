from functools import wraps
from inspect import signature
from time import time


def null(f):
    """
    Un decorateur qui annule l'appel d'une fonction
    """

    def wrapper(*args, **dargs):
        # __qualname__ returns the qualified name. So for a method
        # f in class C, it will return C.f
        print(f'Appel de {f.__qualname__} supprimé !')

    return wrapper


def timer(f):
    """
    un décorateur pour calculer le temps d'exécution d'une fonction.
    Implémentation avec une fonction (cloture)
    """

    def wrapper(*args, **kargs):
        start = time()
        res = f(*args, **kargs)
        print(f"{f.__qualname__} took {time() - start:.2f} seconds to complete")
        return res

    return wrapper


class Timer:
    """
    un décorateur pour calculer le temps d'exécution d'une fonction.
    Implémentation avec une classe
    """

    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        start = time()
        result = self.f(*args)
        print(f"{self.f.__qualname__} took {time() - start:.2f} seconds to complete")
        return result


def caller(func):
    """
    Un decorateur compte le nombre d'appels d'une fonction
    """

    @wraps(func)
    def wrapper(*args, **dwargs):
        wrapper.called = wrapper.called + 1
        print(f'calling function {func.__qualname__}, called {wrapper.called} times')
        return func(*args, **dwargs)

    wrapper.called = 0
    return wrapper


class ArgumentTypeError(Exception):
    """
    Exception raised when the type of the arguments of a function is not the one expected
    """
    pass


def validate_arg_type(_type):
    """
    un décorateur qui valide que le type de tous les arguments est de type _type. Si c'est la cas, appel la fonction
    décorée, sinon, affiche un message d'erreur.
    """

    def validate_type(f):
        def wrapper(*args, **kargs):
            for i in args:
                if type(i) is not _type:
                    raise ArgumentTypeError(f"{i} is not of type {_type}")
            for i in kargs.values():
                if type(i) is not _type:
                    raise ArgumentTypeError(f"{i} is not of type {_type}")
            return f(*args, **kargs)

        return wrapper

    return validate_type


@validate_arg_type(int)
def f(a, b):
    print(a, b)


f(b=1, a=2)


def memoize1(f):
    """
    Un décorateur pour cacher la valeur de retour d'une fonction en utilisant comme clef dans le cache
    les arguments passés (indice, on utilise repr((args, kwargs)))
    Lors d'un nouvel appel pour la même fonction et les mêmes argument, le décorateur va retourner le resultat caché.
    """
    cache = {}

    @wraps(f)
    def decorated(*args, **kwargs):
        # we take the repr to get a string to be sure to have an immutable
        key = repr((args, kwargs))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        else:
            print("cached result")
        return cache[key]

    return decorated


def memoize2(f):
    """
    Un décorateur pour cacher la valeur de retour d'une fonction en utilisant comme clef dans le cache
    les arguments passés. Lors d'un nouvel appel pour la même fonction et les mêmes argument,
    le décorateur va retourner le resultat caché.

    Le défaut de memoize1 est que le cache va considérer les appels df(1) et f(a=1) comme des appels différents pour
    la fonction définie par
    def f(a):
        pass

    Dans cette version, on va utiliser inspect.signature qui permet d'obtenir la signature d'une fonction,
    et inspect. Signature.bind qui permet de résoudre des arguments *args **kargs selon la signature de la fonction
    en retournant un objet inspect.BoundArguments. Finalement on peut extraire inspect.BoundArguments.args et
    inspect.BoundArguments.kargs qui sont les arguments correctement mappé à la signature de la fonction (donc l'ordre
    d'appel n'a plus d'importance).
    """
    cache = {}
    sig = signature(f)

    @wraps(f)
    def decorated(*args, **kwargs):
        bind = sig.bind(*args, **kwargs)
        key = repr((bind.args, bind.kwargs))
        if not key in cache:
            cache[key] = f(*args, **kwargs)
        else:
            print("cached result")
        return cache[key]

    return decorated


# example d'usage de null
@null
def unfinished_func(L):
    # do a super cool stuff on L not yet implemented
    MyNewClass.mega_filter(L)
    return L


unfinished_func(range(10))


class C:
    @null
    def f(self):
        pass


C().f()


# example d'usage de Timer
@Timer
def f_comp():
    return [x ** 2 for x in range(10000000)]


f_comp()


# example d'usage de timer de memoize2
@timer
@caller
@memoize2
def fib(n):
    a, b = 1, 1
    for i in range(n - 1):
        a, b = b, a + b
    return a


print(fib(10))
print(fib(4000))


@validate_arg_type(int)
def f(a, b):
    print(a, b)


f(b=1, a=2)
f(1, 2)
try:
    f(1, 'a')
except ArgumentTypeError as e:
    print(e.args)
#f(b='x', a='y')
