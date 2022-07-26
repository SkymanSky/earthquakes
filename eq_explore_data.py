
import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
from datetime import datetime

filename='data/eq_data_30_day_significiant.json'

with open(filename,encoding="utf8") as f:
    all_eq_data=json.load(f)

readable_file='data/readable_eq_data.json'

with open(readable_file,'w') as f:
    json.dump(all_eq_data, f,indent=4)

all_eq_dicts=all_eq_data['features']
print(len(all_eq_dicts))

dates,mags,lons,lats,hover_texts=[],[],[],[],[]

for eq_dict in all_eq_dicts:
    mag=eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat=eq_dict['geometry']['coordinates'][1]
    title=eq_dict['properties']['title']
    time=eq_dict['properties']['time']/1000
    date=datetime.fromtimestamp(time).date()
    title+=f" - {date}"
    mags.append(mag)
    lons.append(lon)
    lats.append(lat)
    dates.append(date)
    hover_texts.append(title)

print(mags[:10])
print(lons[:5])
print(lats[:5])

#Depremlerin haritasını çıkar.
data=[{
        'type':'scattergeo',
        'lon':lons,
        'lat':lats,
        'text':hover_texts,
        'marker':{
            'size':[5*mag for mag in mags],
            'color':mags,
            'colorscale':'Viridis',
            'reversescale':False,
            'colorbar':{'title':'Magnitude'},
        },
}]

title=all_eq_data['metadata']['title']
my_layout=Layout(title=title)

fig={'data':data,'layout':my_layout}
offline.plot(fig, filename='global_earthquakes.html')