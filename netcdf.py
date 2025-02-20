import numpy as np
from netCDF4 import Dataset
import datetime

index_date = datetime.datetime(1900, 1, 1)  # Start date of interest

start_date = datetime.datetime(2005, 3, 2)  # Start date of interest
end_date = datetime.datetime(2005, 3, 17)  # End date of interest

start_timestamp = int((start_date - index_date).total_seconds())  # Convert to minutes
end_timestamp = int((end_date - index_date).total_seconds())  # Convert to minutes

# Load the NetCDF file
filename = 'reanalysis_waterlevel_10min_2005_03_v2.nc'  # Replace with your actual file path
dataset = Dataset(filename, 'r')

# Print available variables to understand the structure
print(dataset.variables.keys())

# Define your area of interest (latitude and longitude bounds)
lat_min, lat_max = -38.4076, -38.3200
lon_min, lon_max = 147.2000, 148.2000

# Extract latitude and longitude variables
latitudes = dataset.variables['station_y_coordinate'][:]
longitudes = dataset.variables['station_x_coordinate'][:]

# Find indices for the specified area
lat_indices = np.where((latitudes >= lat_min) & (latitudes <= lat_max) & (longitudes >= lon_min) & (longitudes <= lon_max))[0]
lon_indices = np.where((longitudes >= lon_min) & (longitudes <= lon_max))[0]

# Extract the 'tide+rise+surge' variable
tide_rise_surge = dataset.variables['waterlevel']

print(lat_indices)
#print(lon_indices)  # Check the shape of the variable

# Initialize an empty list to store results
results = []

# Loop through time and extract data at 10-minute intervals for the specified area
for time_index in range(len(dataset.variables['time'])):
    if (dataset.variables['time'][time_index] >= start_timestamp) & (dataset.variables['time'][time_index] <= end_timestamp):
        date_time = index_date + datetime.timedelta(seconds=int(dataset.variables['time'][time_index]))
        formatted_date = date_time.strftime('"%Y-%m-%d %H:%M"')
        value1 = tide_rise_surge[time_index, 8803]
        value2 = tide_rise_surge[time_index, 35777]
        results.append((formatted_date, latitudes[8803], longitudes[8803], value1))
        results.append((formatted_date, latitudes[35777], longitudes[35777], value2))

# Save results to a text file
with open('tide_rise_surge_subset.txt', 'w') as f:
    for time, lat, lon, val in results:
        f.write(f"{time}, {lat}, {lon}, {val}\n")

# Close the dataset
dataset.close()
