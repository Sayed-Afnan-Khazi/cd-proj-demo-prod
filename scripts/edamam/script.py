# Script to fetch details of recipes through the Edamam API. Made by Sayed-Afnan-Khazi.

# TO RUN THIS SCRIPT:
# 1. pip install -r requirements.txt
# 2. Create a .env file in the same directory 
# 3. Create an output-datasets folder in the same directory
# 4. Store Filtered-Non_Gluten-IndianFoodRecipes.csv in the output-datasets folder
# 5. Run this script

import pandas as pd
import os
import time
import requests
from datetime import datetime
# import json

from dotenv import load_dotenv

load_dotenv()


############## EMAIL SETUP ##############

import smtplib, ssl
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get("GMAIL_ADDRESS")  
receiver_email = os.environ.get("NOTIFY_ADDRESS")  # Enter receiver address
password = os.environ.get("GMAIL_PASSWORD")
context = ssl.create_default_context()

log_message = ""

def send_email(message,subject):
    # Formatting the message
    message = f"""\
Subject: {subject}

{message}
"""
    print("Sending Notify Email(s)")
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print("Notify Email(s) successfully sent.")

########################################


filteredRecipes = pd.read_csv('../../output-datasets/Filtered-Non_Gluten-IndianFoodRecipes.csv')

key_set = 1 # 1 for first set of keys, 2 for second set of keys

# Getting the APP_ID and APP_KEY from the environment variables
EDAMAM_APP_ID = os.environ.get(f'EDAMAM_APP_ID_{key_set}')
EDAMAM_APP_KEY = os.environ.get(f'EDAMAM_APP_KEY_{key_set}')


# Dataframes
recipeOverview = pd.DataFrame(columns=['Srno',
                                       'uri',
                                       'yield',
                                       'calories',
                                       'totalCO2Emissions',
                                       'co2EmissionsClass',
                                       'totalWeight',
                                       'dietLabels',
                                       'healthLabels',
                                       'cautions',
                                       'cuisineType',
                                       'mealType',
                                       'dishType'
                                       ])

recipeDetailed = pd.DataFrame(columns=['SrNo', 'ENERC_KCAL', 'ENERC_KCAL%', 'FAT', 'FAT%', 'FASAT', 'FASAT%', 'PROCNT', 'PROCNT%', 'CHOLE', 'CHOLE%', 'CHOCDF', 'CHOCDF%', 'FIBTG', 'FIBTG%', 'FATRN', 'FAMS', 'FAPU', 'SUGAR', 'CHOCDF.net', 'NA', 'NA%', 'CA', 'CA%', 'FE', 'FE%', 'ZN', 'ZN%', 'VITC', 'VITC%', 'THIA', 'THIA%', 'NIA', 'NIA%', 'VITB6A', 'VITB6A%', 'MG', 'MG%', 'K', 'K%', 'P', 'P%', 'VITA_RAE', 'VITA_RAE%', 'RIBF', 'RIBF%', 'FOLDFE', 'FOLDFE%', 'VITB12', 'VITB12%', 'VITD', 'VITD%', 'TOCPHA', 'TOCPHA%', 'VITK1', 'VITK1%', 'WATER', 'FOLFD', 'FOLAC'])


count = 0
error_count=0
good_count=0

erroneousRecipes = {}

