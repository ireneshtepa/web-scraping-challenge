# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# @TODO: Initialize your Flask app here
# CODE GOES HERE
app=Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017/mission'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)



# @TODO:  Create a route and view function that takes in a dictionary and renders index.html template
# CODE GOES HERE
@app.route("/")
def index():
    mars = client.missionDb.mars.find_one()
    return render_template("index.html", mars = mars)


@app.route("/scrape")
def scrape():
    mars = client.missionDb.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


    
if __name__ == "__main__":
    app.run(debug=True)
