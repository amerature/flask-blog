from datetime import datetime
import random
from flask import Flask, request, redirect, url_for, render_template
from flask.ext.mongokit import MongoKit, Document

#app declaration
app = Flask(__name__)

#Post model
class Post(Document):
	__collection__ = 'posts'

	#DB Structure
	structure = {
		'id': int,
		'title': unicode,
		'text': unicode,
		'creation': datetime,
	}
	default_values = {'creation': datetime.utcnow}
	#dont know why required, dont remove
	use_dot_notation = True

#connection of database, requires mongod first in terminal running on port.
# brew install mongodb 
db = MongoKit(app)
#registers Post class in DB
db.register([Post])

#generates id
def generate():
	u = int(random.random()*100000)
	return u


@app.route('/add', methods=["GET", "POST"])
#declaring request methods

#new post
def new_post():
	#POST request
	if request.method == 'POST':
		#declaring new post
		post = db.Post()

		#contents of post
		post.id = generate()

		# name attribute from form request
		# note form has to have post method and /add as seen in add.html template
		post.title = request.form['title']
		post.text = request.form['text']
		####################
		post.save()
		#redirects to index to see posts
		return redirect(url_for('index'))

	#on get request, shows add.html in order to add posts
	elif request.method == 'GET':

		return render_template('add.html')

#index page
@app.route('/')
def index():
	#finds all posts and sorts in reverse chronological order
	posts = db.Post.find().sort("creation", -1)
	# displays posts on list template
	return render_template('list.html', posts=posts)

if __name__ == "__main__":
	#debug = True means no closing and re-opening server
	app.run(debug=True)


