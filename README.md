# cd-proj

Repository for a research project on Celiac Diease. Creating diet plans and suggesting recipes for patients diagnosed with Celiac Disease.

## Datasets Used

- [Kaggle Dataset](https://www.kaggle.com/datasets/kanishk307/6000-indian-food-recipes-dataset): IndianFoodDataset for Indian Food Recipes.
- [IFCT Dataset](https://github.com/ifct2017/compositions/tree/master/assets): Detailed nutrient composition of 528 key foods in India.
- [Celiac Disease Foundation](https://celiac.org/gluten-free-living/what-is-gluten/sources-of-gluten/): List of ingredients that contain Gluten.

## Procedure

### Part-1

- We first sorted through the IFCT dataset, renaming, and grouping the tables according to similar compositional properties in the working notebook `dev/dev.ipynb`.
- These new tables are stored into the `ifct-compositions-assets-renamed` subdirectory. Example: All elemental contents such as Al,As,Cd,Ca,Cr,Co,Cu,Fe,Pb,Li are grouped into a single table.
- All the tables have also been merged in the working notebook as `table_merged_master`.

### Part-2

- We then started working on removing gluten containing recipes in the working notebook `IndianFoodDataset/filtering.ipynb`.
- This was done by collecting a list of popular gluten containing ingredients from [The Celiac Disease Foundation](https://celiac.org/gluten-free-living/what-is-gluten/sources-of-gluten/), and comparing them with the list of ingredients present for each row/recipe in the `IndianFoodDataset`.
- If a row/recipe contained any gluten containing item from our list, it was discarded.
- In this process, we were able to **eliminate 2359 recipes** that contained gluten containing ingredients and **preserved 4512 gluten-free recipes**.
- These gluten-free recipes are stored in `IndianFoodDataset/FilteredIndianFoodRecipes.csv`.
