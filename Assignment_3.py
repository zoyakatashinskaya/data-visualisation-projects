import pandas as pd 
import numpy as np
import bokeh.palettes as bp
from bokeh.palettes import inferno
from bokeh.plotting import figure, output_notebook
from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, RangeTool
from bokeh.transform import linear_cmap
from bokeh.layouts import gridplot, column


# ==========================================================================
# Goal: Visualize Covid-19 Tests statistics in Switzerland with linked plots
# Dataset: covid19_tests_switzerland_bag.csv
# Data Interpretation: 
# 		n_negative: number of negative cases in tests
# 		n_positive: number of positive cases in tests
# 		n_tests: number of total tests
# 		frac_negative: fraction of POSITIVE cases in tests
# ==========================================================================



### Task1: Data Preprocessing


## T1.1 Read the data to the dataframe "raw"
# You can read the latest data from the url, or use the data provided in the folder (update Nov.3, 2020)

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_tests_switzerland_bag.csv?raw=true'
raw = pd.read_csv(url, index_col=0)
# print(raw.head(10))


## T1.2 Create a ColumnDataSource containing: date, positive number, positive rate, total tests
# All the data can be extracted from the raw dataframe.
date = list(pd.to_datetime(raw['date']))
# print(date[:10])
pos_num = raw['n_positive'].tolist()
test_num = raw['n_tests'].tolist()
pos_rate = [round(a/b, 4) for a, b in zip(pos_num, test_num)]
# print(pos_rate[60:70])


source = ColumnDataSource(dict(
    date = date,
    positive = pos_num,
    total = test_num,
    pos_rate = pos_rate
))

## T1.3 Map the range of positive rate to a colormap using module "linear_cmap"
# "low" should be the minimum value of positive rates, and "high" should be the maximum value

color_palette = list(inferno(256))
# https://docs.bokeh.org/en/latest/docs/reference/palettes.html
# print(len(color_palette))
# print(color_palette[:10])

mapper = linear_cmap('pos_rate', color_palette, min(pos_rate), max(pos_rate))
# linear_cmap(field_name, palette, low, high, low_color=None, high_color=None, nan_color='gray')[source]


## Task2: Data Visualization
# Reference link:
# (range tool example) https://docs.bokeh.org/en/latest/docs/gallery/range_tool.html?highlight=rangetool


## T2.1 Covid-19 Total Tests Scatter Plot
# x axis is the time, and y axis is the total test number. 
# Set the initial x_range to be the first 30 days.

TOOLS = "box_select,lasso_select,wheel_zoom,pan,reset,help"
p = figure(x_axis_type="datetime", x_range=(date[0], date[30]), tools=TOOLS)
p.scatter(x="date", y="total", marker="circle", fill_color=mapper, size = 8,
         source=source)

p.title.text = 'Covid-19 Tests in Switzerland'
p.yaxis.axis_label = "Total Tests"
p.xaxis.axis_label = "Date"
p.sizing_mode = "stretch_both"

# Add a hovertool to display date, total test number
hover = HoverTool(
    tooltips=[
                ('date', '@date{%F}'),
                ('test', '@total'), 
            ],
    formatters={'@date': 'datetime'},
)
p.add_tools(hover)


## T2.2 Add a colorbar to the above scatter plot, and encode 
# positve rate values with colors; please use the color mapper defined in T1.3 

color_bar = ColorBar(color_mapper=mapper['transform'], location=(0,0), width=15, 
                     title = 'P_rate')
p.add_layout(color_bar, 'right')


## T2.3 Covid-19 Positive Number Plot using RangeTool
# In this range plot, x axis is the time, and y axis is the positive test number.
select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_width=800, height=300, 
                x_axis_type="datetime", 
                tools="", toolbar_location=None)

# Define a RangeTool to link with x_range in the scatter plot
range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "green"
range_tool.overlay.fill_alpha = 0.2

# Draw a line plot and add the RangeTool to the plot
select.line('date', 'positive', source=source)
select.yaxis.axis_label = "Positive Cases"
select.xaxis.axis_label = "Date"

select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool


# Add a hovertool to the range plot and display date, positive test number
hover2 = HoverTool(
    tooltips=[
                ('date', '@date{%F}'),
                ('positive', '@positive'), 
            ],
    formatters={'@date': 'datetime'},
)
select.add_tools(hover2)

## T2.4 Layout arrangement and display

linked_p = column(p, select)
show(linked_p)
output_file("dvc_ex3.html")
save(linked_p)