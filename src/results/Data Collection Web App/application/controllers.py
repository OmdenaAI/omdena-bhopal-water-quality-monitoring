from flask import current_app as app
from flask import render_template, request, url_for, redirect
from .dataFetch import *
import ee
import os
import pandas as pd
from IPython.display import HTML

service_account = os.getenv("auth_email")

credentials = ee.ServiceAccountCredentials(service_account, os.getenv("auth_pass"))
ee.Initialize(credentials)



geometry = ee.Geometry.Polygon([[77.39546956268856,23.265850898429633],[77.39576192347118,23.263643049175467],[77.39595504252026,23.263781040825478],[77.39609988180706,23.263738453582683],[77.39656926838467,23.26489905664098],[77.39658804384777,23.265207070617443],[77.39640297142574,23.265850201505117],[77.39614011494228,23.266249384632868],[77.3959443136842,23.26634548409614],[77.39546956268856,23.265850898429633]])


@app.route("/errorPage")
def errorPage():
	return render_template("404.html")

@app.route("/", methods = ["GET", "POST"])
def home():
	selected_val = ""
	if request.method == "POST":
		selected_val = request.form["param"]
	return render_template("index.html", selected_val = selected_val)

@app.route("/fetch/<param>", methods = ["GET", "POST"])
def fetch(param):
	df = ""
	if request.method == "POST":
		start_date = request.form["start_date"]
		end_date = request.form["end_date"]

		try:
			if param == "NDCI":
				df = NDCI(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "NDTI":
				df = NDTI(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "NDSI":
				df = NDSI(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "DO":
				df = DO(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "pH":
				df = pH(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "Temperature":
				df = Temperature(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "Dissolved Organic Matter":
				df = DissolvedOrganicMatter(geometry, start_date, end_date)
				df = df.to_dict('dict')

			elif param == "Suspended Matter":
				df = SuspendedMatter(geometry, start_date, end_date)
				df = df.to_dict('dict')


		except:
			return redirect(url_for("errorPage"))
	return render_template("value_display.html", param = param, df = df)