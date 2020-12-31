"""Page for viewing the awesome Streamlit vision"""
import pathlib
import streamlit as st
import awesome_streamlit as ast
import plotly.graph_objects as go
import pandas as pd
import altair as alt
from altair import Chart, X, Y, Axis, SortField, OpacityValue
import numpy as np
# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Loading Map ..."):
        #ast.shared.components.title_awesome("")    #Title Awesome Streamlit ausgeblendet

        # read CSV
        # CSV for Choropleth Map
        df = pd.read_csv("https://raw.githubusercontent.com/hannahkruck/awesome-test/Master/Map.csv", encoding ="utf8", sep=";")
        # CSV for Line Map
        df2 = pd.read_csv("https://raw.githubusercontent.com/hannahkruck/awesome-test/Master/Map.csv", encoding ="utf8", sep=";")

        # Title
        st.title("Map view")

#----------------- Side bar (filter options) -------------------

        # Select map (Choropleth or Line Map)
        selectedMapType = st.sidebar.radio("Map",('Choropleth Map', 'Line Map'))
        if selectedMapType == 'Choropleth Map':
            showChoropleth = True
            showLine = False
        else:
            showLine = True
            showChoropleth = False

        # General filter (Age, Gender)
        st.sidebar.header("Filters")
        selectedAge = st.sidebar.multiselect("Select Age", ("under 18", "18 - 34", "35 - 64", "over 65"))
        selectedGender = st.sidebar.selectbox("Select Gender", ("All", "Male", "Female"))

        # Special filter for Choropleth Map
        st.sidebar.header("Filter for Choropleth Map")
        # Drop down menu for Choropleth Map Information
        selectedMapChoropleth = st.sidebar.selectbox("Select Map Information",('Applications to target countries','Applicants by country of origin'))
        # Information for Choropleth Map based on the chosen map information
        if 'target' in selectedMapChoropleth:
            selectedMapChoropleth = 'destinationCountry'
            selectedCode = 'geoCodeDC'
            mapColor = 'Blues'
        else:
            selectedMapChoropleth = 'homeCountry'
            selectedCode = 'geoCodeHC'
            mapColor = 'Reds'

        # Special filter for Line Map
        st.sidebar.header("Filter for Line Map")
        # Select type (show routes of asylum seeker from a particular origin country or to a particular target country)
        selectedType = st.sidebar.radio("Select type",('Target country','Origin country'))
        if selectedType == 'Target country':
            selectedType = df.destinationCountry.unique()
            countryCategory = 'destinationCountry'
            namesToShow = 'homeCountry'
            selectedLon = 'lonDC'
            selectedLat = 'latDC'
        else:
            selectedType = df.homeCountry.unique()
            countryCategory = 'homeCountry'
            namesToShow = 'destinationCountry'
            selectedLon = 'lonHC'
            selectedLat = 'latHC'
        # Drop down menu for selected country
        selectedCountryMapLine = st.sidebar.selectbox("Select country",(selectedType))


