#!/usr/local/bin/python3.6



##--- IMPORTS ---##

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches



##--- DATA ---##

# Dictionary containing Nvidia's annual net income from 1993 to 2016
# All data from Nvidia's 10-K forms stored in the SEC's EDGAR database
# All net income amounts in millions
nvda_ani_raw = {
	   2016 : 1666,
	   2015 : 614,
	   2014 : 631,
	   2013 : 440,
	   2012 : 563,
	   2011 : 581,
	   2010 : 253,
	   2009 : -68,
	   2008 : -30,
	   2007 : 798,
	   2006 : 449,
	   2005 : 301,
	   2004 : 89,
	   2003 : 49,
	   2002 : 51,
	   2001 : 142,
	   2000 : 98,
	   1999 : 41,
	   1998 : 4,
	   1997 : 1,
	   1996 : -4,
	   1995 : -3,
	   1994 : -6,
	   1993 : -1,
	  }

yrs = list(reversed(list(key for key in nvda_ani_raw))) # ordered year data
nis = list(reversed(list(nvda_ani_raw[key] for key in nvda_ani_raw))) # ordered net income data



##--- DATA VISUALIZATION ---##

# Create 10 in x 6 in figure with one subplot
FIG_WIDTH = 12
FIG_HEIGHT = 6
fig, ax = plt.subplots(figsize = (FIG_WIDTH, FIG_HEIGHT))

# Create and plot regression line for predicting future net income
z = np.polyfit(yrs, nis, deg = 1)
f = np.poly1d(z) # regression line
x = np.linspace(yrs[0], yrs[-1] + 11, 50)
y = f(x) # evaluation of regression line function over x
ax.plot(x, y, color = 'black', alpha = 0.7, linestyle = 'solid') # plot regression line

# Plot hand-calculated regression line
y_hc = -79621.9 + 39.86 * x # hand-calculated regression eq.
ax.plot(x, y_hc, color = 'yellow', alpha = 0.3, linewidth = 5) # plot regression line

# Create bar plot of net income data
bars = ax.bar(yrs, nis, color = 'green')

# Create line-plot representation of net income data
points = ax.plot(yrs, nis, linestyle = 'dashed', marker = '*', color = 'blue', alpha = 0.25)

# Create bar plot for the predicted net incomes
extended_yrs = range(max(yrs) + 1, max(yrs) + 11)
pred_nis = list(f(y) for y in extended_yrs)
extended_bars = ax.bar(extended_yrs, pred_nis, color = 'gray')

# Add net income amounts above bars in bar graph (makes graph easier to read)
for bar, ni in zip(bars + extended_bars, nis + pred_nis):
	bar_height = bar.get_height()
	if (bar_height < 0):
		bar.set_color('salmon') # Make bars corresponding to negative net incomes red
		text_height = 20
	else:
		text_height = bar_height + 40
	
	# Insert text
	ax.text(bar.get_x() + bar.get_width() / 2, text_height, '%d' % ni, ha = 'center', va = 'bottom',
	        fontweight = 'bold', color = 'black', fontsize = 6)

# Include text describing predicted growth
ax.text(extended_bars[0].get_x() + extended_bars[0].get_width() / 2, -150, 
	'%d %% growth' % int(((f(extended_yrs[1]) - f(extended_yrs[0])) / f(extended_yrs[0])) * 100),
	fontweight = 'bold', fontsize = 14)

# Include regression line equation
ax.text(2000, -200, '$y=-79621.9 + 39.86x$', fontweight = 'bold', fontsize = 10)

# Create legend for plot
loss_rect = patches.Rectangle((0, 0), 1, 1, fc= 'salmon') # red rectangle
gain_rect = patches.Rectangle((0, 0), 1, 1, fc = 'green') # green rectangle
pred_rect = patches.Rectangle((0, 0), 1, 1, fc = 'gray') # gray rectangle
plt.legend([loss_rect, gain_rect, pred_rect], ["Net loss", "Net gain", "Predicted"])

# Add labels and title to plot
ax.set_title("Nvidia's Annual Net Income " + "(%d - " % min(yrs) + "%d)" % max(yrs))
ax.set_xlabel('Year')
ax.set_ylabel('Net Income (in millions)')

# Set the background color for the plot
ax.set_facecolor('wheat')

# Adjust y range of plot
ax.set_ylim(min(nis) - 500, max(nis) + 500)

# Make x-axis visible on plot
ax.axhline(0, color = 'black')

# Angle years on x-axis, and only include every other year
plt.xticks(np.arange(min(yrs), max(extended_yrs) + 1, 2.0))
fig.autofmt_xdate()

# Display the plot
plt.show()
