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


'''ACQUIRE DATA'''
## Read in car specs data
cars_df = pd.read_csv("car_specs.csv")


'''CLEAN DATA'''
## Strip extra white space from values in columns that have string values
for col_name in list(cars_df.columns.values):
	if isinstance(cars_df[col_name][0], str):
		cars_df[col_name] = cars_df[col_name].str.strip()

## Replace NA values with column mean
for make in cars_df.make.unique():
	make_filter = (cars_df['make'] == make)
	make_filtered_df = cars_df[make_filter]
	for col_name in list(set(cars_df.columns.values).difference(['make', 'model'])):
		cars_df[[col_name]] = cars_df[[col_name]].fillna(make_filtered_df[col_name].mean())


'''GET USER INPUT'''
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


'''VISUALIZE DATA'''
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
hp_obs = obs_df.iloc[0]['horsepower']

# top speed obs
ts_obs = obs_df.iloc[0]['top_speed']

## Display image of car model requested by user
ax1.imshow(model_img)
ax1.set_title(desired_make + " " + desired_model, fontweight = 'bold')

for spine in ['top', 'bottom', 'left', 'right']:
	ax1.spines[spine].set_visible(False)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.text(10, 20, 'Horsepower: %d hp' % hp_obs, fontweight = 'bold')

## Compare horsepower of selected model with all other models
ax2.grid(color = 'k', linestyle = '-', linewidth = 0.3)
ax2.set_facecolor('wheat')
n1, bins1, h_bars1 = ax2.hist(make_filtered_df["horsepower"].values, bins = 30, 
			   histtype = "bar", edgecolor = 'black', linewidth = 1.5, normed = True,
			   color = 'gray')
ax2.set_title(desired_make + " " + "Horsepower Distribution", fontweight = "bold")
ax2.set_xlabel("Horsepower")

for i, edge in zip(range(0, len(bins1) - 1), bins1):
	if (hp_obs > edge):
		h_bars1[i].set_color('green')		
		h_bars1[i].set(edgecolor = 'k')
		h_bars1[i].set(linewidth = 1.5)

## line plot
x2 = list(b.get_x() + b.get_width() / 2 for b in h_bars1)
y2 = list(b.get_height() for b in h_bars1)
ax2.plot(x2, y2, color = 'black', linewidth = 1.5, alpha = 0.8, linestyle = '-.')

hp_pctl = get_percentile(hp_obs, make_filtered_df["horsepower"].values)
#ax2.text(500, 0.01, 'Percentile: %.1f' % (100 * hp_pctl), fontweight = 'bold')

## Compare acceleration of selected model with all other models
ax3.grid(color = 'k', linestyle = '-', linewidth = 0.3)
ax3.set_facecolor('wheat')
n2, bins2, h_bars2 = ax3.hist(make_filtered_df['top_speed'].values, bins = 30,
			      histtype = 'bar', edgecolor = 'black', linewidth = 1.5, normed = True,
			      color = 'gray')
ax3.set_title(desired_make + " " + "Top Speed Distribution", fontweight = 'bold')
ax3.set_xlabel("Top Speed")

for i, edge in zip(range(0, len(bins2) - 1), bins2):
	if (ts_obs > edge):
		h_bars2[i].set_color('green')
		h_bars2[i].set(edgecolor = 'k')
		h_bars2[i].set(linewidth = 1.5)

## line plot
x3 = list(b.get_x() + b.get_width() / 2 for b in h_bars2)
y3 = list(b.get_height() for b in h_bars2)
ax3.plot(x3, y3, color = 'black', linewidth = 1.5, alpha = 0.8, linestyle = '-.')

ts_pctl = get_percentile(ts_obs, make_filtered_df['top_speed'].values)
#ax3.text(150, 0.01, 'Percentile: %.1f' % (100 * ts_pctl), fontweight = 'bold')
	
plt.show()