#----------------- Website content (Year slider, i-Button) -------------------

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
        
        </span></div>
        ''', unsafe_allow_html=True)

        # Slider to choose the year
        selected_year = st.slider("", (int(df["year"].min())),(int(df["year"].max())))

        # Title for map regarding the chosen year
        st.subheader('Asylum seekers in the year %s' % selected_year)


#----------------- Data preparation (general) -------------------

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

        # Delete all cells, except one year (both maps)
        indexNames = df[ df['year'] != selected_year ].index
        df.drop(indexNames , inplace=True)

        indexNames = df2[ df2['year'] != selected_year ].index
        df2.drop(indexNames , inplace=True)


#----------------- Data preparation (Choropleth Map) -------------------

        # Information for Choropleth Map (df) based on the chosen gender and age
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



#----------------- Data preparation (Line Map) -------------------

        # countryCategory = homeCountry or destinationCountry
        # selectedCountryMapLine is the selected country for the map line (for example Syria (homeCountry))
        indexNames = df2[ df2[countryCategory] != selectedCountryMapLine ].index
        df2.drop(indexNames , inplace=True)

        df2['subtotal'] = 0

        if selectedGender == 'Female':
            # if an age is selected
            if selectedAge:
                # selectedAge is a list of strings
                # Therefore, we have to check every entry in the list and delete the row if the value in the column for the age is null
                for i in selectedAge:
                    if i == 'under 18':
                        indexNames = df2[ df2['fu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['fu18']
                    elif i == '18 - 34':
                        indexNames = df2[ df2['f18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['f18']
                    elif i == '35 - 64':
                        indexNames = df2[ df2['f35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['f35']
                    elif i == 'over 65':
                        indexNames = df2[ df2['fo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['fo18']
            else:
                indexNames = df2[ df2['womenTotal'] == 0].index
                df2.drop(indexNames , inplace=True)
                df2['subtotal']=df2['subtotal']+df2['womenTotal']
        elif selectedGender == 'Male':
            if selectedAge:
                # selectedAge is a list of strings
                # Therefore, we have to check every entry in the list and delete the row if the value in the column for the age is null
                for i in selectedAge:
                    if i == 'under 18':
                        indexNames = df2[ df2['mu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['mu18']
                    elif i == '18 - 34':
                        indexNames = df2[ df2['m18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['m18']
                    elif i == '35 - 64':
                        indexNames = df2[ df2['m35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['m35']
                    elif i == 'over 65':
                        indexNames = df2[ df2['mo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['mo18']
            else:
                indexNames = df2[ df2['menTotal'] == 0].index
                df2.drop(indexNames , inplace=True)
                df2['subtotal']=df2['subtotal']+df2['menTotal']
        else: # if no gender is selected, that means the user wants to see all
            if selectedAge:
                for i in selectedAge:
                    if i == 'under 18':
                        indexNames = df2[ df2['mu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['fu18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['mu18']+df2['fu18']
                    elif i == '18 - 34':
                        indexNames = df2[ df2['m18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['f18'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['m18']+df2['f18']
                    elif i == '35 - 64':
                        indexNames = df2[ df2['m35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['f35'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['m35']+df2['f35']
                    elif i == 'over 65':
                        indexNames = df2[ df2['mo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        indexNames = df2[ df2['fo65'] == 0].index
                        df2.drop(indexNames , inplace=True)
                        df2['subtotal']=df2['subtotal']+df2['mo65']+df2['fo65']
            else: # all people are considered
                indexNames = df2[ df2['total'] == 0 ].index
                df2.drop(indexNames , inplace=True)

        # Create list of origin or target countries to display them in hover text
        # Every second index must contain the country name, so a placeholder is necessary in front of it
        # Structur: [placeholder,name+number,placeholder,name+number,...]
        # name = listPlaceholderNames
        # number = listPlaceholderNumber
        
        listPlaceholderNames = df2[namesToShow].values.tolist()
        listPlaceholderNumber = df2[a].values.tolist()

        nameList = []
        i = 0
        if namesToShow == 'homeCountry':
            for x in listPlaceholderNames:
                nameList.append(i)
                x = x +': '+ str(listPlaceholderNumber[i])
                nameList.append(x)
                i = i+1
            if len(nameList) != 0:
                nameList[-2]=None
        else:
            for x in listPlaceholderNames:
                x = x +': '+ str(listPlaceholderNumber[i])
                nameList.append(x)
                nameList.append(i)
                i = i+1
            if len(nameList) != 0:
                nameList[-1]=None


        st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        
#----------------Create Maps with Plotly (Choropleth and Line Map)---------------------------
        
        #Link Toggle Map https://plotly.com/python/custom-buttons/

        fig = go.Figure()

        # Choropleth Map
        fig.add_trace(
            go.Choropleth(
            locations = df[selectedCode],
            visible=showChoropleth,
            z = df['sum'],
            text = df[selectedMapChoropleth],
            colorscale = mapColor,
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix = '',
            colorbar_title = 'Number of<br>asylum<br>applications<br>',
        ))

        # Line Map
        fig.add_trace(
            go.Scattergeo(
            locationmode = 'country names',
            lon = df2[selectedLon],
            lat = df2[selectedLat],
            hoverinfo = 'text',
            name=selectedCountryMapLine,
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

        #hallo = 'testi'

        fig.add_trace(
            go.Scattergeo(
                locationmode = 'country names',
                visible= showLine,
                name='route and number <br>of asylum seekers',
                text=nameList,
                hovertemplate=nameList,
                lon = lons,
                lat = lats,
                mode = 'markers+lines',
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

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            autosize=True,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
            ),
        )

        # Display figure
        st.plotly_chart(fig,use_container_width=True,config=dict(displayModeBar=False))
