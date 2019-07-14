This is a real time, interactive dashboard (link to the dashboard: https://vndashboard.herokuapp.com/) built using the python packages for data visualization - 
dash and plotly, and hosted using flask webframework on heroku

Dashboard is refreshed in real-time by data from virtual nurse app (github link: https://github.com/prathamrg/flaskApp)
App User data is aggregated and fed to the dashboard to construct the various interactive charts:

1. High Level Distribution of Symptoms and Accidents (bar charts)
2. Distribution of Symptoms and Accidents by Gender (pyramid charts)
3. Distribution of Symptoms and Accidents by Age Group (pie charts)

This dashboard is useful for rural health officers to derive interesting insights about the app-users (people of his rural constituency) like:
1. Which is the most common symptom ocurring in children aged 1 to 10 
2. What kind of accidents are most common for women, (for e.g. snake bites, suggesting a need for installing more street-lights in the area)
