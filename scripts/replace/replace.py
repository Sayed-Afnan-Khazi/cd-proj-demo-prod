def replace_string(string, dictionary):
    for key, value in dictionary.items():
        string = string.replace(f"<td>{key}</td>", f"<td>{value}</td>")
    return string

# Example usage
with open("./web-app/templates/recipe.html", "r") as file:
    my_string = file.read()
my_dictionary = {
    "SUGAR.added": "Added sugar",
    "CA": "Calcium, Ca",
    "CHOCDF.net": "Carbohydrate (net)",
    "CHOCDF": "Carbohydrate, by difference",
    "CHOLE": "Cholesterol",
    "ENERC_KCAL": "Energy",
    "FAMS": "Fatty acids, total monounsaturated",
    "FAPU": "Fatty acids, total polyunsaturated",
    "FASAT": "Fatty acids, total saturated",
    "FATRN": "Fatty acids, total trans",
    "FIBTG": "Fiber, total dietary",
    "FOLDFE": "Folate, DFE",
    "FOLFD": "Folate, food",
    "FOLAC": "Folic acid",
    "FE": "Iron, Fe",
    "MG": "Magnesium",
    "NIA": "Niacin",
    "P": "Phosphorus, P",
    "K": "Potassium, K",
    "PROCNT": "Protein",
    "RIBF": "Riboflavin",
    "NA": "Sodium, Na",
    "Sugar.alcohol": "Sugar alcohols",
    "SUGAR": "Sugars, total",
    "THIA": "Thiamin",
    "FAT": "Total lipid (fat)",
    "VITA_RAE": "Vitamin A, RAE",
    "VITB12": "Vitamin B-12",
    "VITB6A": "Vitamin B-6",
    "VITC": "Vitamin C, total ascorbic acid",
    "VITD": "Vitamin D (D2 + D3)",
    "TOCPHA": "Vitamin E (alpha-tocopherol)",
    "VITK1": "Vitamin K (phylloquinone)",
    "WATER": "Water",
    "ZN": "Zinc, Zn"
}

print(len(my_dictionary))
result = replace_string(my_string, my_dictionary)
print(result)
with open("./recipe.html", "w") as file:
    file.write(result)
