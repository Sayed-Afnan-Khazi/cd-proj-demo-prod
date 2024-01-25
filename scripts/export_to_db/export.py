from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

# Get the current directory
basedir = os.path.abspath(os.path.dirname(__file__))
# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db = SQLAlchemy(app)

class RecipeMeta(db.Model):
    __tablename__ = 'RecipeMeta'
    Metano = db.Column(db.Integer)
    Srno = db.Column(db.Integer, primary_key=True)
    RecipeName = db.Column(db.String)
    TranslatedRecipeName = db.Column(db.String)
    Ingredients = db.Column(db.String)
    TranslatedIngredients = db.Column(db.String)
    PrepTimeInMins = db.Column(db.Integer)
    CookTimeInMins = db.Column(db.Integer)
    TotalTimeInMins = db.Column(db.Integer)
    Servings = db.Column(db.Integer)
    Cuisine = db.Column(db.String)
    Course = db.Column(db.String)
    Diet = db.Column(db.String)
    Instructions = db.Column(db.String)
    TranslatedInstructions = db.Column(db.String)
    URL = db.Column(db.String)


class RecipeOverviewV1(db.Model):
    __tablename__ = 'RecipeOverviewV1'
    Srno = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String)
    yield_ = db.Column(db.Float)  # 'yield' is a reserved keyword in Python
    calories = db.Column(db.Float)
    totalCO2Emissions = db.Column(db.Float)
    co2EmissionsClass = db.Column(db.String)
    totalWeight = db.Column(db.Float)
    dietLabels = db.Column(db.String)
    healthLabels = db.Column(db.String)
    cautions = db.Column(db.String)
    cuisineType = db.Column(db.String)
    mealType = db.Column(db.String)
    dishType = db.Column(db.String)

class RecipeDetailedV1(db.Model):
    __tablename__ = 'RecipeDetailedV1'
    Srno = db.Column(db.Integer, db.ForeignKey('RecipeOverviewV1.Srno'), primary_key=True)
    ENERC_KCAL = db.Column(db.Float)
    ENERC_KCAL_perc = db.Column(db.Float)
    FAT = db.Column(db.Float)
    FAT_perc = db.Column(db.Float)
    FASAT = db.Column(db.Float)
    FASAT_perc = db.Column(db.Float)
    PROCNT = db.Column(db.Float)
    PROCNT_perc = db.Column(db.Float)
    CHOLE = db.Column(db.Float)
    CHOLE_perc = db.Column(db.Float)
    CHOCDF = db.Column(db.Float)
    CHOCDF_perc = db.Column(db.Float)
    FIBTG = db.Column(db.Float)
    FIBTG_perc = db.Column(db.Float)
    FATRN = db.Column(db.Float)
    FAMS = db.Column(db.Float)
    FAPU = db.Column(db.Float)
    SUGAR = db.Column(db.Float)
    CHOCDF_net = db.Column(db.Float)
    NA = db.Column(db.Float)
    NA_perc = db.Column(db.Float)
    CA = db.Column(db.Float)
    CA_perc = db.Column(db.Float)
    FE = db.Column(db.Float)
    FE_perc = db.Column(db.Float)
    ZN = db.Column(db.Float)
    ZN_perc = db.Column(db.Float)
    VITC = db.Column(db.Float)
    VITC_perc = db.Column(db.Float)
    THIA = db.Column(db.Float)
    THIA_perc = db.Column(db.Float)
    NIA = db.Column(db.Float)
    NIA_perc = db.Column(db.Float)
    VITB6A = db.Column(db.Float)
    VITB6A_perc = db.Column(db.Float)
    MG = db.Column(db.Float)
    MG_perc = db.Column(db.Float)
    K = db.Column(db.Float)
    K_perc = db.Column(db.Float)
    P = db.Column(db.Float)
    P_perc = db.Column(db.Float)
    VITA_RAE = db.Column(db.Float)
    VITA_RAE_perc = db.Column(db.Float)
    RIBF = db.Column(db.Float)
    RIBF_perc = db.Column(db.Float)
    FOLDFE = db.Column(db.Float)
    FOLDFE_perc = db.Column(db.Float)
    VITB12 = db.Column(db.Float)
    VITB12_perc = db.Column(db.Float)
    VITD = db.Column(db.Float)
    VITD_perc = db.Column(db.Float)
    TOCPHA = db.Column(db.Float)
    TOCPHA_perc = db.Column(db.Float)
    VITK1 = db.Column(db.Float)
    VITK1_perc = db.Column(db.Float)
    WATER = db.Column(db.Float)
    FOLFD = db.Column(db.Float)
    FOLAC = db.Column(db.Float)

with app.app_context():
    db.create_all()

def insert_data_from_csv(model, csv_file_path):
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        # print(row.to_dict())
        record = model(**row.to_dict())
        with app.app_context():
            db.session.add(record)
            print("Added a record")
            db.session.commit()
        

# insert_data_from_csv(RecipeOverviewV1, './datasets/RecipeOverviewV1.csv')
# insert_data_from_csv(RecipeDetailedV1, './datasets/RecipeDetailedV1.csv')
# insert_data_from_csv(RecipeMeta, '../../output-datasets/Filtered-Non_Gluten-IndianFoodRecipes.csv')

# Select first 5 from RecipeOverviewV1
# with app.app_context():
#     print(list(map(lambda x: x., RecipeOverviewV1.query.limit(5).all())))
