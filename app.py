from flask import Flask
from flask import render_template, request, redirect, url_for
from pymongo import *
import csv

app = Flask(__name__)

cluster = MongoClient("mongodb+srv://seyara22:seyara22@cluster0.bydksw5.mongodb.net/?retryWrites=true&w=majority")
database = cluster["Sdgp_Test"]
collection = database["career"]
collection_Signup = database["signUp"]
collection_program = database["program"]
collection_university = database["university"]

# Code to extract the data from csv and inserting to the collection
with open("Data_Files/Enterprising.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        data = {}
        for i in range(len(header)):
            data[header[i]] = row[i]
        collection.insert_one(data)

# Collection files
retrieve_career = collection.find()
retrieve_program = collection_program.find();
retrieve_university = collection_university.find();

# Whole list contains the mongo data
career_list = []
program_list = []
university_list = []

# Required list
interest_code_career = []
interest_code_program = []
interest_code_university = []

# Appending the whole list
for documents in retrieve_career:
    career_list.append(documents)

for documents in retrieve_program:
    program_list.append(documents)

for documents in retrieve_university:
    university_list.append(documents)


# Route for the home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('homePage.html')


# Route for the career finder model
@app.route('/careerFinderModel')
def careerFinderModel():
    return render_template('FinderModel.html')


# Route for the university finder page
@app.route('/universityFinder')
def universityFinder():
    return render_template('universityFinder.html')


# Route for the sign up page
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('SignUp.html')


# sign up page and mongo connecting
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    user = {
        'name': name,
        'email': email,
        'password': password
    }
    collection_Signup.insert_one(user)
    return render_template("OptionPage.html")


# Route for the login page
@app.route('/login', methods=['GET'])
def login():
    return render_template('Login.html')


# login page and mongo connecting
@app.route('/login', methods=['POST'])
def loginForm():
    # Get login data from form submission
    email = request.form['email']
    password = request.form['password']

    # Check if login data exists in MongoDB
    query = {"email": email, "password": password}
    document = collection_Signup.find_one(query)
    exists = document is not None

    if exists:
        print("Account already exits")
    else:
        print("Account not exits")

    return render_template("OptionPage.html")


# Route for the careerfinder page
@app.route('/careerFinder', methods=['GET'])
def careerFinder():
    return render_template('CareerFinder.html')


# Route for the program finder page
@app.route('/programFinder', methods=['GET'])
def programFinder():
    return render_template('ProgramFinder.html')


# sorting user's career appending on requried list
@app.route("/my-python-endpoint", methods=["POST"])
def my_python_endpoint():
    data = request.get_json()
    print("Data received from JavaScript:", data)
    stringData = data.upper()
    print(stringData)

    for i in career_list:
        for values in i.values():
            if values == stringData:
                interest_code_career.append(i)

    for i in interest_code_career:
        print(i, " for career")
    return "success"


# Sorting the user's programs and appending on required list
@app.route("/my-python-endpoint2", methods=["POST"])
def my_python_endpoint2():
    data = request.get_json()
    print("Data received from JavaScript:", data)
    stringData = data.upper()
    print(stringData)
    for i in program_list:
        for values in i.values():
            if values == stringData:
                interest_code_program.append(i)

    for i in interest_code_program:
        print(i, " for program")
    return "success"


# Showing data to the web page
@app.route("/career")
def career():
    print(interest_code_career)
    return render_template('CareerDisplay.html', interest_code_career=interest_code_career)


# Showing data to the web page
@app.route("/program")
def program():
    return render_template('programShow.html', interest_code_program=interest_code_program)


# 127.0.0.1 is the local machines IP address
# 5000 port is for TCP
# Running the server on debugging version
if __name__ == "__main__":
    app.run(debug=True)
