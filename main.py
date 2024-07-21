import flask
import json
from pythonfile.user import User
from flask import render_template, request,url_for, session,jsonify,redirect,abort,flash
from datetime import datetime


app=flask.Flask("main")
app.secret_key='sohaila'
admin_emails = ['sohailaswedan45@gmail.com']

#logOut
@app.route("/logOut", methods=["POST", "GET"])
def exitAccount():
    # Check if email exists in the session
    email = session.get('email')
    if email:
        # Delete user from the database
        User.exit_user()      
        # Remove email from the session
        session.pop('email', None)        
        # Clear the session
        session.clear()   
    return redirect(url_for('login'))    

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

@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mov = None
    with open("movies.json", "r") as json_file:
        movies_info = json.load(json_file)
    
    # Iterate through the list of movies to find the one with the matching ID
    for movie in movies_info["movies"]:
        if int(movie["id"]) == int(movie_id):    
            mov = movie
            break

    # Check if `mov` is still None, meaning no matching movie was found
    if not mov:
        flash("Movie not found", "error")  # Optional: Display an error message
        return redirect(url_for('movies'))

    # Remove the movie from the list
    movies_info["movies"].remove(mov)   
    
    # Write the updated list back to the file
    with open("movies.json", "w") as json_file:
        json.dump(movies_info, json_file, indent=4)
    
    # Redirect to the movies page with a success message
    flash("Movie deleted successfully", "success")
    return redirect(url_for('movies'))

#addMovie
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

#updateMovie
@app.route('/update/<movie_id>', methods=["GET", "POST"])
def update_movie(movie_id):
    with open("movies.json", "r") as json_file:
        movies_info = json.load(json_file)

    if request.method == "GET":
        # Find the movie to update
        movie_to_update = None
        for movie in movies_info["movies"]:
            if int(movie["id"]) == int(movie_id):
                movie_to_update = movie
                break

        # If movie is not found
        if not movie_to_update:
            return jsonify({"message": "Movie not found"}), 404

        # Render the update form with pre-filled data
        return render_template("update.html", movie=movie_to_update)

    elif request.method == "POST":
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

        # Write the updated list back to the file
        with open("movies.json", "w") as movies_file:
            json.dump(movies_info, movies_file, indent=4)
           

        # Redirect to the home page or movies list
        return redirect(url_for('movies', success='true'))

    return render_template('update.html')
