import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask.ext.uploads import UploadSet, configure_uploads
from mysqlconnection import connectToMySQL

from flask_bcrypt import Bcrypt

import re # import regex for email validation

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,
                         # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/')
def index():
    session['userlevel'] = ''
    return render_template('index.html')

@app.route('/register')
def register():

    return render_template('login.html')


@app.route('/process', methods=['POST'])
def process_login():
    is_valid = True
    # print('entered registratn post')
    # print(request.form)
    if len(request.form['firstname']) < 1:
        flash('First name must be longer than 1 letter')
        is_valid = False
        return redirect('/register')
    else:
        session['firstname'] = request.form['firstname']
    if len(request.form['lastname']) < 1:
        flash('Last name must be longer than 1 letter')
        is_valid = False
        return redirect('/register')
    else:
        session['lastname'] = request.form['lastname']

    if request.form['password'] == request.form['password_confirm']:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    else:
        flash('Passwords Do Not Match')
        return redirect('/register')

    if not EMAIL_REGEX.match(request.form['email']):
        flash('Email not in correct format!!')
        is_valid = False
        return redirect('/register')
    else:
        session['email'] = request.form['email']

        ('ELSE STATEMENT')

    mysql = connectToMySQL('pet_adoption')

    query = 'SELECT * FROM users WHERE email = %(em)s'
    data = {
        'em': request.form['email']
    }
    new_user_id = mysql.query_db(query, data)


    if len(new_user_id) > 0:
        return redirect('/')
        flash('This email has been taken')
        return redirect('/register')

    if is_valid:
        mysql = connectToMySQL('pet_adoption')

        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s);'
        data = {
            'fn': session['firstname'],
            'ln': session['lastname'],
            'em': session['email'],
            'pw': pw_hash
        }
        new_user_id = mysql.query_db(query, data)
        print('INSERT NEW ID =  ', new_user_id)
        session['userid'] = new_user_id
        print('session user id is ', session['userid'] )
        # print('INSERT NEW ID =  ', new_user_id['id'])

        return redirect('/pets')


@app.route('/success')
def display_success():

    return render_template('success.html')


@app.route('/login', methods=['POST'])
def login():
    print('entered login function')
    is_valid = True
    if not EMAIL_REGEX.match(request.form['login_email']):
        flash('Login email not in correct format!!')
        is_valid = False
        return redirect('/register')
    else:
        session['email'] = request.form['login_email']
    # if is_valid:
    #     print('success')

    mysql = connectToMySQL('pet_adoption')
    query = 'SELECT * FROM users WHERE email = %(em)s'
    data = {
        'em': session['email']
    }

    new_user_id = mysql.query_db(query, data)

    print('*'*80)
    print('new_user_id',new_user_id[0])
    print(new_user_id[0]['password'])
    if bcrypt.check_password_hash(new_user_id[0]['password'], request.form['login_password']):
        # if we get True after checking the password, we may put the user id in session
        print('Password Matches')

        session['firstname'] = new_user_id[0]['first_name']
        session['userid'] = new_user_id[0]['id']
        session['userlevel'] = new_user_id[0]['user_level']
        print('session level id is ', session['userlevel'] )

        print('session user id is ', session['userid'] )
        return redirect('/pets')
    else:
        # print('did not hit hash check')
        flash('Incorect email info.  Please check your email and password.')
        # return render_template('success.html')
        return redirect('/register')





@app.route('/pets', methods=['GET', 'POST'])
def pets():
    print('session level is ', session['userlevel'])
    mysql = connectToMySQL('pet_adoption') #call the function, passing in the name of our db
    users = mysql.query_db('select * from animals left join users on users.id = animals.user_id order by animals.id desc')   #call the query_db function, pass in the quyery as a string
    # print(users)
    return render_template('pets.html', pets=users)


@app.route('/add_pet')
def add_pet():

    return render_template('add_pet.html')



