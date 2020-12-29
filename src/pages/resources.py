"""This page is for searching and viewing the list of awesome resources"""
import logging

import streamlit as st

import awesome_streamlit as ast
from awesome_streamlit.core.services import resources

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def write():
	
#ast.shared.components.title_awesome("Welcome")      # Titel Awesome_Streamlit ausblenden
	
# CSS Startseite
	st.markdown("""
	<style>
	body {
		color: black;
		font-color: black;
		background-color: white;
	}
	h3 {
		color: #1878a1;
	}
	</style>
    """, unsafe_allow_html=True)

	st.title("Willkommen bei (TOOLNAME)")

# HTML Inhalt
	html = """
	<h3>"Toolname" ist ein Visualisierungstool ..." <br>
	Ziel<br>
	Was kann Tool alles zeigen<br>
	Welche Optionen haben Nutzer</h3>
	
	<hr>
	<br>
	"""
	st.markdown(html, unsafe_allow_html=True)
	
	#Expander - Wenn unter titel dann muss es ueber Spalten erstellen stehen
	my_expander_one = st.beta_expander("Where does the data come from?", expanded=False)
	
	with my_expander_one:
		html_one = """ 
			<p> Die Daten stammen aus der ... </p>
			Datensatz: <a target="_blank" href="https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=migr_asyappctza&lang=de">Asylbewerber und erstmalige Asylbewerber nach Staatsangehörigkeit, Alter und Geschlecht - jährliche aggregierte Daten (gerundet)<br></a>
			<br>"""
		st.markdown(html_one, unsafe_allow_html=True)


	
	#Expander - Wenn unter titel dann muss es ueber Spalten erstellen stehen
	my_expander_two = st.beta_expander("Implementation of the visualisation tool", expanded=False)

	with my_expander_two:
		html_two = """ 
			<p> The visualisation tool was implemented with the open source framework <a target="_blank" href="https://www.streamlit.io"><b> Streamlit</b></a>.<br> 
			Streamlit is both a library and a framework for Python. 
			It allows users to create and publish interactive web apps with a graphical user interface and data visualisation. 
			<br><br>The advantage of Streamlit is that no front-end experience is required and we can create interactive graphical user interfaces and visualisations using only the Python programming language. Probably the strongest point in choosing Streamlit is the time aspect. Because with Streamlit we can invest more time in processing and visualising the data than in dealing with the front end. <br>
			<br>Furthermore, it is possible to integrate various libraries in Streamlit in order to create diagrams.
			For the visualisation of our diagrams and filter options, libraries such as Streamlit, Plotly and Pandas were used:
			<br>
				<ul>
					<li>Choropleth and Line Maps</li>
				</ul>
			</p>"""
			
		st.markdown(html_two, unsafe_allow_html=True)


	#Expander - Wenn unter titel dann muss es ueber Spalten erstellen stehen
	my_expander_three = st.beta_expander("Expand3", expanded=False)
	with my_expander_three:
		html_three = """ 
			<p> Expand3</p>"""
		st.markdown(html_three, unsafe_allow_html=True)

	#Expander - Wenn unter titel dann muss es ueber Spalten erstellen stehen
	my_expander_four = st.beta_expander("Expander 4", expanded=False)
	with my_expander_four:
		html_four = """ 
			<p> Inhalt </p>"""
		st.markdown(html_four, unsafe_allow_html=True)

	#Expander - Wenn unter titel dann muss es ueber Spalten erstellen stehen
	my_expander_five = st.beta_expander("About us", expanded=False)
	with my_expander_five:
		html_five = """ 
			<p> Inhalt </p>"""
		st.markdown(html_five, unsafe_allow_html=True)
		
	
	c1, c2 = st.beta_columns((1,1))
	container = st.beta_container()
	st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


if __name__ == "__main__":
    write()
