def replace_string(string, dictionary):
    for key, value in dictionary.items():
        string = string.replace("<td>{{ recipe."+f"{key}"+" }}</td>", "<td>{{ recipe."+f"{key}"+" }}"+f" {value}"+"</td>")
    return string

# Example usage
with open("./recipe.html", "r") as file:
    my_string = file.read()

my_dictionary = {
    "SUGAR.added": "g",
    "CA": "mg",
    "CHOCDF.net": "g",
    "CHOCDF": "g",
    "CHOLE": "mg",
    "ENERC_KCAL": "kcal",
    "FAMS": "g",
    "FAPU": "g",
    "FASAT": "g",
    "FATRN": "g",
    "FIBTG": "g",
    "FOLDFE": "µg",
    "FOLFD": "µg",
    "FOLAC": "µg",
    "FE": "mg",
    "MG": "mg",
    "NIA": "mg",
    "P": "mg",
    "K": "mg",
    "PROCNT": "g",
    "RIBF": "mg",
    "NA": "mg",
    "Sugar.alcohol": "g",
    "SUGAR": "g",
    "THIA": "mg",
    "FAT": "g",
    "VITA_RAE": "µg",
    "VITB12": "µg",
    "VITB6A": "mg",
    "VITC": "mg",
    "VITD": "µg",
    "TOCPHA": "mg",
    "VITK1": "µg",
    "WATER": "g",
    "ZN": "mg"
}

print(len(my_dictionary))
result = replace_string(my_string, my_dictionary)
# print(result)
with open("./recipe.html", "w") as file:
    file.write(result)