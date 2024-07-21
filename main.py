import flask
import json
from pythonfile.user import User
from flask import render_template, request,url_for, session,jsonify,redirect,abort,flash
from datetime import datetime
import os
from werkzeug.utils import secure_filename 

app=flask.Flask("main")
app.secret_key='sohaila'
admin_emails = ['sohailaswedan45@gmail.com']
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size is 16 MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

#signup page routing
@app.route("/signup", methods=['POST','GET'])
def sign_up():
    validation_message = None
    session.pop('email', None)
    
    # Handle POST request when user submits sign-up form
    if request.method == "POST":
        # Retrieve data from the form
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        date = datetime.now().isoformat()
        role = 'admin' if email in admin_emails else 'user'
        
        # Add user to the database
        user_instance = User('users.json', email, date)
        error_message = user_instance.add_user(password, username , role)
        
        # If there's  error message, render the sign-up page with the error message
        if error_message:
            return render_template('signup.html', validation_message=error_message)
        # Clear the session
        session.clear()       
        # Redirect to the login page after successful sign-up
        return redirect(url_for('login'))
    return render_template('signup.html', validation_message=validation_message)

#deleteAccount
@app.route("/deleteAccount", methods=["POST", "GET"])
def deleteAccount():
    # Check if email exists in the session
    email = session.get('email')
    if email:
        # Delete user from the database
        User.delete_user()      
        # Remove email from the session
        session.pop('email', None)        
        # Clear the session
        session.clear()   
    return redirect(url_for('sign_up'))    

#routing to login page
@app.route("/", methods=["POST", "GET"])
def login():
    validation_message = None

    # If user is already logged in, go the home page
    if 'email' in session:
        return redirect(url_for('home'))

    # Handle login form submission
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Read user data from the JSON file
        with open('users.json', 'r') as infile:
            data = json.load(infile)

        # Check if the provided email and password match any user in the data
        for user in data:
            if user['email'] == email and int(user['password']) == int(password):
                # If match is found, set the email in the session and redirect to the home page
                session['email'] = email
      
                session['role'] = user['role']
                return redirect(url_for('home'))

        # If no match is found, display validation message
        validation_message = 'Invalid email or password. Please try again.'

    return render_template('login.html', validation_message=validation_message)

#routing to login page
@app.route("/home")
def home():
    # Check  user if not logged in redirect to the login page
    if 'email' not in session:
        return redirect('/')     
    else:
        # Read recipes data from the JSON file
        with open("movies.json", "r") as json_file:
            movies_data = json.load(json_file)      
            return render_template("index.html", movies= movies_data["movies"])
        
#moviesRoute
@app.route("/movies")
def movies():
    with open("movies.json", "r") as json_file:
        movies_info= json.load (json_file)
    return flask.render_template("index.html", movies=movies_info["movies"])
                
#deleteMovie function                
@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mov = None
    with open("movies.json", "r") as json_file:
        movies_info= json.load (json_file)
    # Iterate through the list of movies to find the one with the matching ID    
    for movie in movies_info["movies"]:
        if int(movie["id"]) == int(movie_id):    
            mov = movie
            break
        # Check if `mov` is still None, meaning no matching movie was found
        if not mov:
            return redirect(url_for('movies'))              
    movies_info["movies"].remove(mov)   
    with open("movies.json", "w") as json_file:
        json.dump(movies_info, json_file, indent=4)         
        return redirect(url_for('movies'))
    
# #adding movie
# @app.route('/add', methods=["GET", "POST"])
# def add_movie():
#     with open("movies.json", "r") as json_file:
#         movies_info= json.load (json_file)
#     if request.method == "GET":
#         return render_template("add.html")
#     if request.method == "POST":
#         # Retrieve form data
#         movie_id = request.form['id']
#         thumbnail = request.files['thumbnails']
#         moviename = request.form['moviename']
#         description = request.form['description']
#         rating = request.form['rating']
#         # Validation checks
#         if not movie_id or not thumbnail or not moviename or not description or not rating:
#             flash("All fields are required", "error")
#             return redirect(url_for('add_movie'))

#         try:
#             movie_id = int(movie_id)
#         except ValueError:
#             flash("Movie ID must be a number", "error")
#             return redirect(url_for('add_movie'))

