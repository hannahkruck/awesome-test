"""Page for viewing the awesome Streamlit vision"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import plotly.graph_objects as go
import pandas as pd
import altair as alt
from altair import Chart, X, Y, Axis, SortField, OpacityValue
import numpy as np

@st.cache
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Home ..."):
        #ast.shared.components.title_awesome("")    #Title Awesome Streamlit ausgeblendet

        # read CSV
        # CSV for Choropleth Map
        df = pd.read_csv("https://raw.githubusercontent.com/hannahkruck/VIS_Test1/Develop/mapNew.csv", encoding ="utf8", sep=";")
        # CSV for Line Map
        df2 = pd.read_csv("https://raw.githubusercontent.com/hannahkruck/VIS_Test1/Develop/mapNew.csv", encoding ="utf8", sep=";")

        # Remove 'overall' and 'Überseeische Länder und Hoheitsgebiet' for both CSV
        indexNames = df[ df['destinationCountry'] == 'Overall' ].index
        df.drop(indexNames , inplace=True)
        indexNames = df[ df['homeCountry'] == 'Overall' ].index
        df.drop(indexNames , inplace=True)

        indexNames = df[ df['destinationCountry'] == 'Überseeische Länder und Hoheitsgebiete' ].index
        df.drop(indexNames , inplace=True)
        indexNames = df[ df['homeCountry'] == 'Überseeische Länder und Hoheitsgebiete' ].index
        df.drop(indexNames , inplace=True)

        indexNames = df2[ df2['destinationCountry'] == 'Overall' ].index
        df2.drop(indexNames , inplace=True)
        indexNames = df2[ df2['homeCountry'] == 'Overall' ].index
        df2.drop(indexNames , inplace=True)

        indexNames = df2[ df2['destinationCountry'] == 'Überseeische Länder und Hoheitsgebiete' ].index
        df2.drop(indexNames , inplace=True)
        indexNames = df2[ df2['homeCountry'] == 'Überseeische Länder und Hoheitsgebiete' ].index
        df2.drop(indexNames , inplace=True)


        st.title("Welcome to the Asylum Seekers EU Information Website")


        # Select map
        selectedMapType = st.sidebar.radio("Map",('Choropleth Map', 'Line Map'))

        if selectedMapType == 'Choropleth Map':
            showChoropleth = True
            showLine = False
        else:
            showLine = True
            showChoropleth = False

        # Filter
        st.sidebar.header("Filters")
        selectedAge = st.sidebar.multiselect("Select Age", ("under 18", "18 - 34", "35 - 64", "over 65"))
        selectedGender = st.sidebar.selectbox("Select Gender", ("All", "Male", "Female"))

        # Filter for Choropleth Map
        st.sidebar.header("Filter for Choropleth Map")
        # Drop down menu for Choropleth Map Information
        selectedMapChoropleth = st.sidebar.selectbox("Select Map Information",('Applications to target countries','Applicants by country of origin'))

        # Filter for Line Map
        st.sidebar.header("Filter for Line Map")
        # Select type
        selectedType = st.sidebar.radio("Select type",('Target country','Origin country'))

        if selectedType == 'Target country':
            selectedType = df.destinationCountry.unique()
            countryCategory = 'destinationCountry'
            selectedLon = 'lonDC'
            selectedLat = 'latDC'
        else:
            selectedType = df.homeCountry.unique()
            countryCategory = 'homeCountry'
            selectedLon = 'lonHC'
            selectedLat = 'latHC'

        # Drop down menu for selected country
        selectedCountryMapLine = st.sidebar.selectbox("Select country",(selectedType))


        #year = 2013 #Platzhalter

        # Information for Choropleth Map based on the chosen map information
        if 'target' in selectedMapChoropleth:
            selectedMapChoropleth = 'destinationCountry'
            selectedCode = 'geoCodeDC'
            mapColor = 'Blues'
        else:
            selectedMapChoropleth = 'homeCountry'
            selectedCode = 'geoCodeHC'
            mapColor = 'Reds'

        # Information for Choropleth Map based on the chosen gender and age
        df['subtotal']=0
        # Check selected gender
        if selectedGender == 'Female':
            # if an age is selected
            if selectedAge:
                # selectedAge is a list of strings
                # Therefore, we have to check every entry in the list and sum up partial results in new column subtotal
                for i in selectedAge:
                    if i == 'under 18':
                        df['subtotal']=df['subtotal']+df['fu18']
                    elif i == '18 - 34':
                        df['subtotal']=df['subtotal']+df['f18']
                    elif i == '35 - 64':
                        df['subtotal']=df['subtotal']+df['f35']
                    elif i == 'over 65':
                        df['subtotal']=df['subtotal']+df['fo65']
            else: # no age is selected, that means the user wants to see all women
                df['subtotal'] = df['subtotal']+df['womenTotal']
            a = 'subtotal'
        elif selectedGender == 'Male':
            if selectedAge:
                for i in selectedAge:
                    if i == 'under 18':
                        df['subtotal']=df['subtotal']+df['mu18']
                    elif i == '18 - 34':
                        df['subtotal']=df['subtotal']+df['m18']
                    elif i == '35 - 64':
                        df['subtotal']=df['subtotal']+df['m35']
                    elif i == 'over 65':
                        df['subtotal']=df['subtotal']+df['mo65']
            else:
                df['subtotal'] = df['subtotal']+df['menTotal']
            a = 'subtotal'
        else: # if no gender is selected, that means the user wants to see all
            if selectedAge:
                for i in selectedAge:
                    if i == 'under 18':
                        df['subtotal']=df['subtotal']+df['mu18']+df['fu18']
                    elif i == '18 - 34':
                        df['subtotal']=df['subtotal']+df['m18']+df['f18']
                    elif i == '35 - 64':
                        df['subtotal']=df['subtotal']+df['m35']+df['f35']
                    elif i == 'over 65':
                        df['subtotal']=df['subtotal']+df['fo65']+df['mo65']
                a = 'subtotal'
            else:
                a = 'total'

        # Group the countries by year and sum up the number (total) in a new column sum (df['sum']
        df['sum']=df.groupby([selectedMapChoropleth,'year'])[a].transform('sum')

        #Datentabelle ausblenden
        #    return df
        # df = load_data()


        # Slider to choose Year for choropleth map
        year = st.slider("", (int(df["year"].min())),(int(df["year"].max())))
        selected_year = year

        # Expander to hide and show informations
        """my_expander = st.beta_expander("Click me to choose a specific year and get information about it", expanded=False)
        with my_expander:
            selected_year = st.slider('%s' % selected_year, (int(df["year"].min())), (int(df["year"].max())),
            step=1)"""


        # Delete all cells, except one year (both maps)
        indexNames = df[ df['year'] != selected_year ].index
        df.drop(indexNames , inplace=True)

        indexNames = df2[ df2['year'] != selected_year ].index
        df2.drop(indexNames , inplace=True)


        # Information for Line Map

        # countryCategory = homeCountry or destinationCountry
        # selectedCountryMapLine is the selected country for the map line (for example Syria (homeCountry))
        indexNames = df2[ df2[countryCategory] != selectedCountryMapLine ].index
        df2.drop(indexNames , inplace=True)

        if selectedGender == 'Female':
            # if an age is selected
            if selectedAge:
                # selectedAge is a list of strings
                # Therefore, we have to check every entry in the list and delete the row if the value in the column for the age is null
                for i in selectedAge:
                    if i == 'under 18':
                        indexNames = df2[ df2['fu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                    elif i == '18 - 34':
                        indexNames = df2[ df2['f18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                    elif i == '35 - 64':
                        indexNames = df2[ df2['f35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                    elif i == 'over 65':
                        indexNames = df2[ df2['fo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
            else:
                indexNames = df2[ df2['womenTotal'] == 0].index
                df2.drop(indexNames , inplace=True)
        elif selectedGender == 'Male':
            for i in selectedAge:
                if i == 'under 18':
                    indexNames = df2[ df2['mu18'] == 0].index
                    df2.drop(indexNames , inplace=True)
                elif i == '18 - 34':
                    indexNames = df2[ df2['m18'] == 0].index
                    df2.drop(indexNames , inplace=True)
                elif i == '35 - 64':
                    indexNames = df2[ df2['m35'] == 0].index
                    df2.drop(indexNames , inplace=True)
                elif i == 'over 65':
                    indexNames = df2[ df2['mo65'] == 0].index
                    df2.drop(indexNames , inplace=True)
            else:
                indexNames = df2[ df2['menTotal'] == 0].index
                df2.drop(indexNames , inplace=True)
        else: # if no gender is selected, that means the user wants to see all
            if selectedAge:
                for i in selectedAge:
                    if i == 'under 18':
                        indexNames = df2[ df2['mu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['fu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                    elif i == '18 - 34':
                        indexNames = df2[ df2['m18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['f18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                    elif i == '35 - 64':
                        indexNames = df2[ df2['m35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['f35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                    elif i == 'over 65':
                        indexNames = df2[ df2['mo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['fo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
            else: # all people are considered
                indexNames = df2[ df2['total'] == 0 ].index
                df2.drop(indexNames , inplace=True)



        st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        #st.markdown(f'<span title="hoveer">ich bin ein test</span>',unsafe_allow_html=True)
        st.subheader('Asylum seekers in Europe in the year %s' % selected_year)

        # Markdown for i-Button
        # CSS and HTML Code
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

        # Text for tooltip
        st.markdown('''
        <div class="tooltip">&#x24D8
        <span class="tooltiptext">
        <b>Choropleth Map</b><br>The Choropleth Map shows the number of asylum applications per country in Europe and the number of refugees per country worldwide for the selected year (see filter 'Select Map Information' for Choropleth Map).
        <br><br>
        <b>Line Map</b><br>The Line Map presents the routes of the refugees depending on the selected type. The type 'target country' shows from which countries the asylum seekers originate based on a specific target country. The type 'origin country' indicates where the asylum seekers are fleeing to from a specific country of origin.
        <br><br>The visualisations can be adjusted using the filters. It should be noted that due to the overview, unknown data as well as data on overseas countries and territories have been removed from the dataset.  In addition, for a few countries only temporary data has been provided.
        </span></div>
        ''', unsafe_allow_html=True)

#----------------Sidebar und Parameter------------------------------

        # Parameterfilter - Nur bestimmte Ziellaender anzeigen lassen
        #country_name_input = st.sidebar.multiselect(
        #'Select Destination Country (funktioniert)',
        #df.groupby('destinationCountry').count().reset_index()['destinationCountry'].tolist())
        # by country name
        #if len(country_name_input) > 0:
        #    df = df[df['destinationCountry'].isin(country_name_input)]
            
        #Vollbild verwenden
        #st.set_page_config(layout="wide")
            
#----------------Create Maps (alt)---------------------------

        # Map with colours (Number of asylum applications)
#           fig = go.Figure(data=go.Choropleth(
#            locations = df['geoCodeDC'],
#            z = df['sum'],
#            text = df['destinationCountry'],
#            colorscale = 'Blues', #Viridis
#            autocolorscale=False,
#            reversescale=False,
#            marker_line_color='darkgray',
#            marker_line_width=0.5,
#            colorbar_tickprefix = '',
#            colorbar_title = 'Number of asylum applications'
#        ))

#        fig.update_layout(
#            title_text='Asylum seekers in Europe in the year %s' % a,
#            geo=dict(
#                showframe=False,
#            showcoastlines=False,
#                projection_type='equirectangular'
#            ),
#            autosize=True,
#            width=1500,
#            height=1080,
#        )
        
        
#----------------Create Maps (Color und Line Map)---------------------------
        
        #Link Toggle Map https://plotly.com/python/custom-buttons/
                # Choropleth Map with colours (Number of asylum applications)


        fig = go.Figure()


        fig.add_trace(
            go.Choropleth(
            locations = df[selectedCode],
            visible=showChoropleth,
            z = df['sum'],
            text = df[selectedMapChoropleth],
            colorscale = mapColor,                   #Magenta
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix = '',
            colorbar_title = 'Number of<br>asylum<br>applications<br>',


        ))


        fig.add_trace(
            go.Scattergeo(
            locationmode = 'country names',
            lon = df2[selectedLon],
            lat = df2[selectedLat],
            hoverinfo = 'text',
            text = df2[countryCategory],
            line = dict(width = 1,color = 'red'),
            opacity = 0.510,
            visible=showLine,
            mode = 'markers',
            marker = dict(
                size = 3,
                color = 'rgb(255, 0, 0)',
                line = dict(
                    width = 3,
                    color = 'rgba(68, 68, 68, 0)',
                ))))


        lons = []
        lats = []
        lons = np.empty(2 * len(df2))
        lons[::2] = df2['lonDC']
        lons[1::2] = df2['lonHC']
        lats = np.empty(2 * len(df2))
        lats[::2] = df2['latDC']
        lats[1::2] = df2['latHC']

        fig.add_trace(
            go.Scattergeo(
                locationmode = 'country names',
                visible= showLine,
                lon = lons,
                lat = lats,
                mode = 'lines',
                line = dict(width = 1,color = 'red'),
                opacity = 0.5
            )
        )

        fig.update_layout(
            showlegend = True,
            geo = go.layout.Geo(
                scope = 'world',
                #projection_type = 'azimuthal equal area',
                showland = True,
                showcountries=True,
                landcolor = 'rgb(243, 243, 243)',
                countrycolor = 'rgb(105,105,105)',
            ),

        )

        # Update figure (Choropleth or Line Map)
        '''
        fig.update_layout(
            
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    active=0,
                    x=0.57,
                    y=1.2,
                    buttons=list([
                        dict(label="Choropleth Map",
                            method="update",
                            args=[{"visible": [True, False, False]},
                                    ]),
                        
                        dict(label="Line Map",
                            method="update",
                            args=[{"visible": [False,True,True]},
                                    ]),
                        
                    ]),
                )
            ]) 
        '''


        fig.update_layout(
            geo=dict(
                showframe=False,            # Map Rahmen ausgeblendet
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            autosize=True,
            #height=800,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
            ),
        )
        
        
        
        st.plotly_chart(fig,use_container_width=True,config=dict(displayModeBar=False))




#Datentabelle einblenden
    #    st.dataframe(data=df)
