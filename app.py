#Mileage Tracker by Blake Pecore
#app.py
#Main file for project

#Import for Flask
from flask import Flask, render_template

#Import for Forms (Registration, Login, Mileage maker)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

#Import for SQL
from flask_sqlalchemy import SQLAlchemy

#Misc imports
import os
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic, Distance

#Global variables
SECRET_KEY = os.urandom(24).hex()
locations = [("125 Finney Blvd, Malone, NY 12953", "Finney"), 
    ("294 Elm Street, Malone, NY 12953", "Home"),
    ("324 Creighton Road, Malone, NY 12953", "Creighton")]

#Geolocation variables
geolocator = Nominatim(user_agent='caimileage')

#Initial Flaks instance
app = Flask(__name__)

#App configurations
app.config['SECRET_KEY'] = SECRET_KEY

#Form class for creating mileage
class MileageForm(FlaskForm):
    startingLocation = SelectField("Starting Location", choices=locations)
    endingLocation = SelectField("Ending Locations", choices=locations)
    submit = SubmitField("Submit")

class AddLocation(FlaskForm):
    locationName = StringField("Location Name")
    locationAddr = StringField("Location Address")
    submit2 = SubmitField("Submit")

def getDistance(location1, location2):
    location1Geo = geolocator.geocode(location1)
    location2Geo = geolocator.geocode(location2)

    loc1Lat = location1Geo.latitude
    loc1Lon = location1Geo.longitude
    loc2Lat = location2Geo.latitude
    loc2Lon = location2Geo.longitude

    location1Addr = (loc1Lat, loc1Lon)
    location2Addr = (loc2Lat, loc2Lon)
    try:
        return (geodesic(location1Addr, location2Addr)).miles
    except:
        print('Not valid')

#Main route page
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/mileage", methods=['GET', 'POST'])
def mileage():
    startingLocation = None
    endingLocation = None
    locationName = None
    locationAddr = None
    distance = None
    mileageForm = MileageForm()
    locationForm = AddLocation()
    if mileageForm.validate_on_submit():
        startingLocation = mileageForm.startingLocation.data
        endingLocation = mileageForm.endingLocation.data
        mileageForm.endingLocation.data = ''
        mileageForm.startingLocation.data = ''
        distance = math.ceil(getDistance(startingLocation, endingLocation))
    if locationForm.validate_on_submit():
        print('validated')
        locationName = locationForm.locationName.data
        locationAddr = locationForm.locationAddr.data
        locationForm.locationName.data = ''
        locationForm.locationAddr.data = ''
        locations.append((locationAddr, locationName))
        print(locations)
    else:
        print('not validated')
    return render_template("mileage.html",
        startingLocation = startingLocation,
        endingLocation = endingLocation,
        mileageForm = mileageForm,
        distance = distance,
        locationName = locationName,
        locationAddr = locationAddr,
        locationForm = locationForm)