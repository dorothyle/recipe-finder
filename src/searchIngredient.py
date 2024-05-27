from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv
import psycopg2

app = Flask(__name__)
CORS(app, origins="*")
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

endpoint = os.environ.get("HOST")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
database_name = os.environ.get("DB_NAME")

@app.route('/')
def home():
    return {"host": host}

@app.route('/ingredient', methods=["GET"])
def getIngredient():
    # ingredient = request.json["ingredient"]
    ingredient = "pea"

    try:
        print("trying to make connection")
        connection = psycopg2.connect(database=database_name,
                                    user=username,
                                    host=endpoint,
                                    password=password)
        print("Database connected successfully")

        cursor = connection.cursor()
        print("making query")
        command = """
        SELECT DISTINCT LOWER(ingredients_name) AS ingredients_name, 
            LENGTH(ingredients_name) - LENGTH(REPLACE(LOWER(ingredients_name), '""" + ingredient + """', '')) AS occurrences,
            LENGTH(ingredients_name) AS ingredient_length
        FROM (
            SELECT unnest(NER) AS ingredients_name
            FROM recipes_table
        ) AS expanded_ingredients
        WHERE LOWER(ingredients_name) ILIKE '%""" + ingredient + """%'
        ORDER BY occurrences DESC, ingredient_length ASC
        LIMIT 10;
        """
        print("query completed")
        cursor.execute(command)

        rows = cursor.fetchall()
        matches = []

        for row in rows:
            matches.append(row[0])
            print(row[0])
        return {"matches": str(matches)}

    except:
        print("Database not connected successfully")
        return {"message":"ERROR"}

    return {"message": "end of function"}

if __name__ == '__main__':
    app.run(debug=True)