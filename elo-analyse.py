import pickle
from matplotlib import pyplot as plt
import numpy as np

data_filename = 'fide_profiles_2021-02-02-233013.pickle'

# Filter the guessers and people without a rating.
def filter_garbage(p):
	# People without a lichess rating
	if p[0] == 1500:
		return False
	# Guesses and extreme lying.
	if p[1] <= 600 or p[1] >= 2900 or p[1] % 100 == 0:
		return False

	return True

# Filter all the goddamn liars out.
def filter_outliers(p):
	return abs(p[1] - (m*p[0] + b)) <= 800

with open(data_filename, 'rb') as file:
	fide_profiles = pickle.load(file)

'''
i[0]: username
i[1]: lichess bullet
i[2]: lichess blitz
i[3]: lichess rapid
i[4]: lichess classical
i[5]: FIDE
'''
# Create a list of points to plot
points = [(i[2],i[5]) for i in fide_profiles]

# Filter out the garbage values
filtered_points = list(filter(filter_garbage, points))

# Calculate a line of best fit
x,y = zip(*filtered_points)
m,b = np.polyfit(x, y, 1)

# Use the line of best fit to filter out the outliers
filtered_points_outliers = filter(filter_outliers, filtered_points)

# Calculate a new line of best fit for the filtered data
x,y = zip(*filtered_points_outliers)
m,b = np.polyfit(x, y, 1)

# Print dataset size (n), the gradient (m) and the constant (b)
print("n:", len(x), "m:", m, "b:", b)

# Plot the line of best fit
plt.plot([1000,3000], m*np.array([1000,3000]) + b, 'c--')

# Plot the points
plt.scatter(x, y, c='k', marker="s", s=2, edgecolor="None")

# Label the axes
plt.xlabel("Lichess Blitz")
plt.ylabel("FIDE")

# Show the graph
plt.show()
