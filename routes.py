
import json
import re
from user import User
from flask import render_template, request,url_for, session,jsonify,redirect,flash

def deleteAccount():
    email = session.get('email')
    if email:
        User.delete_user(email)      
        session.pop('email', None)        
        session.clear()   
    return redirect(url_for('login'))


def login():
    validation_message = None
    if 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with open('static/json/users.json', 'r') as infile:
            data = json.load(infile)
        for user in data:
            if user['email'] == email and int(user['password']) == int(password):
                session['email'] = email
                session['role'] = user['role']
                return redirect(url_for('home'))
        validation_message = 'Invalid email or password. Please try again.'
    return render_template('login.html', validation_message=validation_message)


def home():
    if 'email' not in session:
        return redirect('/')
    with open("static/json/movies.json", "r") as json_file:
        movies_data = json.load(json_file)      
    return render_template("index.html", movies=movies_data["movies"],filtered_movies = None)



def movies():
    with open("static/json/movies.json", "r") as json_file:
        movies_info = json.load(json_file)
    return render_template("index.html", movies=movies_info["movies"],filtered_movies = None)



def delete_movie(movie_id):
    mov = None
    with open("static/json/movies.json", "r") as json_file:
        movies_info = json.load(json_file)
    for movie in movies_info["movies"]:
        if int(movie["id"]) == int(movie_id):    
            mov = movie
            break
    if not mov:
        flash("Movie not found", "error")
        return redirect(url_for('movies'))
    movies_info["movies"].remove(mov)   
    with open("static/json/movies.json", "w") as json_file:
        json.dump(movies_info, json_file, indent=4)
    flash("Movie deleted successfully", "success")
    return redirect(url_for('movies'))



def add_movie():
    with open("static/json/movies.json", "r") as json_file:
        movies_info = json.load(json_file)
    if request.method == "GET":
        return render_template("add.html")
    if request.method == "POST":
        movie_id = request.form['id']
        thumbnail = request.form['thumbnail']
        moviename = request.form['moviename']
        description = request.form['description']
        rating = request.form['rating']
        if not validate_word_count(description):
            flash("Description exceeds the maximum word limit of 100 words.", "error")
            return redirect(url_for('add_movie'))
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
        if any(int(movie['id']) == int(movie_id) for movie in movies_info['movies']):
            flash("Movie with this ID already exists", "error")
            return redirect(url_for('add_movie'))
        new_movie = {
            'id': movie_id,
            'thumbnails': thumbnail,
            'movie_name': moviename,
            'brief_description': description,
            'rating': rating
        }
        movies_info["movies"].append(new_movie)
        with open("static/json/movies.json", "w") as movies_file:
            json.dump(movies_info, movies_file, indent=4)
        flash("Movie added successfully", "success")
        return redirect(url_for('movies'))
    return render_template('add.html')



def update_movie(movie_id):
    with open("static/json/movies.json", "r") as json_file:
        movies_info = json.load(json_file)
    if request.method == "GET":
        movie_to_update = None
        for movie in movies_info["movies"]:
            if int(movie["id"]) == int(movie_id):
                movie_to_update = movie
                break
        if not movie_to_update:
            return jsonify({"message": "Movie not found"}), 404
        return render_template("update.html", movie=movie_to_update)
    elif request.method == "POST":
        updated_thumbnail = request.form['thumbnail']
        updated_moviename = request.form['moviename']
        updated_description = request.form['description']
        updated_rating = float(request.form['rating'])
        movie_to_update = None
        for movie in movies_info["movies"]:
            if int(movie["id"]) == int(movie_id):
                movie_to_update = movie
                break
        if not movie_to_update:
            return jsonify({"message": "Movie not found"}), 404
        movie_to_update['thumbnails'] = updated_thumbnail
        movie_to_update['movie_name'] = updated_moviename
        movie_to_update['brief_description'] = updated_description
        movie_to_update['rating'] = updated_rating
        with open("static/json/movies.json", "w") as movies_file:
            json.dump(movies_info, movies_file, indent=4)
        return redirect(url_for('movies', success='true'))
    return render_template('update.html')

def validate_word_count(text, max_words=100):
    word_count = len(re.findall(r'\b\w+\b', text))
    return word_count <= max_words


def search_movies():
        with open("static/json/movies.json", "r") as json_file:
                movies_info = json.load(json_file)
        if request.method=="POST":
            query = request.form["query"].lower()
            if not query:
                return render_template("index.html", movies=movies_info["movies"],filtered_movies = None)
            # Filter movies based on the search query
            filtered_movies = [
                    movie for movie in movies_info["movies"]
                    if query in movie["movie_name"].lower()
                ]
            return render_template("index.html", movies=movies_info["movies"],filtered_movies = filtered_movies)
        return render_template("index.html", movies=movies_info["movies"],filtered_movies = None)




