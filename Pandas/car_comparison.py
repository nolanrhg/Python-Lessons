#!/usr/local/bin/python3.6

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

cars_df = pd.read_csv("car_specs.csv")

porsche_df = cars_df.loc[cars_df['make'] == "Porsche"]
bmw_df = cars_df.loc[cars_df['make'] == "BMW"]

print(porsche_df.describe())
print(bmw_df.describe())

# Find the average price of a car with 0 - 60 accel. time less than or equal to 4.0 s
accel_filter = (cars_df["acceleration"] <= 4.0)
accel_filtered_df = cars_df[accel_filter]

print(accel_filtered_df.mean())

print(cars_df.corr())