@app.route("/upload", methods=['POST'])
def upload():
    print('*'*80)
    target = os.path.join(APP_ROOT, 'static/images/')
    # target = os.path.join('/', '/images/')
    print('target ', target)
    print('*'*80)
    if not os.path.isdir(target):
        os.mkdir(target)

    # steven = request.form['file']
    # print('steven ', steven)

    for file in request.files.getlist('file'):
        print('&&&&&'*80)
        filename = file.filename
        print('filename ', filename)
        destination = "/".join([target, filename])
        print('destination ', destination)
        img_loc = 'static/images/'
        final_destination = "".join([img_loc,filename])
        print('final destination ', final_destination)
        file.save(destination)

    if len(request.form['firstname']) < 1:
        flash('First name must be longer than 1 letter')
        return redirect('/add_pet')
    else:
        first = request.form['firstname']
    if len(request.form['pettype']) < 1:
        flash('Type of pet must be longer than 1 letter')
        return redirect('/add_pet')
    else:
        type = request.form['pettype']
    if len(request.form['breed']) < 1:
        flash('Breed must be longer than 1 letter')
        return redirect('/add_pet')
    else:
        breed = request.form['breed']
    if len(request.form['color']) < 1:
        flash('Color name must be longer than 1 letter')
        return redirect('/add_pet')
    else:
        color = request.form['color']
    if len(request.form['location']) < 1:
        flash('Location name must be longer than 1 letter')
        return redirect('/add_pet')
    else:
        location = request.form['location']

    # print(first)
    # print(first)
    # print(first)
    # print(first)

    # type = request.form['pettype']
    # breed = request.form['breed']
    # color = request.form['color']



    mysql = connectToMySQL('pet_adoption')
    query = 'INSERT INTO animals (name, type, breed, color, location, file_name, file_location, user_id) VALUES (%(first)s, %(type)s, %(br)s, %(color)s, %(loc)s, %(fn)s,  %(tar)s, %(usid)s );'
    data = {
        'first': first,
        'type': type,
        'br': breed,
        'color': color,
        'loc': location,
        'fn': final_destination,
        'tar': target,
        'usid': session['userid']
    }
    new_pet = mysql.query_db(query, data)

    # return render_template("complete.html")
    return redirect('/pets')


@app.route('/show_pet/<id>')
def show_pet(id):

    mysql = connectToMySQL('pet_adoption')
    query = 'select * from animals left join users on users.id = animals.user_id where animals.id = ' + id
    show_pet = mysql.query_db(query)
    print('show pet ', show_pet)
    print('pet file name is ', show_pet[0]['file_name'])
    return render_template('show.html', pet=show_pet[0])


@app.route('/edit_pet/<id>')
def edit_pet(id):
    mysql = connectToMySQL('pet_adoption')
    query = 'select * from animals left join users on users.id = animals.user_id where animals.id = ' + id
    edit_pet = mysql.query_db(query)
    print('show pet ', edit_pet)
    print('pet file name is ', edit_pet[0]['file_name'])
    return render_template('edit_pet.html', pet=edit_pet[0])


@app.route('/update_pet/<id>', methods=['POST'])
def update_pet(id):

    if len(request.form['name']) <3:
        flash('Name must be longer than 3 characters')
        return redirect(f'/edit_pet/{id}')
        # return redirect('/success')
    if len(request.form['type']) <3:
        flash('Type must be longer than 3 characters')
        return redirect(f'/edit_pet/{id}')
    if len(request.form['breed']) <3:
        flash('Breed must be longer than 3 characters')
        return redirect(f'/edit_pet/{id}')
    if len(request.form['color']) <3:
        flash('Color must be longer than 3 characters')
        return redirect(f'/edit_pet/{id}')
    if len(request.form['location']) <3:
        flash('Location must be longer than 3 characters')
        return redirect(f'/edit_pet/{id}')

    mysql = connectToMySQL('pet_adoption')

    query = 'UPDATE animals SET name = %(name)s, type = %(type)s, breed = %(breed)s, color = %(color)s, location = %(loc)s where id = %(id)s'
    data = {
        'name': request.form['name'],
        'type': request.form['type'],
        'breed': request.form['breed'],
        'color': request.form['color'],
        'loc': request.form['location'],
        'id': id
    }
    one_job = mysql.query_db(query, data)


    return redirect('/pets')

@app.route('/pets/<id>/delete')
def delete_user(id):
    # print(session['new_user'])
    mysql = connectToMySQL('pet_adoption')
    query = 'DELETE FROM animals WHERE id = ' + id
    delete_user_id = mysql.query_db(query)

    return redirect('/pets')



# @app.route('/destroy_session', methods=['POST'])
@app.route('/destroy_session')
def delete_session():
    session.clear()
    # session.pop('visits') # delete visits
    return redirect('/')
    # return 'Sessions deleted'

if __name__ == "__main__":
    app.run(debug=True)