#         try:
#             rating = int(rating)
#             if rating < 1 or rating > 4:
#                 raise ValueError
#         except ValueError:
#             flash("Rating must be a positive number from 1 to 4", "error")
#             return redirect(url_for('add_movie')) 
#          # Save the thumbnail image
#         if thumbnail:
#             filename = secure_filename(thumbnail.filename)
#             thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             thumbnail_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         else:
#             flash("Thumbnail upload failed", "error")
#             return redirect(url_for('add_movie'))  
#         # Create a new movie entry
#         new_movie = {
#             'id': movie_id,
#             'thumbnails': thumbnail_url,
#             'movie_name': moviename,
#             'brief_description': description,
#             'rating': rating
#         }
#          # Check for duplicate ID
#         if any(movie['id'] == new_movie['id'] for movie in movies_info['movies']):
#             flash("Movie with this ID already exists", "error")
#             return redirect(url_for('add_movie'))

#         # Add the new movie to the list
#         movies_info["movies"].append(new_movie)

#         # Write the updated list back to the file
#         with open("movies.json", "w") as movies_file:
#             json.dump(movies_info, movies_file, indent=4)

#         # Redirect to the home page
#         flash("Movie added successfully", "success")
#         return redirect(url_for('movies'))

#     return render_template('add.html')

@app.route('/add', methods=["GET", "POST"])
def add_movie():
    with open("movies.json", "r") as json_file:
        movies_info = json.load(json_file)

    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        # Retrieve form data
        movie_id = request.form['id']
        thumbnail = request.form['thumbnail']
        moviename = request.form['moviename']
        description = request.form['description']
        rating = request.form['rating']

        # Validation checks
        if not movie_id or not thumbnail or not moviename or not description or not rating:
            flash("All fields are required", "error")
            return redirect(url_for('add_movie'))

        try:
            movie_id = int(movie_id)
        except ValueError:
            flash("Movie ID must be a number", "error")
            return redirect(url_for('add_movie'))

        try:
            rating = int(rating)
            if rating < 1 or rating > 4:
                raise ValueError
        except ValueError:
            flash("Rating must be a positive number from 1 to 4", "error")
            return redirect(url_for('add_movie'))
        # Check for duplicate ID
        if any(int(movie['id']) == int(movie_id) for movie in movies_info['movies']):
            flash("Movie with this ID already exists", "error")
            return redirect(url_for('add_movie'))

        # Create a new movie entry
        new_movie = {
            'id': movie_id,
            'thumbnails': thumbnail,
            'movie_name': moviename,
            'brief_description': description,
            'rating': rating
        }
        # Add the new movie to the list
        movies_info["movies"].append(new_movie)

        # Write the updated list back to the file
        with open("movies.json", "w") as movies_file:
            json.dump(movies_info, movies_file, indent=4)

        # Redirect to the home page
        flash("Movie added successfully", "success")
        return redirect(url_for('movies'))

    return render_template('add.html')

#update movie
@app.route('/update/<movie_id>', methods=["GET", "POST"])
def update_movie(movie_id):
    with open("movies.json", "r") as json_file:
        movies_info = json.load(json_file)
    
    if request.method == "GET":
        # Render the update form without pre-filling data
        return render_template("update.html",movie_id = movie_id)
    
    elif request.method == "POST":
        with open("movies.json", "r") as json_file:
            movies_info = json.load(json_file)
        # Retrieve form data
        updated_thumbnail = request.form['thumbnail']
        updated_moviename = request.form['moviename']
        updated_description = request.form['description']
        updated_rating = float(request.form['rating'])
        
        # Find the movie to update
        movie_to_update = None
        for movie in movies_info["movies"]:
            if int(movie["id"]) == int(movie_id):
                movie_to_update = movie
                break
        
        # If movie is not found
        if not movie_to_update:
            return jsonify({"message": "Movie not found"}), 404
        
        # Update movie data
        movie_to_update['thumbnails'] = updated_thumbnail
        movie_to_update['movie_name'] = updated_moviename
        movie_to_update['brief_description'] = updated_description
        movie_to_update['rating'] = updated_rating
        
        # Save updated data to JSON file
        with open("movies.json", "w") as json_file:
            json.dump(movies_info, json_file, indent=4)
        return redirect(url_for('movies'))  
        
    return redirect(url_for('movies'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS