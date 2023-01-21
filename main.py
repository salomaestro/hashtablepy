import random
from hashtable import Hashtable, Entry

names = ["Jonny", "Reka", "Richardt", "Rånny", "Turid", "Laila", \
         "Kenneth", "Pølsa", "Hjørdis", "Peder", "Finn-Åge", "Gjerdrun", \
         "Finnlugg", "Jesus Kristus"]
sexes = ["M", "F", "M", "M", "F", "F", "M", "M", "F", "M", "M", "F", "M", "F"]
ages = [random.randint(27, 63) for _ in range(len(names)-1)]; ages.append(2023)
people = [(name, age, sex) for name, age, sex in zip(names, ages, sexes)]

table = Hashtable(5)

for name, age, sex in people:
    data = {"age": age, "sex": sex}
    table.insert(name, **data)

print(table)

print(table.find("Reka"))
print(table.find("Jesus Kristus").values)

print(table.remove("Finn-Åge"))
print(table)