#python-*- coding: utf-8 -*-
import flask
from flask import Flask, render_template, url_for, request
from sklearn.externals import joblib
from flask_sqlalchemy import SQLAlchemy
import os
import corapp
from corapp import app 
from corapp import db

#app = Flask(__name__) # Instansiation de l'application

#app.config.from_object(os.environ["APP_SETTINGS"]) # Choisir l'environnement de l'application. Voir dans .env pour savoir le quel sera choisi. Puis on se connecte à la base de données en utilisant les données de connexion dans .env DBUSR, DBPASS, DBHOST, DBNAME
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app) 

from models import Result

@app.route("/") # route par défaut --> elle te renvoie à la page principale (index.html)
def index():
    return render_template("index.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        regressor = joblib.load("./linear_regression_model.pkl") # Charger notre modèle
        yearsExperience = [[float(dict(request.form)["YearsExperience"])]] # Récupérer le nombre d'année qui a été envoyé à partir de la page index.html (voir le fomulaire)
        prediction = regressor.predict(yearsExperience) # Lancer la prédiction avec le modèle chargé plus haut

        result = Result(
            YearsExperience = yearsExperience[0][0],
            Prediction = float(prediction)
        ) # Stocker notre prédiction dans la variable result : Année d'expérience et notre prédiction
        print(db)
        db.session.add(result) # Ajouter nos résultats à BD
        db.session.commit()


    return render_template("prediction.html", prediction = float(prediction)) # Afficher les résultats dans la page prediction.html

if __name__ == "__main__":
    corapp.app.run(debug=True)
