#!/usr/local/bin/python3.6

'''IMPORTS'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import sys

'''DATA'''
cars_df = pd.read_csv("car_specs.csv")

# Strip extra white space from values in columns that have string values
for col_name in list(cars_df.columns.values):
	if isinstance(cars_df[col_name][0], str):
		cars_df[col_name] = cars_df[col_name].str.strip()

commands = ["makelist"]

if (sys.argv[1] == "makelist"):
	for make in cars_df.make.unique():
		print(make)	

	desired_make = input("Which make are you interested in? ")
	
	# List all models made by "desired_make" company	
	make_filter = (cars_df["make"] == desired_make)
	make_filtered_df = cars_df[make_filter]
	
	print("The latest models made by " + desired_make + " are as follows:\n")	
	for model in make_filtered_df.model.unique():
		print(model) 

	desired_model = input("Which model are you interested in? ")
	
	# Create string corresponding to name of model's image file	
	model_img_str = desired_model.lower().replace(" ", "_")
	img_path = "car_pics/" + desired_make + "/" + model_img_str + ".png"
	
	try:
		model_img = mpimg.imread(img_path)
	except FileNotFoundError:
		img_path = img_path.replace(".png", ".jpg")	
		model_img = mpimg.imread(img_path)
	
	plt.imshow(model_img)
	plt.show()
		

