from haversine import haversine
cities={'NYC':[40.7587,-73.984509,6, 2000], 'SF':[37.745764,-122.441638,9, 2000], 'LA:':[34.040884,-118.38861,11,10000], 'CHI':[41.910326,-87.677447, 6, 8500]}
def hotspots(lat, lon):
	for city in cities:
		if haversine(float(lat), float(lon), city[0],city[1])<city[2]:
                newradius=city[3]
		else:
			pass
	return newradius