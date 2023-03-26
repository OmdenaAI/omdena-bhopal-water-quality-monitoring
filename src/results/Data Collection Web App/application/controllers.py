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


@app.route("/errorPage")
def errorPage():
	return render_template("404.html")

@app.route("/", methods = ["GET", "POST"])
def home():
	selected_val = selected_lake = ""
	if request.method == "POST":
		selected_lake = request.form["lake"]
		selected_val = request.form["param"]
	return render_template("index.html", selected_val = selected_val, selected_lake = selected_lake)

@app.route("/fetch/<param>/<lake>", methods = ["GET", "POST"])
def fetch(param, lake):
	df = ""
	if request.method == "POST":
		lake_df = pd.read_csv("data_directory/lake_data.csv")
		print()
		geometry = ee.Geometry.Polygon(list(eval(lake_df[lake_df["Name"] == lake].iloc[0]["Coordinates "])))
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
	return render_template("value_display.html", param = param, lake = lake , df = df)