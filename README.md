# happy-dash
An interactive exploration of the World Happiness Report

Heroku app [here](https://happydash.herokuapp.com/).

### Description of Dashboard Design
This dashboard is to compare happiness across multiple countries.
The dashboard will be divided into two main screens: an overview and a detailed view.
Both screens will have some aspects in common: they will both contain a menu that will allow the user of the dashboard to select the features they want to analyze as well as the geographies they want to compare. Geographies can be divided into countries or continents. For both screens the majority of the screen will display visuals and the user will be able to select the date range for the visuals as well. This date slider will be located on the upper right side of the screen in both screens.


### Features Completed:
#### Detailed View

![Detailed View](Detailed_view.png)

In detailed view, the user is able to select all features and any desired countries. On the visual section, they will be shown up to 8 line charts. The first and central one will display happiness scores over time by country. The other line charts will be charts of the individual features and will appear below the central chart. There will be a legend displaying the country or continent names as well as the corresponding colours for each.

### Features To Be Implemented:
#### Overview View

![Overview](Overview.png)

In the overview, in the menu the user can select all or a certain number of features. This also applies to countries and continents. In the visual section there will be one chart which will be a stacked horizontal bar chart of the selected features that comprise happiness score. On the left side will be the names of each country, their ranking (i.e. 1) and their happiness score. In the bottom will be a legend with the corresponding colours to given features. (Time permitting) there will also be a button in the bottom left of the visual that will allow for the user to toggle it to a choropleth view (map view). 


### Running Locally:

To run this app locally and modify it - first clone this repo:

```bash
$ git clone https://github.com/UBC-MDS/happy-dash.git
```

Setup a conda env for it, and activate it using the following commands from the root of the project on your computer:

```bash
$ conda env create
$ conda activate happydash
```

Finally, run the app with:

```bash
$ python src/app.py
```
