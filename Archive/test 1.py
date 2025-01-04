import folium
import pandas as pd

# Example data
data = pd.DataFrame({
    'latitude': [37.7749, 34.0522, 40.7128],
    'longitude': [-122.4194, -118.2437, -74.0060],
    'name': ['San Francisco', 'Los Angeles', 'New York']
})

# Create a map
map = folium.Map(location=[37.7749, -122.4194], zoom_start=5)

# Add dots to the map
for _, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(map)

# Save to an HTML file
map.save("map.html")
