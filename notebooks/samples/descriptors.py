########### Example avec __getattr__ et __setattr__ ###############
class Temperature:
    """
    Une classe qui stocke et retourne une température automatiquement
    convertie en celcius ou en farhenheit on fonction de l'attribut
    utilisé

    On rappelle c = f*1.8 + 32 et f = (c-32)/1.8
    """

    def __init__(self):
        self.value = 0

    def __getattr__(self, name):
        if name == 'celsius':
            return self.value
        if name == 'fahrenheit':
            return self.value * 1.8 + 32
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'celsius':
            self.value = value
        elif name == 'fahrenheit':
            self.value = (value - 32) / 1.8
        else:
            object.__setattr__(self, name, value)


print(f"{'*' * 10}Example 1: __setattr__ {'*' * 10}")

t = Temperature()
t.celsius = 20
print(f"t.celsius: {t.celsius}")
print(f"t.fahrenheit: {t.fahrenheit}")


########### Example avec des descripteurs ###############
class Celsius:
    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("celsius")
        return instance.value

    def __set__(self, instance, value):
        instance.value = value


class Fahrenheit:
    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError("fahrenheit")
        return instance.value * 1.8 + 32

    def __set__(self, instance, value):
        instance.value = (value - 32) / 1.8


class TemperatureDesc:
    # On instancie les deux attributs de la classe
    celsius = Celsius()
    fahrenheit = Fahrenheit()

    def __init__(self):
        self.value = 0


print(f"{'*' * 10}Example 2: Descripteurs{'*' * 10}")

t = TemperatureDesc()
t.celsius = 20
print(f"t.celsius: {t.celsius}")
print(f"t.fahrenheit: {t.fahrenheit}")


########### Example avec des propriétés ###############

class TemperatureProp:
    def __init__(self):
        self.value = 0

    @property
    def celsius(self):
        return self.value

    @celsius.setter
    def celsius(self, value):
        self.value = value

    @property
    def fahrenheit(self):
        return self.value * 1.8 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.value = (value - 32) / 1.8


print(f"{'*' * 10}Example 3: propriétés{'*' * 10}")

t = TemperatureProp()
t.celsius = 20
print(f"t.celsius: {t.celsius}")
print(f"t.fahrenheit: {t.fahrenheit}")