try:
    for recipe in zip(filteredRecipes['Srno'],filteredRecipes['TranslatedRecipeName'],filteredRecipes['Ingredients'],filteredRecipes['TranslatedIngredients']):
        ingredientsList = str(recipe[3]).split(",")
        url = f"https://api.edamam.com/api/nutrition-details?app_id={EDAMAM_APP_ID}&app_key={EDAMAM_APP_KEY}"
        headers = {"Content-Type": "application/json"}

        body = {
            "ingr": ingredientsList
        }

        response = requests.post(url, headers=headers, json=body)

        response_dict = response.json()

        ## Viewing the data - Uncomment the import json statement at the top level
        # prettified_json = json.dumps(response_dict, indent=4)
        # print(prettified_json)

        if 'totalNutrients' in response_dict: 
            good_count+=1

            ## Adding data to the dataframes

            # Sometimes a NaN appeared in totalCO2Emissions that didn't come with a cO2EmissionsClass
            if response_dict['totalCO2Emissions'] == 'NaN':
                response_dict['co2EmissionsClass'] = 'NaN'
            
            # create a dictionary to store the recipe overview data
            recipe_overview_dict = {'Srno': recipe[0], 'uri': response_dict['uri'], 'yield': response_dict['yield'], 'calories': response_dict['calories'], 'totalCO2Emissions': response_dict['totalCO2Emissions'], 'co2EmissionsClass': response_dict['co2EmissionsClass'], 'totalWeight': response_dict['totalWeight'], 'dietLabels': ','.join(response_dict['dietLabels']), 'healthLabels': ','.join(response_dict['healthLabels']), 'cautions': ','.join(response_dict['cautions']),'cuisineType': ','.join(response_dict['cuisineType']), 'mealType': ','.join(response_dict['mealType']), 'dishType': ','.join(response_dict['dishType'])}
            # create a dictionary to store the recipe detailed data
            recipe_detailed_dict = {'SrNo': recipe[0], 'ENERC_KCAL': response_dict['totalNutrients']['ENERC_KCAL']['quantity'], 'ENERC_KCAL%': response_dict['totalDaily']['ENERC_KCAL']['quantity'], 'FAT': response_dict['totalNutrients']['FAT']['quantity'], 'FAT%': response_dict['totalDaily']['FAT']['quantity'], 'FASAT': response_dict['totalNutrients']['FASAT']['quantity'], 'FASAT%': response_dict['totalDaily']['FASAT']['quantity'], 'PROCNT': response_dict['totalNutrients']['PROCNT']['quantity'], 'PROCNT%': response_dict['totalDaily']['PROCNT']['quantity'], 'CHOLE': response_dict['totalNutrients']['CHOLE']['quantity'], 'CHOLE%': response_dict['totalDaily']['CHOLE']['quantity'], 'CHOCDF': response_dict['totalNutrients']['CHOCDF']['quantity'], 'CHOCDF%': response_dict['totalDaily']['CHOCDF']['quantity'], 'FIBTG': response_dict['totalNutrients']['FIBTG']['quantity'], 'FIBTG%': response_dict['totalDaily']['FIBTG']['quantity'], 'FATRN': response_dict['totalNutrients']['FATRN']['quantity'], 'FAMS': response_dict['totalNutrients']['FAMS']['quantity'], 'FAPU': response_dict['totalNutrients']['FAPU']['quantity'], 'SUGAR': response_dict['totalNutrients']['SUGAR']['quantity'], 'CHOCDF.net': response_dict['totalNutrients']['CHOCDF.net']['quantity'], 'NA': response_dict['totalNutrients']['NA']['quantity'], 'NA%': response_dict['totalDaily']['NA']['quantity'], 'CA': response_dict['totalNutrients']['CA']['quantity'], 'CA%': response_dict['totalDaily']['CA']['quantity'], 'FE': response_dict['totalNutrients']['FE']['quantity'], 'FE%': response_dict['totalDaily']['FE']['quantity'], 'ZN': response_dict['totalNutrients']['ZN']['quantity'], 'ZN%': response_dict['totalDaily']['ZN']['quantity'], 'VITC': response_dict['totalNutrients']['VITC']['quantity'], 'VITC%': response_dict['totalDaily']['VITC']['quantity'], 'THIA': response_dict['totalNutrients']['THIA']['quantity'], 'THIA%': response_dict['totalDaily']['THIA']['quantity'], 'NIA': response_dict['totalNutrients']['NIA']['quantity'], 'NIA%': response_dict['totalDaily']['NIA']['quantity'], 'VITB6A': response_dict['totalNutrients']['VITB6A']['quantity'], 'VITB6A%': response_dict['totalDaily']['VITB6A']['quantity'], 'MG': response_dict['totalNutrients']['MG']['quantity'], 'MG%': response_dict['totalDaily']['MG']['quantity'], 'K': response_dict['totalNutrients']['K']['quantity'], 'K%': response_dict['totalDaily']['K']['quantity'], 'P': response_dict['totalNutrients']['P']['quantity'], 'P%': response_dict['totalDaily']['P']['quantity'], 'VITA_RAE': response_dict['totalNutrients']['VITA_RAE']['quantity'], 'VITA_RAE%': response_dict['totalDaily']['VITA_RAE']['quantity'], 'RIBF': response_dict['totalNutrients']['RIBF']['quantity'], 'RIBF%': response_dict['totalDaily']['RIBF']['quantity'], 'FOLDFE': response_dict['totalNutrients']['FOLDFE']['quantity'], 'FOLDFE%': response_dict['totalDaily']['FOLDFE']['quantity'], 'VITB12': response_dict['totalNutrients']['VITB12']['quantity'], 'VITB12%': response_dict['totalDaily']['VITB12']['quantity'], 'VITD': response_dict['totalNutrients']['VITD']['quantity'], 'VITD%': response_dict['totalDaily']['VITD']['quantity'], 'TOCPHA': response_dict['totalNutrients']['TOCPHA']['quantity'], 'TOCPHA%': response_dict['totalDaily']['TOCPHA']['quantity'], 'VITK1': response_dict['totalNutrients']['VITK1']['quantity'], 'VITK1%': response_dict['totalDaily']['VITK1']['quantity'], 'WATER': response_dict['totalNutrients']['WATER']['quantity'], 'FOLFD': response_dict['totalNutrients']['FOLFD']['quantity'], 'FOLAC': response_dict['totalNutrients']['FOLAC']['quantity']}
            # append the recipe overview data to the dataframe
            recipeOverview = pd.concat([recipeOverview, pd.DataFrame(recipe_overview_dict, index=[0])], ignore_index=True)
            # append the recipe detailed data to the dataframe
            recipeDetailed = pd.concat([recipeDetailed, pd.DataFrame(recipe_detailed_dict, index=[0])], ignore_index=True)
        
            # Printing a GOOD message
            print(f"#{count} \033[92m GOOD {response_dict['totalNutrients']['ENERC_KCAL']['quantity']} \033[00m")
            log_message += f'''{datetime.now()} #{count} GOOD {response_dict['totalNutrients']['ENERC_KCAL']['quantity']}
'''
        else:
            error_count+=1
            print(f"#{count} \033[91m ERROR! \033[00m",response_dict,"HTTP Error Code:",response.status_code,"Recipe Srno:",recipe[0])
            log_message += f'''{datetime.now()} #{count} ERROR! {response_dict} HTTP Error Code: {response.status_code} Recipe Srno: {recipe[0]}
'''
            erroneousRecipes[recipe[0]] = response_dict

        count+=1

        # Waiting for 60 seconds after every 10 requests
        if count%10==0:
            print("\033[93m Waiting for 60 seconds \033[00m")

            print("Saving current results to CSV files")
            log_message += f'''{datetime.now()} Saving current results to CSV files
'''
            recipeOverview.to_csv('../../output-datasets/RecipeOverview.csv', index=False)
            recipeDetailed.to_csv('../../output-datasets/RecipeDetailed.csv', index=False)
            
            time.sleep(60)

        # Switching API keys
        # Switching on 385 instead of 400 for caution
        if count%385 == 0:
            key_set += 1
            EDAMAM_APP_ID = os.environ.get(f'EDAMAM_APP_ID_{key_set}')
            EDAMAM_APP_KEY = os.environ.get(f'EDAMAM_APP_KEY_{key_set}')
            if not EDAMAM_APP_ID or not EDAMAM_APP_KEY:
                print("No more keys available. Stopping the script.")
                log_message += f'''{datetime.now()} No more keys available. Stopping the script.
'''
                print("Saving current results to CSV files")
                recipeOverview.to_csv('../../output-datasets/RecipeOverview.csv', index=False)
                recipeDetailed.to_csv('../../output-datasets/RecipeDetailed.csv', index=False)
                send_email(log_message,subject="SCRIPT STOPPED DUE TO EXHAUSTION OF KEYS!")
                break
            print("*"*50,"Switching to key set",key_set,"*"*50)
            log_message += f'''{datetime.now()} {'*'*50} Switching to key set {key_set} {'*'*50}
'''

        if good_count%1000 == 0:
            print("Saving current results to CSV files")
            recipeOverview.to_csv('../../output-datasets/RecipeOverview.csv', index=False)
            recipeDetailed.to_csv('../../output-datasets/RecipeDetailed.csv', index=False)

            print("*"*50,"1000 GOOD RECIPES REACHED!","*"*50)
            print("FINAL STATISTICS:")
            print("COUNT:",count)
            print("GOOD COUNT:",good_count)
            print("ERROR COUNT:",error_count)
            print("YIELD (good/total)% :",(good_count/count)*100)
            print("List of erroneous recipes' srno:",erroneousRecipes)
            log_message += f'''{datetime.now()} {'*'*50} 1000 GOOD RECIPES REACHED! {'*'*50}
'''
            log_message += f'''{datetime.now()} FINAL STATISTICS:\nCOUNT: {count}\nGOOD COUNT: {good_count}\nERROR COUNT: {error_count}\nYIELD (good/total)% : {(good_count/count)*100}\nList of erroneous recipes' srno: {erroneousRecipes}
'''
            send_email(log_message,subject="SCRIPT SUCCESS!")
            break

