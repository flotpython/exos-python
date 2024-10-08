print(f"file {__file__} is obsolete, keeping it for the record only")
exit(0)

import parse_people

###

import pprint

S_FILENAMES = ["data-simple-03", "data-simple-10"]
L3 = parse_people.parse("data-simple-03")
L10 = parse_people.parse("data-simple-10")

G_FILENAMES = ["data-groups-10", "data-groups-120"]

print("PARSE a file")
NAMES = [name for name in dir(parse_people) if name.startswith("parse")]
for name in NAMES:
    fun = getattr(parse_people, name)
    for filename in S_FILENAMES:
        print(10*'-', f"{name}({filename}) ->")
        pprint.pprint(fun(filename))


print("INDEX the tuples")
NAMES = [name for name in dir(parse_people) if name.startswith("index")]
for name in NAMES:
    fun = getattr(parse_people, name)
    print(10*'-', f"{name}(L3) ->")
    pprint.pprint(fun(L3))


print("INITIAL index the tuples on the first's initial")
NAMES = [name for name in dir(parse_people) if name.startswith("initial")]
for name in NAMES:
    fun = getattr(parse_people, name)
    print(10*'-', f"{name}(L10) ->")
    pprint.pprint(fun(L10))


print("DATAFRAME from the tuples")
NAMES = [name for name in dir(parse_people) if name.startswith("dataframe")]
for name in NAMES:
    fun = getattr(parse_people, name)
    print(10*'-', f"{name}(L10) ->")
    pprint.pprint(fun(L10))


print("group_parse")
NAMES = [name for name in dir(parse_people) if name.startswith("group_parse")]
for name in NAMES:
    fun = getattr(parse_people, name)
    F = G_FILENAMES[0]
    print(10*'-', f"{name}({F}) ->")
    pprint.pprint(fun(F))


print("check_values")
NAMES = [name for name in dir(parse_people) if name.startswith("check_values")]
for name in NAMES:
    fun = getattr(parse_people, name)
    print(10*'-', f"{name}(L10) ->")
    pprint.pprint(fun(L10))
