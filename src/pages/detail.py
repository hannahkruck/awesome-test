"""This page is for more details"""
import logging
from typing import List

import streamlit as st

import awesome_streamlit as ast
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Get an instance of a logger
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
def write():
    """Writes content to the app"""
    #ast.shared.components.title_awesome("Detail")      # Titel Awesome_Streamlit
    
    # Page title
    st.title("Detailed view")
    
    # read CSV
    # CSV for Pie Chart
    df = pd.read_csv('https://raw.githubusercontent.com/hannahkruck/awesome-test/master/Piechart.csv',sep = ';')
    

    #-----------------Markdown info-----------------
    st.markdown('''
    <!-- https://www.w3schools.com/css/tryit.asp?filename=trycss_tooltip_transition & https://www.w3schools.com/css/tryit.asp?filename=trycss_tooltip_right-->
    <style>
        .tooltip {
            position: relative;
            display: inline-block;
            font-size:1.6rem;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 50vw;
            background-color: #f1f3f7;
            color: #262730;
            text-align: justify;
            border-radius: 6px;
            padding: 5px;
            font-size:0.9rem;
            
            /* Position the tooltip */
            position: absolute;
            z-index: 1;
            top: -5px;
            left: 105%;
            opacity: 0;
            transition: opacity 0.8s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
    ''', unsafe_allow_html=True)

    st.markdown('''
        <div class="tooltip">&#x24D8
            <span class="tooltiptext">
                <b>Pie Chart</b><br>
                    The pie chart shows the age distribution worldwide for the selected year. 
                <br><br>
                <b>Sankey Diagram</b><br>
                    The Sankey diagram shows the top 10 origin (left) and target (right) countries 
                    as well as the distribution of asylum seekers per year.
            </span>
        </div>
        ''', unsafe_allow_html=True)  

    # read csv
    # old csv  pie structure 
    # df = pd.read_csv('https://raw.githubusercontent.com/hannahkruck/awesome-test/master/Piechart.csv',sep = ';')
    # new csv  pie structure
    df = pd.read_csv('https://raw.githubusercontent.com/hannahkruck/awesome-test/master/Piechart_neu_struk.csv',sep = ';')


    #-----------------Slider-------------------
    # Slider to choose Year for diagramm
    year = st.slider("", (int(df["Year"].min())),(int(df["Year"].max())))
    selected_year = year


    #-----------------Page Layout--------------
    # Layout setting of the page 
    c1, c2 = st.beta_columns((1, 1))
    container = st.beta_container()
    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


    #------------------Create Sankey diagram-------------------------------
    # https://www.geeksforgeeks.org/sankey-diagram-using-plotly-in-python/
    # https://coderzcolumn.com/tutorials/data-science/how-to-plot-sankey-diagram-in-python-jupyter-notebook-holoviews-and-plotly#2
    
    # Variable year for Sankey diagram
    yearVar = selected_year    
                         
    # read sankey csv and data selection
    show_df = pd.read_csv('https://raw.githubusercontent.com/hannahkruck/awesome-test/master/Sankey_Diagramm.csv',sep = ';')

    # year
    yearRows = show_df[show_df['Year'] != yearVar].index
    show_df.drop(yearRows , inplace=True)

    # Nodes, links, colors
    label_souce = show_df['Label_Source'].dropna(axis=0, how='any')
    label_souce2 = []
    elementVar = ''

    for i in label_souce: 
        if(i != elementVar) : 
            label_souce2.append(i)
        elementVar = i

    label_target = show_df['Label_Target'].dropna(axis=0, how='any')
    label = [*label_souce2, *label_target]
    source = show_df['Source'].dropna(axis=0, how='any')
    target = show_df['Target'].dropna(axis=0, how='any')
    value = show_df['Value'].dropna(axis=0, how='any')

    # setting color for node and link
    color_node = [
    # Source order Syria, Afghanistan, Venezuela, Irak, Colombia, Pakistan, Türkei, Nigeria, Iran, Albania
    '#40bf77', '#93beec', '#1ff91f', '#cd8162', '#a6a6a6', '#80e5ff', '#b299e6', '#ff33ff', '#CDC037', '#ff6a6a',
    # Target 
    '#0B2641', '#0B2641', '#0B2641', '#0B2641', '#0B2641', '#0B2641', '#0B2641', '#0B2641', '#0B2641', '#0B2641']
    
    color_link = [
    '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', '#b8e0b8', 
    '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', '#bed8f4', 
    '#bef4be', '#bef4be', '#bef4be', '#bef4be', '#bef4be', '#bef4be', '#bef4be', '#bef4be', '#bef4be', '#bef4be',
    '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1', '#e7c1b1',
    '#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc', '#cccccc', 
    '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff', '#80e5ff',  
    '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb', '#c2adeb',
    '#ffccff', '#ffccff', '#ffccff', '#ffccff', '#ffccff', '#ffccff', '#ffccff', '#ffccff', '#ffccff', '#ffccff', 
    '#ffec80', '#ffec80', '#ffec80', '#ffec80', '#ffec80', '#ffec80', '#ffec80', '#ffec80', '#ffec80', '#ffec80', 
    '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc',]  

    # data to dict, dict to sankey
    link = dict(source = source, target = target, value = value, color = color_link)
    node = dict(label = label, pad = 20, thickness = 10, color = color_node)
    layout = dict(
        height = 800, 
        font = dict(
            size = 11),)
    
    data = go.Sankey(link = link, node=node)
    
    # properties sanky diagram layout 
    fig2 = go.Figure(data, layout= layout)

    #-----------------Create pie chart-------------------
    # https://jasonxqh.github.io/2020/07/12/plotly基础/
    
    # read csv for pie chart
    df = pd.read_csv('https://raw.githubusercontent.com/hannahkruck/awesome-test/master/Piechart.csv',sep = ';')
	
    # show specific value if a choosen year is selected on slider
    labels = df['year'].tolist()
    if selected_year == 2010:
            values = df['2010'].tolist()
    if selected_year == 2011:
            values = df['2011'].tolist()     
    if selected_year == 2012:
            values = df['2012'].tolist()       
    if selected_year == 2013:
            values = df['2013'].tolist()
    if selected_year == 2014:
            values = df['2014'].tolist()
    if selected_year == 2015:
            values = df['2015'].tolist()
    if selected_year == 2016:
            values = df['2016'].tolist()
    if selected_year == 2017:
            values = df['2017'].tolist()
    if selected_year == 2018:
            values = df['2018'].tolist()
    if selected_year == 2019:
            values = df['2019'].tolist()
            
    # define color sets 
    colors = ['#e6f2ff', '#b3d9ff', '#80bfff', '#3386E6']

    # create pie figure
    fig1 = go.Figure(data=[go.Pie(
            labels = labels, 
            values = values, 
            insidetextorientation = 'radial',
            hole = 0.399,)])

    # update settings hover and text informations
    fig1.update_traces(
            hoverinfo = 'label+percent+value', 
            textinfo = 'percent+label',
            textfont_size = 11,
            marker = dict(colors = colors, 
            line = dict(color = 'lightskyblue', width = 0.1)))  
	
    # update settings layout
    fig1.update_layout(dict(
        height = 600, 
        font = dict(
            size = 12)))

    # add annotations in the center of the donut pie
    fig1.update_layout(
    annotations=[dict(
            text='<b>Age<br> Distribution</b>', 
            font_size=12, 
            showarrow=False),])