except KeyboardInterrupt:
    print("A keyboard interrupt stopped the script.")
    print("Saving current results to CSV files")
    recipeOverview.to_csv('../../output-datasets/RecipeOverview.csv', index=False)
    recipeDetailed.to_csv('../../output-datasets/RecipeDetailed.csv', index=False)
    print("FINAL STATISTICS:")
    print("COUNT:",count)
    print("GOOD COUNT:",good_count)
    print("ERROR COUNT:",error_count)
    print("YIELD (good/total)% :",(good_count/count)*100)
    print("List of erroneous recipes' srno:",erroneousRecipes)
    log_message += f'''{datetime.now()} A keyboard interrupt stopped the script.
'''
    log_message += f'''FINAL STATISTICS:\nCOUNT: {count}\nGOOD COUNT: {good_count}\nERROR COUNT: {error_count}\nYIELD (good/total)% : {(good_count/count)*100}\nList of erroneous recipes' srno: {erroneousRecipes}
'''
    send_email(log_message,subject="SCRIPT STOPPED BY KEYBOARD INTERRUPT!")

except Exception as e:
    print("Saving current results to CSV files")
    recipeOverview.to_csv('../../output-datasets/RecipeOverview.csv', index=False)
    recipeDetailed.to_csv('output-datasets/RecipeDetailed.csv', index=False)

    print("*"*50,"RUNTIME ERROR OCCURED!","*"*50)
    print("ERROR:",e)
    print("FINAL STATISTICS:")
    print("COUNT:",count)
    print("GOOD COUNT:",good_count)
    print("ERROR COUNT:",error_count)
    print("YIELD (good/total)% :",(good_count/count)*100)
    print("List of erroneous recipes' srno:",erroneousRecipes)
    log_message += f'''{datetime.now()} {'*'*50} A RUNTIME ERROR OCCURED! {'*'*50}
'''
    log_message += f'''ERROR: {e}\n
'''
    log_message += f'''FINAL STATISTICS:\nCOUNT: {count}\nGOOD COUNT: {good_count}\nERROR COUNT: {error_count}\nYIELD (good/total)% : {(good_count/count)*100}\nList of erroneous recipes' srno: {erroneousRecipes}
'''
    send_email(log_message,subject="SCRIPT ERROR!")
