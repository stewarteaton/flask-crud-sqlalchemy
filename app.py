from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'flash_secret'
app.permanent_session_lifetime = timedelta(minutes=5)

# SQLAlchemy - write DB in python 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pet(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True, unique=True)
    name = db.Column( db.String(100), nullable=False)
    species = db.Column( db.String(3), nullable=False)

    def __init__ (self, name, species):
        self.name = name
        self.species = species

    @property
    def serialize(self):
       ## Return object data in easily serializable format
       return {
           '_id' : self._id,
           'name': self.name,
           'species'  : self.species
       }


# Get all records or Delete by ID
@app.route("/", methods=["GET", "POST"])
def home():
    # delete pet if post
    if request.method == "POST":
        petID = request.form['delete']
        p = Pet.query.filter_by(_id=petID).first()
        db.session.delete(p)
        db.session.commit()
        flash(f'Successfully deleted pet id: {petID}','info')
        return redirect('/')

    # Get all records for home
    else:
        pets = Pet.query.all()
        json_list = [i.serialize for i in pets] # Convert to JSON
        print(json_list)

        return render_template('index.html', pets=json_list)


# Create new pet entry
@app.route("/new-pet", methods=["POST"])
def newPet():
    if not request.form['name'] or not request.form['species']:
        flash('Error with request', 'error')
    else:
        petName = request.form['name']
        petSpecies = request.form['species']
        pet = Pet(petName, petSpecies)

        db.session.add(pet)
        db.session.commit()
        flash(f'Successfully added {petName}','info')

    return redirect('/')


# Get or Update pet by ID
@app.route("/pet", methods=["POST","GET"])
def pet():
    # Return searched pet if Get
    if request.method == "GET":
        petID = request.args.get('petID')
        pet = Pet.query.filter_by(_id=petID).first()
        return render_template('pet.html', pet=pet)
    # Update if Post
    elif request.method == "POST":
        petID = request.form['update']
        p = Pet.query.filter_by(_id=petID).first()
        p.name = request.form['name']
        p.species = request.form['species']
        db.session.commit()
        flash(f'Successfully updated {p.name}, id: {petID}','error')
        return redirect('/')
    else:
        return redirect('/')



if __name__ == "__main__":
    db.create_all()     #create db when run if doesn't already exist
    app.run(host='0.0.0.0', port=8881, debug=True)