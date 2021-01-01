"""This page is for searching and viewing the list of awesome resources"""
import logging

import streamlit as st

import awesome_streamlit as ast
from awesome_streamlit.core.services import resources

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import base64


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
def write():
	
	#ast.shared.components.title_awesome("Welcome")      # Titel Awesome_Streamlit ausblenden
	
	#-----------CSS Startseite------------
	st.markdown("""
	<style>
		body {
			color: black;
			font-color: black;
			background-color: white;
  			/*background: #e6f2ff;*/
		}
		#h1 {
			text-align: center;
		}
		/* Navigationsueberschrift mittig
		h1 {
			text-align: center;
		}*/
		h3 {
			text-align: justify;
			text-align: center;*/
		}
		p {
			text-align: justify; 
		}
		#text {
			color: #06648c; /*#1878a1;*/
			font-weight:normal;
		}
		#expand_three {
			color: #1878a1;
			font-size: 18px;
		}
		#aufzaehlung {
			margin-left: 30px;
		}
		
	</style>
	
    """, unsafe_allow_html=True)
	
	# title of the page
	#st.title("Welcome to visuasyl")

	# html markdown text
	html = """
		<h1 id=h1><b>Welcome to VISUASYL</b><h1>
		<h3 id=text><b>VISUASYL</b> is an interactive visualisation tool that visually illustrates information about asylum applications and the development in Europe. 
			<br>The aim of VISUASYL is to provide users with an insight and overview of the number of annual asylum applications and migration in Europe 
			between 2010 and 2019, using different visualisation methods. 
			<br>VISUASYL was mainly developed for political parties, politicians and non-governmental organisations (NGOs). 
			Because of the simple functionalities, VISUASYL can also be used by non-experts and interested parties.	
			<br>
		</h3>
	<hr>
	"""
	st.markdown(html, unsafe_allow_html=True)
	
	# expander 1 to open and close informations
	my_expander_three = st.beta_expander("Informations and interaction options of VISUASYL", expanded=False)
	with my_expander_three:
		html_three = """ 
			<b id=expand_three>Informations</b>
			<br>VISUASYL uses visualisation methods to provide an overview of the number of annual asylum applications and migration in Europe. The diagrams and the information they provide are described below.
			
			<div id=aufzaehlung>
				<u>Chorpleth Map</u>:<br>
					<ul>
						<li>The number of asylum applications per country in Europe and the number of refugees per country worldwide for the selected year.
						</li>
					</ul>
				<u>Line Map</u>:
					<ul>
						<li>Route of the refugees: From which countries the asylum seekers originate in relation to a specific country and 
						where the asylum seekers are fleeing from in relation to a particular country of origin.
						</li>
					</ul>
				<u>Pie Chart</u>:<br>
					<ul>
						<li>Represents the age distribution worldwide for the selected year. 
						</li>
					</ul>
				<u>Sankey Diagram</u>:<br>
					<ul>
						<li>Shows the distribution of asylum applications from the different countries of origin to the different countries of destination. 
						Also the Top 10 destination countries of a year are illustrated here. 
						</li>
					</ul>
				<u>Time graph</u>:<br>
					<ul>	
						<li>Shows the total number of asylum applications over the years.			
						</li>
					</ul>
			</div>
			<br><b id=expand_three>Interaction Options</b><br>
				VISUASYL contains a navigation bar that allows users to switch between the <i>Welcome, Map and Detail page</i>. 
				The tool also offers users various ways to interact with the diagrams. Some charts allows users to show more information by hovering above the diagram or hide some informations 
				by clicking on the legends of an diagram to highlight certain information. Other charts such as the maps offer greater interaction possibilities by allowing users to select filters or parameter settings to obtain specific information, e.g. on a country, citizenship, age or gender. 
				<br>
				The following filtering options for the maps are available to users in the navigation bar:
			<div id=aufzaehlung>
				<ul><li>Switching between the choropleth and line map </li></ul>
				<ul><li>Filtering the map by selecting Age, Gender </li></ul>
				<ul><li>Special filters for the Choropleth Map: Application to target country, Application by country of origin </li></ul>
				<ul><li>Special filters for the  Line Map: Select a Type for Map (Target or Origin Country), Select a specific Country </li></ul>
			</div>
			By adjusting the time slider, users can update the data of the charts to the selected year.
			<br><br>"""
		st.markdown(html_three, unsafe_allow_html=True)


	# expander 2 to open and close informations
	my_expander_one = st.beta_expander("Source of the dataset", expanded=False)
	with my_expander_one:
		html_one = """ 
			<p>The dataset used to create the visualisation tool was provided by Eurostat, the statistical office of the European Union.
			Eurostat is an administrative unit of the European Union with the mission to produce official European statistics.
			<br>These data are provided by the national ministries of the interior and related official institutions.  
			<br>Link to the Dataset: <a target="_blank" href="https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=migr_asyappctza&lang=de">Asylum and first time asylum applicants by citizenship, age and sex - annual aggregated data (rounded)<br></a>
			<br>
			</p>"""
		st.markdown(html_one, unsafe_allow_html=True)
	
	# expander 3 to open and close informations
	my_expander_two = st.beta_expander("Implementation and sharing of our visualisation tool", expanded=False)
	with my_expander_two:
		html_two = """ 
			<p> The visualisation tool was implemented with the open source framework <a target="_blank" href="https://www.streamlit.io"><b> Streamlit</b></a>.<br> 
			Streamlit is both a library and a framework for Python. 
			It allows users to create and publish interactive web apps with a graphical user interface and data visualisation. 
			<br><br>The advantage of Streamlit is that no front-end experience is required and we can create interactive graphical user interfaces and visualisations using only the Python programming language. 
			Probably the strongest point in choosing Streamlit is the time aspect. Because with Streamlit we can invest more time in processing and visualising the data than in dealing with the front end. <br>
			<br>Furthermore, it is possible to integrate various libraries in Streamlit in order to create diagrams.
			For the visualisation of our diagrams and filter options, libraries such as Streamlit, Plotly and Pandas were used:
			<br>
			<div id=aufzaehlung>
				<u>Pandas</u>
					<ul>
						<li>To read CSV files</li>
					</ul>
				<u>Plotly (plotly.graph_objects)</u>
					<ul>
						<li>To create the maps, pie chart, sankey diagram and time graph</li>
					</ul>
				<u>Streamlit</u>
					<ul>
						<li>Create navigation sidebar, sliders, parameter filter and structure of the site</li>
					</ul>
				<u>HTML and CSS</u>
					<ul>
						<li>For user-specific design of the website and the information button</li>
					</ul>
			</div>
		</p>
		
		<u>Sharing our Visualiszation tool to the public</u>
		<br>Streamlit offers a function called "Streamlit Sharing", which makes it easy to publish our visualisation application. 
		For this, a GitHub account was created by uploading all code files and then linking them to our Streamlit Sharing account. This is another advantage of Streamlit. It allows third parties to use our visualisation tool easily and without further installation. 
		
		"""	
		st.markdown(html_two, unsafe_allow_html=True)

	# expander 4 to open and close informations
	my_expander_three = st.beta_expander("Data Preprocessing", expanded=False)
	with my_expander_three:
		html_three = """ 
			<p> In order to have the data in a appropriate format to be displayed in the GUI, 
			the existing data set had to be filtered and adjusted. 
			It was found that it is easiest for the visualization to create a separate pre-processed data set for each visualization form.
			This creates more effort on the side of data pre-processing and data transformations, 
			but makes the visualization in the GUI much easier.  
			<br></br>
			As a first step, it was examined what a suitable CSV file should look like for each visualization form and 
			thereby a data structure was defined. 
			The data is provided in CSV files, since these can be processed well with Python and no database has to be set up.
			<br></br>
			In the given dataset, data without specific classification, such as gender, age, or country of origin, was listed as unknown. 
			For our application, we decided to use only unambiguously assignable data, 
			as this allows a conclusive statement for the given rubric and does not add to the complexity. 
			In addition, it was particularly important for us to remain consistent, so for each of the pre-processed datasets, 
			we explicitly selected males, females, and those under 18, 18-34, 35-64, and over 65. 
			For additional simplicity, we also omitted the distinction between asylum applications and initial applications.
			Furthermore, data for the Overseas Countries and Territories ("Überseeische Länder und Hoheitsgebiete") were removed, 
			since no unique geocode could be determined for this area, which is, however, important for the visualization of the map.
			A period of 10 years (2010 to 2019) was selected as the data for 2020 was not yet complete, 
			but in general the less distant data seemed more interesting.
			</p>"""
		st.markdown(html_three, unsafe_allow_html=True)

	# expander 5 to open and close informations
	my_expander_three = st.beta_expander("Target Group", expanded=False)
	with my_expander_three:
		html_three = """ 
			<p> Visuasyl was mainly developed for political parties, politicians and non-governmental organisations (NGOs). 
			Because of the simple functionalities, visuasyl can also be used by non-experts and interested parties. </p>"""
		st.markdown(html_three, unsafe_allow_html=True)

	# expander 6 to open and close informations
	my_expander_four = st.beta_expander("Insights through the visualisation tool", expanded=False)
	with my_expander_four:
		html_four = """ 
			<p> 
				<table>
					<tr>
						<th>Hypothesis</th>
						<th>Can the hypothesis be investigated with the data?</th>
						<th>Does the data confirm or refute the hypothesis?</th>
					</tr>
					<tr>
						<td>The start of the war in Syria in 2011 can also be seen in the number of asylum applications since that time.</td>
						<td>Yes and no. Based on the development of the number of asylum applications, 
						it is possible to examine whether there has been an increase since that time. 
						However, such an increase may also have other/different reasons.</td>
						<td>Since 2011, we have actually seen an increase. Not only are the numbers on the world maps getting bigger. 
						Syria is also among the top 10 countries of origin. 
						The Sankey diagram shows impressively how the refugees from Syria are distributed among the top 10 destination countries.</td>
					</tr>
					<tr>
						<td>More asylum applications are prepared by men than by women.</td>
						<td>Yes, this question can be examined. However, the data classified as unknown were omitted. 
						Due to this unreported number, it is possible that the actual values differ from those presented here.</td>
						<td> ... </td>
					</tr>
					<tr>
						<td>Federal states which have a border with neighboring states receive more asylum applications.</td>
						<td>This hypothesis cannot be answered since a worldwide data set was chosen instead of the data set for Germany.</td>
						<td> - </td>
					</tr>
					<tr>
						<td>Countries that have a border at the sea receive more asylum applications.</td>
						<td> The number of asylum applications can be taken and compared manually. 
						But differences in distribution can also be influenced by other factors, such as the size of the country and the policies of the respective country.</td>
						<td> ... </td>
					</tr>
					<tr>
						<td>Countries with a good economic situation receive more asylum applications.</td>
						<td>The number of asylum applications can be taken and compared manually. 
						However, the data do not provide information on the economic situation of the respective countries. 
						This information would have to be supplemented by another data source. 
						However, it is unclear whether this number then reflects the distribution of recent years and can therefore be generalized. 
						In addition, differences in distribution can also be influenced by other factors, 
						such as the size of the country and the policies of the respective country.</td>
						<td> - </td>
					</tr>
				</table>
			</p>"""
		st.markdown(html_four, unsafe_allow_html=True)


	# expander 7 to open and close informations
	my_expander_five = st.beta_expander("About us", expanded=False)
	with my_expander_five:
		html_five = """ 
			<p>The visualisation tool <b>visuasyl</b> was developed as part of the module "Visualisation". 
			The aim of this module has been to find a dataset of interest and to develop a visualisation tool. 
			<br>visuasyl was developed by five students (3rd semester) of the Human-Centered Computing programme at Reutlingen University:
			<br>
			<ul>
				<li> Rahel Anna, Illi<br></li>
				<li> Jessica, Giebel<br></li>
				<li> Yailda, Aini<br></li>
				<li> Hannah, Kruck<br></li>
				<li> Manuel, Haynes<br></li>
			</ul>
			<u>Why did we choose this theme and data set?</u><br>
			The issue of refugees and migration has always been an important topic and affects all citizens, whether directly or only indirectly. According to the German Federal Government, more than 70 million people are on the brink of flight worldwide today [1]. 
			Wars, persecution or the financial situation lead people to leave their homeland in order to find a safer and better life.
			We chose this topic and data set to provide information on migration and refugees to interested parties with the help of a visualisation tool.
			<u>What is the purpose of data visualization?</u><br>
			To gain insights from data, it is not enough to look at the raw data. 
			It is usually unstructured and not very useful. It is necessary to analyse the data further so that a conclusion can be drawn from the data. 
			To make this possible from the data set of asylum applications, we have developed a visualisation tool that allows the data to be illustrated with the help of various diagrams. 
			The visualisation of the data makes it possible for the user to recognise patterns or correlations within the data sets.
			</p>	
			"""
		st.markdown(html_five, unsafe_allow_html=True)
	
	

	# expander 8 to open and close informations
	my_expander_four = st.beta_expander("Source", expanded=False)
	with my_expander_four:
		html_four = """ 
			[1] Link to GitHub Project: <a target="_blank" href="https://github.com/hannahkruck/VIS_Test1.git"> VISUASYL</a><br> 			
			<p>[2] <a target="_blank" href="https://www.bundesregierung.de/breg-de/themen/migration-und-integration">Was tut die Bundesregierung im Bereich Migration und Integration? (16.10.2020)</a><br></p>
			"""
		st.markdown(html_four, unsafe_allow_html=True)


	#-----------------Page Layout--------------
    # Layout setting of the page
	c1, c2 = st.beta_columns((1,1))
	container = st.beta_container()
	st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	

		
if __name__ == "__main__":
	write()