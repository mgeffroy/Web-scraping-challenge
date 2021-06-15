# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def home():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars= mars)


@app.route("/scrape")
def scrape():
    #Run scrape function 
    mars_data = mars_scrape.scrape_info()
    mars.update({}, mars_data, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
