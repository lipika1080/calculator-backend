from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Connect to Azure Cosmos DB (MongoDB API)
MONGO_URI = ("mongodb://calculatordb:XheAHNWsMoTOh1kcOYYYC4cxVU4ZdzgO8Yr0srzS41N6KfWONedWuNYa57si4rHMLqyC1jOocVSTACDbh5AlVw==@calculatordb.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@calculatordb@")
client = MongoClient(MONGO_URI)
db = client["calculator"]
calculations_collection = db["calculations"]

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    operation = data.get("operation")
    numbers = data.get("numbers")

    if not numbers or not isinstance(numbers, list):
        return jsonify({"error": "Numbers must be a list"}), 400

    if operation not in ["add", "subtract", "multiply", "divide"]:
        return jsonify({"error": "Invalid operation"}), 400

    try:
        if operation == "add":
            result = sum(numbers)
        elif operation == "subtract":
            result = numbers[0] - sum(numbers[1:])
        elif operation == "multiply":
            result = 1
            for num in numbers:
                result *= num
        elif operation == "divide":
            result = numbers[0]
            for num in numbers[1:]:
                result /= num

        # Save the calculation in the database
        calc_data = {"operation": operation, "numbers": numbers, "result": result}
        calculations_collection.insert_one(calc_data)

        return jsonify({"operation": operation, "numbers": numbers, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
