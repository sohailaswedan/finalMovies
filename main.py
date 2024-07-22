from flask import Flask
import json
from user import User
import routes
from flask import render_template, request,url_for, session,jsonify,redirect,flash


app = Flask(__name__)
app.secret_key='sohaila'
admin_emails = ['sohailaswedan45@gmail.com']

app.add_url_rule('/', 'login', routes.login, methods=['POST', 'GET'])
app.add_url_rule('/home', 'home', routes.home)
app.add_url_rule('/update/<movie_id>', 'update_movie', routes.update_movie, methods=['GET', 'POST'])
app.add_url_rule('/add', 'add_movie', routes.add_movie, methods=['GET', 'POST'])
app.add_url_rule('/delete_movie/<movie_id>', 'delete_movie', routes.delete_movie)
app.add_url_rule('/movies', 'movies', routes.movies)
app.add_url_rule('/deleteAccount', 'deleteAccount', routes.deleteAccount, methods=['POST', 'GET'])

if __name__ == "__main__":
    app.run(debug=True)
