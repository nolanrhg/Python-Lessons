#!/usr/local/bin/python3.6

'''IMPORTS'''
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import sys

'''FUNCTIONS'''
def get_percentile(obs, data):
	
	# Counts observations less than or equal to obs	
	obs_lte = 0
	for d in data:
		if d <= obs:
			obs_lte += 1
	
	# Calculate percentile
	pctl = (obs_lte * 1.0) / len(data)		
	
	# Return percentile to caller
	return pctl

'''DATA'''
## Read in car specs data
cars_df = pd.read_csv("car_specs.csv")

## Strip extra white space from values in columns that have string values
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


## Create a figure with 4 subplots for displaying car information
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize = (11, 6))

## Get image of requested car model
try:
	model_img = mpimg.imread(img_path)
except FileNotFoundError:
	img_path = img_path.replace(".png", ".jpg")	
	model_img = mpimg.imread(img_path)

## Display selected model's horsepower percentile on graph
obs_filter = (make_filtered_df["model"] == desired_model)
obs_df = make_filtered_df[obs_filter]
obs = obs_df.iloc[0]['horsepower']

## Display image of car model requested by user
ax1.imshow(model_img)
ax1.set_title(desired_make + " " + desired_model, fontweight = 'bold')
for spine in ['top', 'bottom', 'left', 'right']:
	ax1.spines[spine].set_visible(False)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.text(10, 20, 'Horsepower: %d hp' % obs, fontweight = 'bold')

## Compare horsepower of selected model with all other models
make_filtered_df.loc[make_filtered_df['horsepower'].isnull()] = make_filtered_df["horsepower"].mean()
n, bins, h_bars = ax2.hist(make_filtered_df["horsepower"].values, bins = 20, 
			   histtype = "bar", edgecolor = 'black', linewidth = 1.5, normed = True,
			   color = 'lightblue')
ax2.set_title(desired_make + " " + "Horsepower Distribution", fontweight = "bold")
ax2.set_xlabel("Horsepower")

for i, edge in zip(range(0, len(bins) - 1), bins):
	if (obs > edge):
		h_bars[i].set_color('green')		
		h_bars[i].set(edgecolor = 'k')
		h_bars[i].set(linewidth = 1.5)
	else:
		continue

hp_pctl = get_percentile(obs, make_filtered_df["horsepower"].values)

ax2.text(500, 0.01, 'Percentile: %.1f' % (100 *hp_pctl), fontweight = 'bold')
	
plt.show()
