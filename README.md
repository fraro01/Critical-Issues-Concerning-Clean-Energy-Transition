# Critical Issues Concerning Clean Energy Transition
This repository is linked to: "https://critical-materials-cella-romaggi.onrender.com",
it is a public DashBoard made with Python and some libraries (dash, pandas, plotly, statsmodels, dash-bootstrap-components).
It regards the two main sectors concerning renewable energy (Wind and Solar PV) and all the materials that are needed for them.\
Specifically the DashBoard with four graphs represents: the quantities of materials needed, the added capacities and all the costs that are required in order to satisfy 
the scenarios proposed by IEA ("https://www.iea.org/reports/the-role-of-critical-minerals-in-clean-energy-transitions"); 
there is another graph representing the time series and the future predictions made with the Exponential Smoothing and Holt-Winters algorithms, for the world productions 
and prices of the materials. I collected the data regarding this last graph from the United States Geologial Survey website ("https://www.usgs.gov/centers/national-minerals-information-center/historical-statistics-mineral-and-material-commodities"),
In these particular csv files I bumped into some data-missing issues, so I applied a Python script of the "Adjusted Random Imputation" algorithm.
