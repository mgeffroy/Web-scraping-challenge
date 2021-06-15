# import necessary libraries

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


@app.route("/")
def home():
    mongo_mars = client.mars_db.collection.find_one()
    return render_template("index.html", flask_mars= mongo_mars)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()
    client.mars_db.collection.update({}, mars_data, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
