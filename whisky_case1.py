# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 16:43:58 2018

@author: sudhanshu kumar sinh
"""
from pandas_prac1 import whisky,correlations
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import output_file,show
import numpy as np

cluster_colors = ["red", "orange", "green", "blue", "purple", "gray"]
regions = ["Speyside", "Highlands", "Lowlands", "Islands", "Campbelltown", "Islay"]

region_colors = {}
for i in range(len(cluster_colors)):
    region_colors[regions[i]]=cluster_colors[i]
print(region_colors)



distilleries = list(whisky.Distillery)
correlation_colors = []
for i in range(len(distilleries)):
    for j in range(len(distilleries)):
        if correlations[i][j] < 0.7 :                # if low correlation,
            correlation_colors.append('white')         # just use white.
        else:                                          # otherwise,
            if whisky.Group[i]==whisky.Group[j]:                # if the groups match,
                correlation_colors.append(cluster_colors[whisky.Group[i]]) # color them by their mutual group.
            else:                                      # otherwise
                correlation_colors.append('lightgray') # color them lightgray.
                
                
source = ColumnDataSource(
    data = {
        "x": np.repeat(distilleries,len(distilleries)),
        "y": list(distilleries)*len(distilleries),
        "colors": correlation_colors,
        "correlations": correlations.flatten(),
    }
)

output_file("Whisky Correlations.html", title="Whisky Correlations")
fig = figure(title="Whisky Correlations",
    x_axis_location="above", tools="reset,hover,save",
    x_range=list(reversed(distilleries)), y_range=distilleries)
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.major_label_text_font_size = "5pt"
fig.xaxis.major_label_orientation = np.pi / 3

fig.rect('x', 'y', .9, .9, source=source,
     color='colors', alpha='correlations')
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {
    "Whiskies": "@x, @y",
    "Correlation": "@correlations",
}
show(fig)

# edit this to make the function `location_plot`.
def location_plot(title,colors):
    output_file(title+".html")
    location_source = ColumnDataSource(
        data={
            "x": whisky[" Latitude"],
            "y": whisky[" Longitude"],
            "colors": colors,
            "regions": whisky.Region,
            "distilleries": whisky.Distillery
        }
    )
    
    fig = figure(title = title,
        x_axis_location = "above", tools="resize, hover, save")
    fig.plot_width  = 400
    fig.plot_height = 500
    fig.circle("x", "y", 10, 10, size=9, source=location_source,
         color='colors', line_color = None)
    fig.xaxis.major_label_orientation = np.pi / 3
    hover = fig.select(dict(type = HoverTool))
    hover.tooltips = {
        "Distillery": "@distilleries",
        "Location": "(@x, @y)"
    }
    show(fig)

region_cols = []
for i in range(len(whisky.Region)):
    region_cols.append(region_colors[whisky.Region[i]])
    
#location_plot("Whisky Locations and Regions", region_cols)
    
region_cols =[region_colors[whisky.Region[i]] for i in range(len(whisky.Region))]
classification_cols =[cluster_colors[whisky.Group[i]] for i in range(len(whisky.Group))]

#location_plot("Whisky Locations and Regions", region_cols)
#location_plot("Whisky Locations and Groups", classification_cols)

