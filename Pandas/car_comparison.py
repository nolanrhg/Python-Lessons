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


def get_horsepower(make, model):

	
	"""Get horsepower of desired car"""	

	
	## Filter by car make
	make_filter = (cars_df['make'] == make)
	make_filtered_df = cars_df[make_filter]

	## Filter by model
	model_filter = (make_filtered_df['model'] == model)
	make_model_filtered_df = make_filtered_df[model_filter]		

	## Get horsepower observation
	hp = make_model_filtered_df.iloc[0]['horsepower']	

	## Return horsepower to caller
	return hp

			
def get_top_speed(make, model):

	
	"""Get top speed of desired car"""	

	
	## Filter by car make
	make_filter = (cars_df['make'] == make)
	make_filtered_df = cars_df[make_filter]

	## Filter by model
	model_filter = (make_filtered_df['model'] == model)
	make_model_filtered_df = make_filtered_df[model_filter]		

	## Get horsepower observation
	ts = make_model_filtered_df.iloc[0]['top_speed']	

	## Return horsepower to caller
	return ts 


def get_accel_time(make, model):
	
	
	"""Get acceleration time of desired car"""


	## Filter by car make
	make_filter = (cars_df['make'] == make)
	make_filtered_df = cars_df[make_filter]

	## Filter by model
	model_filter = (make_filtered_df['model'] == model)
	make_model_filtered_df = make_filtered_df[model_filter]		

	## Get horsepower observation
	at = make_model_filtered_df.iloc[0]['acceleration_time']	

	## Return horsepower to caller
	return at


def get_price(make, model):
	
	
	"""Get price of desired car"""


	## Filter by car make
	make_filter = (cars_df['make'] == make)
	make_filtered_df = cars_df[make_filter]

	## Filter by model
	model_filter = (make_filtered_df['model'] == model)
	make_model_filtered_df = make_filtered_df[model_filter]		

	## Get horsepower observation
	price = make_model_filtered_df.iloc[0]['price']	

	## Return horsepower to caller
	return price 

"""**************************************************
*						    *
*	         DATA ACQUISITION		    *
*						    *
**************************************************"""
## Read in car specs data
global cars_df
cars_df = pd.read_csv("car_specs.csv")


"""**************************************************
*						    *
*	         DATA CLEANING		            *
*						    *
**************************************************"""
## Strip leading and trailing white space from strings in cars dataframe
strip_white_space(cars_df)
replace_na_with_col_mean(cars_df, 'make', cars_df['make'].unique())


"""**************************************************
*						    *
*	          USER INPUT		            *
*						    *
**************************************************"""
# List all car makers
for make in cars_df.make.unique():
	print(make)	

# Car make the user is interested in
desired_make = input("Which make are you interested in? ")

# List all models made by "desired_make" company	
make_filter = (cars_df["make"] == desired_make)
make_filtered_df = cars_df[make_filter]
for model in make_filtered_df.model.unique():
	print(model) 

print("Above is a list of the most recent models made by " + desired_make)	

# Car model the user is interested in
desired_model = input("Which model are you interested in? ")


"""**************************************************
*						    *
*	          DATA VISUALIZATION	            *
*						    *
**************************************************"""

def display_car_image(make, model, ax):
	

	"""Displays car image on provided set of axes (ax)"""

	
	model_img_str = model.lower().replace(" ", "_")	
	img_path = "car_pics/" + make + "/" + model_img_str + ".png"

	try:
		model_img = mpimg.imread(img_path)	
	except FileNotFoundError:
		img_path = img_path.replace(".png", ".jpg")
		model_img = mpimg.imread(img_path)	
	
	## Remove spines and axes' ticks/tick labels	
	for spine in ['top', 'bottom', 'left', 'right']:
		ax.spines[spine].set_visible(False)	
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	
	## Add car information to display		
	ax.set_title(make + " " + model, fontweight = 'bold', fontsize = 8)
	
	## Show image of car on ax
	ax.imshow(model_img)


def display_car_specs(make, model, ax):
	
	hp = get_horsepower(make, model)
	ts = get_top_speed(make, model)
	at = get_accel_time(make, model)	
	p = get_price(make, model)
	
	ax.text(0, 1, 'Horsepower:', fontweight = 'bold', fontsize = 8)
	ax.text(0.5, 1, '%d hp' % hp, color = 'blue', fontsize = 8)

	ax.text(0, 0.9, 'Top Speed:', fontweight = 'bold', fontsize = 8)
	ax.text(0.4, 0.9, '%d mph' % ts, fontsize = 8, color = 'blue')

	ax.text(0, 0.8, '0 - 60 MPH:', fontweight = 'bold', fontsize = 8)
	ax.text(0.5, 0.8, '%.1f s' %at, fontsize = 8, color = 'blue')

	ax.text(0, 0.7, 'Price:', fontweight = 'bold', fontsize = 8)
	ax.text(0.3, 0.7, '$%d' %p, color = 'blue', fontsize = 8)

		


## Create a figure with 4 subplots for displaying car information
FIG_WIDTH = 13
FIG_HEIGHT = 6
fig, ((ax1, ax2, ax3, ax4), (ax5, ax4, ax6, ax7)) = plt.subplots(nrows = 2, ncols = 4, figsize = (FIG_WIDTH, FIG_HEIGHT))
fig.subplots_adjust(wspace = 0.5, hspace = 0.3)

hp_obs = get_horsepower(desired_make, desired_model)
ts_obs = get_top_speed(desired_make, desired_model)
accel_obs = get_accel_time(desired_make, desired_model)

## Display image of car model requested by user
display_car_image(desired_make, desired_model, ax1)
display_car_specs(desired_make, desired_model, ax5)

## Compare horsepower of selected model with all other models
ax2.grid(color = 'k', linestyle = '-', linewidth = 0.3)
ax2.set_facecolor('wheat')
n1, bins1, h_bars1 = ax2.hist(make_filtered_df["horsepower"].values, bins = 20, 
			   histtype = "bar", edgecolor = 'black', linewidth = 1.5, normed = True,
			   color = 'gray')
ax2.set_title(desired_make + " " + "Horsepower Distribution", fontweight = "bold", fontsize = 8)
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
n2, bins2, h_bars2 = ax3.hist(make_filtered_df['top_speed'].values, bins = 20,
			      histtype = 'bar', edgecolor = 'black', linewidth = 1.5, normed = True,
			      color = 'gray')
ax3.set_title(desired_make + " " + "Top Speed Distribution", fontweight = 'bold', fontsize = 8)
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

## Remove spines from ax5
for spine in ['top', 'bottom', 'left', 'right']:
	ax5.spines[spine].set_visible(False)	
ax5.get_xaxis().set_visible(False)
ax5.get_yaxis().set_visible(False)

plt.show()