#------------Create Timeline Years V. 2.0-------------------
    # read CSV for the histogram graph
    df = pd.read_csv("https://raw.githubusercontent.com/hannahkruck/awesome-test/master/Histogramm.csv",encoding ="utf8", sep = ";")
    # use years for the x-axis and the worldwide amount of asylum applications for the y-axis
    fig3 = go.Figure(go.Scatter(x = df['year'], y = df['asylum_applications_worldwide']))
    # customizing the graph
    fig3.update_layout(
    # customize width
        #autosize=False,
        width=1900,
        height=100,
    # hide labels
        yaxis={'visible': False, 'showticklabels': False
        },
    # show every year as a label below
        xaxis={'type': 'category'},
    # create white background to match with initial background of streamlit
        plot_bgcolor='rgb(255,255,255)',
    # set all margins and padding to zero to create full width graph
        margin=go.layout.Margin(
        l=0,
        r=35,
        b=0,
        t=0,
        pad = 0
    )
)
#------------Create Slider Years V. 2.0-------------------

    with c1:
        st.subheader('Asylum seekers by age in Europe in the year %s' % selected_year) 
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.subheader('Top 10 Distribution of a Countries Asylum Applications among the various Countries of Destination  %s' % selected_year)
        st.plotly_chart(fig2, use_container_width=True)
    with container:
        st.plotly_chart(fig3, use_container_width=True)
      
if __name__ == "__main__":
    write()