# import necessary libraries

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars_info = scrape_mars
    mongo.db.collection.update({}, mars_info, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
