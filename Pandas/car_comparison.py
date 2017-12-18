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

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize = (11, 6))

try:
	model_img = mpimg.imread(img_path)
except FileNotFoundError:
	img_path = img_path.replace(".png", ".jpg")	
	model_img = mpimg.imread(img_path)

ax1.imshow(model_img)
ax1.set_title(desired_make + " " + desired_model, fontweight = 'bold')

for spine in ['top', 'bottom', 'left', 'right']:
	ax1.spines[spine].set_visible(False)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)

plt.show()
