import pandas as pd 
from math import pi
import numpy as np
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange
import bokeh.palettes as bp
from bokeh.palettes import inferno
 
# Goal: Draw a line chart displaying averaged daily new cases for all cantons in Switzerland.
# Dataset: covid19_cases_switzerland_openzh-phase2.csv
# Interpretation: value on row i, column j is either the cumulative covid-19 case number of canton j on date i or null value




### Task 1: Data Preprocessing


## T1.1 Read data into a dataframe, set column "Date" to be the index 

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_cases_switzerland_openzh-phase2.csv?raw=true'

raw = pd.read_csv(url, index_col=0)


# Initialize the first row with zeros, and remove the last column 'CH' from dataframe
raw.drop(raw.iloc[:, 26:], inplace = True, axis = 1)
# raw = raw.drop(columns="CH")
raw.loc["2020-05-31"] = 0.0 # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
# raw["Date"] = 0 #inserts raw at the end
# val = [0] * 27
# raw.insert(loc=0, column = "A", value = 0)


# Fill null with the value of previous date from same canton
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
raw = raw.fillna(method='ffill')

# T1.2 Calculate and smooth daily case changes

# # Compute daily new cases (dnc) for each canton, e.g. new case on Tuesday = case on Tuesday - case on Monday;
# # Fill null with zeros as well
dnc = raw.diff()
dnc.loc["2020-05-31"] = 0.0
# print(dnc.head(10))


# # TODO: Smooth daily new case by the average value in a rolling window, and the window size is defined by step
# # Why do we need smoothing? How does the window size affect the result?
# # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
step = 3
dnc_avg = dnc.rolling(step).mean()
# print(dnc_avg.head(20))


# ## TODO: T1.3 Build a ColumnDataSource 

# # Extract all canton names and dates
# # NOTE: be careful with the format of date when it is used as x input for a plot
cantons = list(dnc.columns)
# print(cantons)
date = list(dnc.index)
# print(date)

# Create a color list to represent different cantons in the plot, you can either construct your own color patette or use the Bokeh color pallete
color_palette = inferno(26)
# print(color_palette)

# Build a dictionary with date and each canton name as a key, i.e., {'date':[], 'AG':[], ..., 'ZH':[]}
# For each canton, the value is a list containing the averaged daily new cases
source_dict = {'date' : date}
for canton in cantons:
    source_dict[canton] = dnc_avg[canton].tolist()
# for key, value in source_dict.items():
#     print(key, ' : ', value)

source = ColumnDataSource(data=source_dict)



# ### TODO: Task 2: Data Visualization

# ## T2.1: Draw a group of lines, each line represents a canton, using date, dnc_avg as x,y. Add proper legend.
# # https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/line.html?highlight=line#bokeh.models.glyphs.Line
# # https://docs.bokeh.org/en/latest/docs/user_guide/interaction/legends.html

p = figure(plot_width=1000, plot_height=800, x_axis_type="datetime") #tooltips=TOOLTIPS)
p.title.text = 'Daily New Cases in Switzerland'

# lines = []
# for canton,color in zip(cantons,color_palette): 
# 	lines.append(...)

df = pd.DataFrame(source_dict)

for canton, color in zip(cantons,color_palette):
    df['date'] = pd.to_datetime(df['date'])
    p.line(df['date'], df[canton], line_width=2, color=color, alpha=0.8, legend_label=canton)

# # Make the legend of the plot clickable, and set the click_policy to be "hide"

p.legend.location = "top_left"
p.legend.click_policy="hide"


# ##TODO:  T2.2 Add hovering tooltips to display date, canton and averaged daily new case

# # (Hovertip doc) https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# # (Date hover)https://stackoverflow.com/questions/41380824/python-bokeh-hover-date-time
hover = HoverTool(
            tooltips=[
                ( 'date',   '@x{%F}'            ),
                ( 'canton',  canton ), # use @{ } for field names with spaces
                ( 'cases', '@y'),
            ],

            formatters={
                '@x'        : 'datetime', # use 'datetime' formatter for '@date' field
                '@{adj cases}' : 'printf',   # use 'printf' formatter for '@{adj close}' field
                                            # use default 'numeral' formatter for other fields
            },

            # display a tooltip whenever the cursor is vertically in line with a glyph
            # mode='vline'
)


p.add_tools(hover)

show(p)
output_file("dvc_ex2.html")
save(p)

# hide / mute glyphs - https://docs.bokeh.org/en/latest/docs/user_guide/interaction/legends.html 













