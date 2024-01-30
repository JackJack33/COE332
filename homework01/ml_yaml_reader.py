import yaml
import numpy as np

def countUniqueEntries(arr, key):
    unique = {}
    for x in arr:
        if not x[key] in unique:
            unique[x[key]] = 1
        else:
            unique[x[key]] += 1
    return unique

def customSign(num): # edge case insurance
    if num == 0:
        return np.sign(num-1)
    else:
        return -np.sign(num)

ml_data = {}
with open('Meteorite_Landings.yaml', 'r') as f:
    ml_data = yaml.load(f, Loader=yaml.SafeLoader)

data = {}
data['meteorite_landings'] = []
for landing in ml_data['meteorite_landings']:
    data['meteorite_landings'].append({
        'name': landing['name'],
        'id': int(landing['id']),
        'recclass': landing['recclass'],
        'mass (g)': float(landing['mass (g)']),
        'reclat': float(landing['reclat']),
        'reclong': float(landing['reclong']),
        'geolocation': landing['GeoLocation']
    })


stat_entries = len(data['meteorite_landings'])
stat_class = countUniqueEntries(data['meteorite_landings'], 'recclass')
stat_avgMass = 0.0
stat_maxMass = [data['meteorite_landings'][0]['mass (g)'], data['meteorite_landings'][0]['name']]
stat_minMass = [data['meteorite_landings'][0]['mass (g)'], data['meteorite_landings'][0]['name']]
stat_hemisphere = [0,0,0,0] # [N,E,S,W]

for landing in data['meteorite_landings']:
    stat_avgMass += landing['mass (g)'] / stat_entries
    if landing['mass (g)'] > stat_maxMass[0]:
        stat_maxMass = [landing['mass (g)'], landing['name']]
    if landing['mass (g)'] < stat_minMass[0]:
        stat_minMass = [landing['mass (g)'], landing['name']]

    hemi_lat = int(customSign(landing['reclat'])) + 1
    hemi_long = int(customSign(landing['reclong'])) + 2
    stat_hemisphere[hemi_lat] += 1
    stat_hemisphere[hemi_long] += 1

print(f'Number of Entries: {stat_entries}')
print(f'Unique Classes: {len(stat_class)}')
print(f'Average Mass: {stat_avgMass}g')
print(f'Largest: {stat_maxMass[1]}, {stat_maxMass[0]}g')
print(f'Smallest: {stat_minMass[1]}, {stat_minMass[0]}g')
print(f'Hemisphere Counts:\nN: {stat_hemisphere[0]}\nE: {stat_hemisphere[1]}\nS: {stat_hemisphere[2]}\nW: {stat_hemisphere[3]}')
