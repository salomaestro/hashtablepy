import random
from hashtable import hashtable

names = ["Raymond", "Reka", "Richardt", "Rånny", "Turid", "Laila", \
         "Kenneth", "Pølsa", "Hjørdis", "Peder", "Finn-Åge", "Gjerdrun", \
         "Finnlugg", "Jesus Kristus"]
sexes = ["M", "F", "M", "M", "F", "F", "M", "M", "F", "M", "M", "F", "M", "F"]
ages = [random.randint(27, 63) for _ in range(len(names)-1)]; ages.append(2023)
people = [(name, age, sex) for name, age, sex in zip(names, ages, sexes)]

table = hashtable(len(names) - 5)

for name, age, sex in people:
    data = {"age": age, "sex": sex}
    table.insert(name, **data)

print(table)

print("Reka" in table) # Or use table.find("Reka") to get the data.
print(table.find("Jesus Kristus").values)

del table["Finn-Åge"] # or popped = table.remove("Finn-Åge")

print(table)

print(table["Turid"])

# print(table.keys())

# print(table.values())

# print(table.items())