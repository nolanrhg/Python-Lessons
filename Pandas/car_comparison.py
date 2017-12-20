#!/usr/local/bin/python3.6


"""**************************************************
*						    *
*			IMPORTS			    *
*						    *
**************************************************"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import sys


"""**************************************************
*						    *
*	              FUNCTIONS			    *
*						    *
**************************************************"""
def get_percentile(obs, data):


	"""Find an observation's percentile"""

	
	# Counts observations in data that are less than or equal to obs	
	obs_lte = 0

	for d in data:

		if d <= obs:
			obs_lte += 1
	
	# Percentile calculation 
	pctl = 100 * ((obs_lte * 1.0) / len(data))
	
	# Return percentile to caller
	return pctl


def strip_white_space(df):


	"""Strip leading and trailing white space from any strings in the dataframe"""

	
	for col_name in list(df.columns.values):

		if isinstance(df[col_name][0], str):
			df[col_name] = df[col_name].str.strip()


def replace_na_with_col_mean(df, colname, categories):
	

	"""Replaces NA values in dataframe with corresponding column mean,
	   where the data is grouped according to the categories in the 
	   provided column name (colname)."""
	
	print("\n\n\nTEST\n\n\n")	
	
	## First find columns that this method cannot be applied to
	## (i.e., columns that don't contain numbers)
	blacklist = []
	for col_name in list(df.columns.values):
		if isinstance(df[col_name][0], str):
			blacklist.append(col_name)		

	## Replace NA values in non-blacklisted columns
	for c in categories:

		category_filter = (df[colname] == c)
		category_filtered_df = df[category_filter]

		for col_name in list(set(df.columns.values).difference(blacklist)):

			df[[col_name]] = df[[col_name]].fillna(category_filtered_df[col_name].mean())



"""**************************************************
*						    *
*	         DATA ACQUISITION		    *
*						    *
**************************************************"""
## Read in car specs data
cars_df = pd.read_csv("car_specs.csv")


"""**************************************************
*						    *
*	         DATA CLEANING		            *
*						    *
**************************************************"""
## Strip white leading and trailing white space from strings in cars dataframe
strip_white_space(cars_df)
print('\n\n\n')
print(cars_df)
print('\n\n\n')
replace_na_with_col_mean(cars_df, 'make', cars_df['make'].unique())


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
#ax2.text(500, 0.01, 'Percentile: %.1f' % hp_pctl, fontweight = 'bold')

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
#ax3.text(150, 0.01, 'Percentile: %.1f' % ts_pctl, fontweight = 'bold')
	
plt.show()
