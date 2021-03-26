import pandas as pd 
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined

output_file("dvc_ex1.html")
### Task 1: Data Preprocessing
 

## T1.1 Read online .csv file into a dataframe using pandas
# Reference links: 
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas 
# about pandas DataFrame - https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm

original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv?raw=true'
df = pd.read_csv(original_url, index_col=0)
#print(df)
##print(df.head(5))


## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting: 
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped


# Filter out rows containing 'CH' 
df = df[df.canton != "CH"]
#print(df['canton'])

# Extract unique value lists of canton, age_group and sex
cantons = df['canton'].unique()
#print(cantons)
age_group = df['age_group'].unique()
#print(age_group)
sex = df['sex'].unique()
#print(sex)


# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]
factors = []
for canton in cantons:
    for age in age_group:
        factors.append((canton, age))
#print(factors) # [('AG', '0 - 9'), ('AG', '10 - 19'), ... ('ZH', '80+')]

# Use genders as stack names
stacks = ['male','female']

# Calculate total population size as the value for each stack identified by canton,age_group and sex
#stack_val = ...
df = df.groupby(['canton','age_group', 'sex'])['pop_size'].sum().reset_index()
male = []
female = []
for i in range(len(df)):
    if df.loc[i, "sex"] == "Männlich":
        male.append(df.loc[i, "pop_size"])
    else: 
        female.append(df.loc[i, "pop_size"])
#print(male[:5]) #[36330, 34556, 42119, 48915, 48236 ...]
#print(female[:5]) #[34179, 32180, 39744, 46987, 46889 ...]
#print(df.head()) #AG     0 - 9  Männlich     36330

# Build a ColumnDataSource using above information
source = ColumnDataSource(data=dict(
    x=factors,
    male= male,
    female= female,
))




### Task 2: Data Visualization
## another approach 
#group = df.groupby(by = ['canton','age_group'])
#p=figure(x_range=group, plot_height=500, plot_width=800, title='Canton Population Visualization')

## T2.1: Visualize the data using bokeh plot functions
p=figure(x_range=FactorRange(*factors), plot_height=500, plot_width=800, title='Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = 1.2


p.vbar_stack(stacks, x='x', width=0.8, alpha=0.5, color=["#3288bd", "#fc8d59"], source=source,
             legend_label=stacks)

p.legend.location = "top_center"
p.legend.orientation = "horizontal"



## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart


hover = HoverTool(tooltips=[
    ("gender", "$name"),
    ("canton, age group", "@x"),
    ("population", "@$name"),
])
p.add_tools(hover)
show(p)


## T2.3 Save the plot as "dvc_ex1.html" using output_file


