from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import sys

app = Flask(__name__, template_folder='templates', static_folder='static')

app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DB'] = 'petFinder'

# Intialize MySQL
mysql = MySQL(app)

# ---- route function ---- #
''' Decorator which tells the 
    application which URL should call the 
    associated function '''

# HTTP methods GET and POST as argument in route decorator
@app.route("/", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    request1 = request.form
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)

    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)



@app.route('/pythonlogin/logout', methods=['GET', 'POST'])
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        if request.method == 'POST':
            if "Add Pet Listing" in request.form:
                return redirect(url_for('pets'))
            elif "Remove Pet Listing" in request.form:
                return redirect(url_for('removePets'))
            elif "Logout" in request.form:
                return redirect(url_for('logout'))
        else:
            # User is loggedin show them the home page
            return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/adopter", methods=['GET', 'POST'])
def adopter():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age = request.form['age']
        homeType = request.form['hometype']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = '{0}'".format(username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            cursor.execute("SELECT id FROM users WHERE username = '{0}'".format(username))
            id = cursor.fetchone()
            idnum = id['id']
            cursor.execute('INSERT INTO adopters VALUES (NULL, %s, %s, %s)', (int(age), homeType, idnum))
            mysql.connection.commit()
            return redirect(url_for('login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('adopter.html', msg=msg)

@app.route("/owner", methods=['GET', 'POST'])
def owner():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age = request.form['age']
        famsize = request.form['famsize']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = '{0}'".format(username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            cursor.execute("SELECT id FROM users WHERE username = '{0}'".format(username))
            id = cursor.fetchone()
            idnum = id['id']
            cursor.execute('INSERT INTO owners VALUES (NULL, %s, %s, %s)', (int(age), famsize, idnum))
            mysql.connection.commit()
            return redirect(url_for('home'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('owner.html', msg=msg)

@app.route("/pets", methods=['GET', 'POST'])
def pets():
    if 'loggedin' in session:
        if request.method == "POST" and 'name' in request.form and 'breed' in request.form and 'weight' in request.form:
            if request.method == "POST" and "View Listings" in request.form:
                return redirect(url_for('listings'))
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            animal = request.form['animal']
            name = request.form['name'];
            breed = request.form['breed'];
            weight = request.form['weight'];
            cursor.execute("SELECT ownerid FROM owners WHERE userid = '{0}'".format(session['id']))
            query = cursor.fetchone()
            ownerID = query['ownerid']
            ownerEmail = ""


            cursor.execute("SELECT email FROM users WHERE id = '{0}'".format(ownerID))
            owner = cursor.fetchone()
            ownerEmail = owner['email']

            cursor.execute('INSERT INTO pets VALUES (NULL, %s, %s, %s, %s, %s)', (animal, name, breed, weight, ownerID))
            mysql.connection.commit()
            return redirect(url_for('pets'))
    else:
        return redirect(url_for('login'))

    return render_template('pet.html')

@app.route("/removePets", methods=['GET', 'POST'])
def removePets():
    request1 = request.form.to_dict()
    if request1 and request.method == "POST":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        for checkbox in request1:
            petID = request1[checkbox]
            cursor.execute("DELETE FROM pets WHERE petid={}".format(petID))
            cursor.connection.commit()

    if 'loggedin' in session:
        userID = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT pets.* FROM pets\
                        WHERE pets.owner IN (SELECT owners.ownerid FROM owners\
                                             WHERE owners.userid IN (SELECT users.id FROM users\
                                                                     WHERE users.id = {}))".format(userID))
        pets = cursor.fetchall()

        # Counter for use in removePets.html
        i = 1
        for pet in pets:
            pet.update({'rowNum' : i})
            i += 1
        return render_template('removePets.html', pets=pets)

    else:
        return redirect(url_for('login'))

@app.route("/updatePets", methods=['GET', 'POST'])
def updatePets():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
@app.route("/listings", methods=['GET', 'POST'])
def listings():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT pets.pet, pets.name, pets.breed, pets.weight, users.username\
                    FROM pets\
                    INNER JOIN owners ON pets.owner = owners.ownerid\
                    INNER JOIN users ON owners.userid = users.id")
    pets = cursor.fetchall()

    return render_template('listings.html', pets=pets);

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT email FROM users WHERE username = '{0}'".format(session['username']))
    query = cursor.fetchone()
    email = query['email']
    cursor.execute("SELECT age FROM owners WHERE userid = '{0}'".format(session['id']))
    query = cursor.fetchone()
    if (cursor.rowcount > 0):
        age = query['age']
        cursor.execute("SELECT familysize FROM owners WHERE userid = '{0}'".format(session['id']))
        query = cursor.fetchone()
        size = query['familysize']
        return render_template('profile.html', username=session['username'], email=email, age=age, owner="Family Size", famsize=size)
    else:
        cursor.execute("SELECT age FROM adopters WHERE userid = '{0}'".format(session['id']))
        query = cursor.fetchone()
        age = query['age']
        cursor.execute("SELECT hometype FROM adopters WHERE userid = '{0}'".format(session['id']))
        query = cursor.fetchone()
        size = query['hometype']
        return render_template('profile.html', username=session['username'], email=email, age=age, owner="Home Type",
                               famsize=size)

@app.route("/profile/changeProfile", methods=['GET', 'POST'])
def changeProfile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT age FROM owners WHERE userid = '{0}'".format(session['id']))
    query = cursor.fetchone()
    if (cursor.rowcount > 0):
        age = query['age']
        cursor.execute("SELECT email FROM users WHERE id = '{0}'".format(session['id']))
        query = cursor.fetchone()
        email = query['email']
        cursor.execute("SELECT password FROM users WHERE id = '{0}'".format(session['id']))
        query = cursor.fetchone()
        password = query['password']
        cursor.execute("SELECT familysize FROM owners WHERE userid = '{0}'".format(session['id']))
        query = cursor.fetchone()
        size = query['familysize']

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            age = request.form['age']
            homeType = request.form['hometype']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE username = '{0}'".format(username))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute("UPDATE users SET username = '{0}', password = '{1}', email = '{2}' WHERE id = '{3}'".format(username, password, email, session['id']))
                mysql.connection.commit()
                cursor.execute("UPDATE owners SET age = '{0}', familysize = '{1}' WHERE userid = '{2}'".format(int(age), homeType, session['id']))
                mysql.connection.commit()
                return redirect(url_for('profile'))
    else:
        cursor.execute("SELECT email FROM users WHERE id = '{0}'".format(session['id']))
        query = cursor.fetchone()
        email = query['email']
        cursor.execute("SELECT password FROM users WHERE id = '{0}'".format(session['id']))
        query = cursor.fetchone()
        password = query['password']
        cursor.execute("SELECT age FROM adopters WHERE userid = '{0}'".format(session['id']))
        query = cursor.fetchone()
        age = query['age']
        cursor.execute("SELECT hometype FROM adopters WHERE userid = '{0}'".format(session['id']))
        query = cursor.fetchone()
        size = query['hometype']

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            age = request.form['age']
            size = request.form['hometype']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE username = '{0}'".format(username))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cursor.execute("UPDATE users SET username = '{0}', password = '{1}', email = '{2}' WHERE id = '{3}'".format(username, password, email, session['id']))
                mysql.connection.commit()
                cursor.execute("UPDATE adopters SET age = '{0}', hometype = '{1}' WHERE userid = '{2}'".format(int(age), size, session['id']))
                mysql.connection.commit()
                return redirect(url_for('profile'))

    return render_template('changeProfile.html', username=session['username'], password=password, email=email, age=age,
                               type=size)

# ---- run method ---- #
if __name__ == "__main__":
    app.run(debug=True)
