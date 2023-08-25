# cd-proj

Repository for a research project on Celiac Diease. Creating diet plans and suggesting recipes for patients diagnosed with Celiac Disease.

## Datasets Used

- Note: The following datasets are stored in the subdirectory `input-datasets`.
- [Kaggle Dataset](https://www.kaggle.com/datasets/kanishk307/6000-indian-food-recipes-dataset): IndianFoodDataset for Indian Food Recipes.
- [IFCT Dataset](https://github.com/ifct2017/compositions/tree/master/assets): Detailed nutrient composition of 528 key foods in India.
- [Celiac Disease Foundation](https://celiac.org/gluten-free-living/what-is-gluten/sources-of-gluten/): List of ingredients that contain Gluten.

## Procedure

### Part-1

- We first sorted through the IFCT dataset, renaming, and grouping the tables according to similar compositional properties in the working notebook `dev.ipynb`.
- These new tables are stored into the `input-datasets/ifct-compositions-assets-renamed` subdirectory. Example: All elemental contents such as Al,As,Cd,Ca,Cr,Co,Cu,Fe,Pb,Li are grouped into a single table.
- All the tables have also been merged in the working notebook as `table_merged_master`.

### Part-2

- We then started working on removing gluten containing recipes in the same working notebook `dev.ipynb`.
- This was done by collecting a list of popular gluten containing ingredients from [The Celiac Disease Foundation](https://celiac.org/gluten-free-living/what-is-gluten/sources-of-gluten/), and comparing them with the list of ingredients present for each row/recipe in the `IndianFoodDataset` (`input-datasets/IndianFoodDataset/IndianFoodDatasetCSV.csv`).
- If a row/recipe contained any gluten containing item from the list, it was discarded.
- In this process, we were able to **eliminate 2359 recipes** that contained gluten containing ingredients and **preserved 4512 gluten-free recipes**.
- These gluten-free recipes are stored in `output-datasets/Filtered-Non_Gluten-IndianFoodRecipes.csv`.
- The eliminated gluten containing recipes are stored in `output-datasets/Gluten-IndianFoodRecipes.csv`.

### Part-3: The Re-haul

- The Problem: We have over 8000 recipes, with over 800 unique ingredients and many more unique measuring quantities. We need to find a way to group these ingredients together, and standardize/convert the measuring quantities.

- Approaching the Solution: We looked into OpenAI's GPT-4, a state-of-the-art (Generative Pretrained Transformer) language model that can be used to generate text. Since GPT-4 has been trained on the knowledge of the internet, it should theoretically be able to automatically convert the ingredients and quantities into a standardized format, and use its knowledge database to find the nutritional contents of each recipe by adding the nutritional contents of all ingredients in that recipe. Upon further research, we found out that this would be expensive, since per call usage of the GPT-4 API is charged at $0.06 per 1000 input tokens. Each recipe is about 90-100 tokens based on the [OpenAI Tokeniser Tool](https://platform.openai.com/tokenizer). We would need to make 8000 (recipe) calls to the API, which would be about 800000 input tokens and would cost us $48000. This estimate does not consider the output tokens cost which is about $0.12 per 1000 tokens. This would be a very expensive solution.

- Moreover, using GPT-3.5, we compared a few sample recipes and found that the output was not very accurate.

- More research led us to [Edamam's Nutrition Analysis API](https://developer.edamam.com/edamam-nutrition-api). This API uses Natural Language Processing along with their database to find the nutritional contents of a recipe by sending a list of all ingredients in that recipe. The free developer edition allows us to look up 400 recipes/month at 10 recipes/minute, and the Enterprise edition allows us to look up 50,000 recipes/month at 150/minute for $69/month (We would only need one month since we only have 8000 recipes). This is a much more cost effective solution.
