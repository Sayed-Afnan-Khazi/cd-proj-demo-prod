from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import or_
import os
import re
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import pandas as pd
import csv
import pandas as pd


load_dotenv()
app = Flask(__name__, template_folder='templates')

# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

bcrypt = Bcrypt(app)
# server_session=Session(app)
# db = SQLAlchemy(app)

# Flask Bcrypt
bcrypt = Bcrypt()

def validate_password(password):
    '''Password Validator:
    Conditions for password validation:
    Minimum 8 characters.
    The alphabet must be between [a-z]
    At least one alphabet should be of Upper Case [A-Z]
    At least 1 number or digit between [0-9].
    At least 1 character from [ _ or @ or $ ]. '''

    if len(password) < 8 or re.search("\s" , password):  
        return False  
    if not (re.search("[a-z]", password) and re.search("[A-Z]", password) and re.search("[0-9]", password) ):
        return False  
    return True  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/browse')
def browse():
    # Read the EVERY RECIPE CSV file
    data = pd.read_csv('../output-datasets/Filtered-Non_Gluten-IndianFoodRecipes.csv')

    # Fetching valid srno's from the CSV file
    sr_data = pd.read_csv('../output-datasets/RecipeOverviewV1.csv')
    srno_list = sr_data['Srno'].tolist()

    # Only displaying the data which is present in the RecipeOverviewV1.csv file
    recipes = []
    for index, row in data.iterrows():
        if row['Srno'] in srno_list:
            # Convert the data to a list of dictionaries
            recipes.append(row.to_dict())

    return render_template('browse.html', recipes=recipes)

@app.route('/recipe-details/<int:id>')
def recipe_details(id):
    data = pd.read_csv('../output-datasets/RecipeOverviewV1.csv')
    recipe = data[data['Srno'] == id].to_dict('records')
    if recipe:
        meta = pd.read_csv('../output-datasets/Filtered-Non_Gluten-IndianFoodRecipes.csv')
        meta_data = meta[meta['Srno'] == id].to_dict('records')

        detailed = pd.read_csv('../output-datasets/RecipeDetailedV1.csv')
        detailed_data = detailed[detailed['Srno'] == id].to_dict('records')
        return render_template('recipe.html', recipe=recipe[0], meta_data=meta_data[0], detailed_data=detailed_data[0])
    return "Recipe not found"

if __name__=='__main__':
    app.run(debug=True)