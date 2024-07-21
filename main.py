import flask
import json
from pythonfile.user import User
from flask import render_template, request,url_for, session,jsonify,redirect,abort,flash
from datetime import datetime 

app=flask.Flask("main")
app.secret_key='sohaila'
admin_emails = ['sohailaswedan45@gmail.com']





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
        

                

@app.route("/movies")
def movies():
    with open("movies.json", "r") as json_file:
        movies_info= json.load (json_file)


    return flask.render_template("index.html", movies=movies_info["movies"])
                

@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mov = None
    with open("movies.json", "r") as json_file:
        movies_info= json.load (json_file)
    for movie in movies_info["movies"]:
        if int(movie["id"]) == int(movie_id):    
            mov = movie
            break
        if not mov:
            return redirect(url_for('movies'))
                    # return jsonify({"success": False, "message": "Failed to remove the movie"}), 404
                
    movies_info["movies"].remove(mov)   
    with open("movies.json", "w") as json_file:
        json.dump(movies_info, json_file, indent=4)
                
        return redirect(url_for('movies'))


@app.route('/add', methods=["GET", "POST"])
def add_movie():
    with open("movies.json", "r") as json_file:
        movies_info= json.load (json_file)
    if request.method == "GET":
        return render_template("add.html")
    if request.method == "POST":
        # Retrieve form data
        movie_id = request.form['id']
        thumbnail = request.form['thumbnail']
        moviename = request.form['moviename']
        description = request.form['description']
        rating = request.form['rating']   
        # Create a new movie entry
        new_movie = {
            'id': movie_id,
            'thumbnails': thumbnail,
            'movie_name': moviename,
            'brief_description': description,
            'rating': rating
        }
        # Check for duplicate ID
        if any(movie['id'] == new_movie['id'] for movie in movies_info['movies']):
            flash("Movie with this ID already exists", "error")
            return redirect(url_for('add_movie'))
        # Add the new movie to the list
        movies_info["movies"].append(new_movie)    
        # Write the updated list back to the file
        with open("movies.json", "w") as movies_file:
            json.dump(movies_info, movies_file, indent=4)        
        # Redirect to the home page
        return redirect(url_for('movies'))
    
    return render_template('add.html')

#remove dupliacates with the same name and ID
def remove_duplicates(file_path):
    with open("movies.json", 'r') as file:
        movies = json.load(file)

    seen_ids = set()
    unique_movies = []
    for movie in movies['movies']:
        if movie['id'] not in seen_ids:
            unique_movies.append(movie)
            seen_ids.add(movie['id'])

    movies['movies'] = unique_movies

    with open("movies.json", 'w') as file:
        json.dump(movies, file, indent=4)

remove_duplicates('movies.json')


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
        
        # return jsonify({"message": "Movie updated successfully"}), 200
    return redirect(url_for('movies'))
    
    # return render_template('index.html')


        






    

    