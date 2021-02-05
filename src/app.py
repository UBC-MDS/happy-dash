# Author: Kevin Shahnazari, Dustin Andrews
# Date created: Jan 18 2021

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px

###********************************* Define constants *******************************************
summary_df = pd.read_csv("data/processed/summary_df.csv").sort_values(by="country")

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    # "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Define relationship between dataset columns and display names
feature_dict = {
    "GDP Per Capita": "gdp_per_capita",
    "Family": "family",
    "Life Expectancy": "health_life_expectancy",
    "Freedom": "freedom",
    "Corruption": "perceptions_of_corruption",
    "Generosity": "generosity",
    "Dystopia baseline + residual": "dystopia_residual",
}

discrete_color_scheme = px.colors.qualitative.Pastel

###***************************************Layout building************************************

sidebar = dbc.Col(
    children=[
        html.H1("World Happiness Report Explorer", className="display-5"),
        html.Hr(),
        html.H2("Features", className="display-6"),
        html.Hr(),
        dbc.Checklist(
            id="feature-select-1",
            options=[{"label": k, "value": v} for k, v in feature_dict.items()],
            value=[v for k, v in feature_dict.items()],
        ),
        html.Hr(),
        html.H3("Year Range", className="display-6"),
        dcc.RangeSlider(
            id="year-select-1",
            min=min(summary_df.year),
            max=max(summary_df.year),
            step=1,
            marks={
                int(x): {"label": str(x), "style": {"transform": "rotate(45deg)"}}
                for x in list(summary_df.year.unique())
            },
            value=[2015, 2019],
            pushable=1,
        ),
        html.Hr(),
        html.H3(
            "Countries",
            className="display-6",
            style={"width": "50%", "display": "inline-block"},
        ),
        dbc.Button(
            "?",
            id="country-help",
            color="info",
            outline=True,
            size="sm",
            style={"float": "right"},
        ),
        dbc.Col(
            dcc.Dropdown(
                id="country-select-1",
                multi=True,
                options=[{"label": x, "value": x} for x in summary_df.country.unique()],
                value=["Canada", "Switzerland", "China"],
            ),
            width=12,
            style={
                "padding": "10px 10px 10px 0px",
            },
        ),
        # Add a help box for showing how to select countries
        dbc.Popover(
            [
                dbc.PopoverHeader("Country Selection"),
                dbc.PopoverBody(
                    "Select countries to evaluate here, or you can click on them on the map"
                ),
            ],
            id="popover",
            is_open=False,
            target="country-help",
        ),
    ],
    style={"background-color": "#f8f9fa"},
    md=3,
)

## Build out content within each tab. Sidebar is outside of tab structure
detail_content = dbc.Col(
    id="detail_content",
    children=[
        dcc.Loading(
            type="cube",
            children=[
                dcc.Graph(id="happiness-over-time", style={"height": "30vh"}),
                dcc.Graph(id="features-over-time", style={"height": "68vh"}),
            ],
        ),
    ],
)

summary_content = dbc.Col(
    id="summary_content",
    children=[
        dcc.Loading(
            type="cube",
            children=[
                dcc.Graph(id="happiness-map", figure={}, style={"height": "50vh"}),
                dcc.Graph(
                    id="happiness-bar-chart", figure={}, style={"height": "45vh"}
                ),
            ],
        ),
    ],
)

app = dash.Dash(
    __name__,
    title="World Happiness Explorer",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server

app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                sidebar,
                dbc.Col(
                    children=[
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    summary_content,
                                    label="Summary View",
                                    tab_id="summary_view",
                                ),
                                dbc.Tab(
                                    detail_content,
                                    label="Detailed View",
                                    tab_id="detail_view",
                                ),
                            ],
                            id="tabs",
                            active_tab="summary_view",
                        ),
                    ],
                    md=9,
                ),
            ],
        )
    ],
    fluid=True,
    style={"width": "80%"},
)

####*******************************************Callback definition***************************
def filter_df(summary_df, country_list, feat_list, year_range):
    """
    Helper func to filter summary_df to countries, columns (feat_list), and list of years.
    Keep "country", "happiness_score", "year" for downstream tasks
    """
    year_list = list(range(min(year_range), max(year_range) + 1))

    if country_list == []:
        country_list = summary_df.country.unique().tolist()

    return summary_df.loc[
        ((summary_df.country.isin(country_list)) & (summary_df.year.isin(year_list))),
        feat_list + ["country", "happiness_score", "year", "country_code"],
    ]


@app.callback(
    [Output("happiness-over-time", "figure"), Output("features-over-time", "figure")],
    [
        Input("country-select-1", "value"),
        Input("feature-select-1", "value"),
        Input("year-select-1", "value"),
        Input("tabs", "active_tab"),
    ],
)
def build_detail_plots(country_list, feat_list, year_range, active_tab):
    """Builds a list of charts summarizing certain countries, feature names (columns in the df)
    and a time frame.

    First chart returned is happiness score over time.
    Second chart is a facetted plot for each contributing feature to overall happiness in each country

    ** Only executes if "Detailed View" tab is selected **

    Parameters
    ----------
    country_list : list
        List of country names to filter `summary_df` on
    feat_list : list
        List of features (column names in `summary_df`). If `None` use all 7 contributing features to happiness score
    year_range : list
        List of years to filter on. Will only contain endpoints
    active_tab : string
        Name of active tab in content area. Used to short circuit callback if detail content isn't active

    Returns
    -------
    list : List[plotly.express.Figure]
        First chart: Happiness score over time by country
        Second - Eigth chart: Contributing factor trend over time by country.
        Empty charts appended at end if all features aren't specified.
    """
    # Short circuit if detail tab isn't active
    if active_tab != "detail_view":
        return [{}, {}]

    # ALl features to consider
    all_feats = [v for v in feature_dict.values()]

    if feat_list is None:
        feat_list = all_feats

    if country_list == []:
        country_list = ["Canada"]

    # Filter to specified data
    # Improve year formatting for datetime x-axis
    filtered_df = (
        filter_df(summary_df, country_list, feat_list, year_range)
        .assign(year=lambda x: pd.to_datetime(x.year, format="%Y"))
        .sort_values(by="year")
    )
    cols = list(set(all_feats).intersection(filtered_df.columns))

    fig_list = []

    # Build first plot - happiness scores over time
    happiness_plot = (
        px.line(
            filtered_df,
            x="year",
            y="happiness_score",
            color="country",
            color_discrete_sequence=discrete_color_scheme,
            title="Happiness Score Over Time by Country",
        )
        .update_traces(mode="lines+markers")
        .update_layout(
            {
                "xaxis": {
                    "tickmode": "array",
                    "tickvals": filtered_df.year.dt.year.unique(),
                    "ticktext": [str(x) for x in filtered_df.year.dt.year.unique()],
                },
                "margin": {"b": 0},
            }
        )
    )
    fig_list.append(happiness_plot)

    # Facetted plot for features
    fig_list.append(
        px.line(
            filtered_df.melt(
                id_vars=["country", "year"], value_vars=cols, value_name="Contribution"
            ),
            x="year",
            y="Contribution",
            color_discrete_sequence=discrete_color_scheme,
            color="country",
            facet_col="variable",
            facet_col_wrap=2,
            facet_col_spacing=0.04,
            facet_row_spacing=0.07,
            title="Impact Of Features Over Time On Happiness Score",
        )
        .for_each_annotation(
            lambda label: label.update(
                text=list(feature_dict.keys())[
                    list(feature_dict.values()).index(label.text.split("=")[1])
                ]
            )
        )
        .update_yaxes(matches=None, showticklabels=True)
        .update_xaxes(showticklabels=True)
        .update_traces(mode="lines+markers")
    )

    return fig_list


@app.callback(
    Output("happiness-map", "figure"),
    [
        Input("year-select-1", "value"),
        Input("tabs", "active_tab"),
    ],
)
def happiness_map(year_range, active_tab):
    """Builds a cholorpleth map colored by happiness score based on year, time range, country list
    ** Only executes if "Summary View" tab is selected **

    Parameters
    ----------
    year_range : list
        List of years to filter on. Will only contain endpoints
    active_tab : string
        Name of active tab in content area. Used to short circuit callback if detail content isn't active

    Returns
    -------
    fig : [plotly.express.Figure]
        Chloropleth map with happiness score by country
    """

    # Short circuit if detail tab isn't active
    if active_tab != "summary_view":
        return {}

    # Filter to specified data
    # Leave all countries in
    filtered_df = filter_df(summary_df, [], [], year_range).sort_values(by="year")

    fig = px.choropleth(
        data_frame=filtered_df,
        # locationmode="ISO-3",
        locations="country_code",
        hover_name="country",
        color="happiness_score",
        animation_frame="year",
        animation_group="country",
        color_continuous_scale=px.colors.sequential.Sunset_r,
    )

    fig.layout.sliders[0].pad.t = 10
    fig.layout.updatemenus[0].pad.t = 10

    fig.update_layout(
        title_text="Happiness Score Worldwide on 10 Point Scale",
        geo=dict(
            showframe=False, showcoastlines=False, projection_type="equirectangular"
        ),
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig


@app.callback(
    Output("happiness-bar-chart", "figure"),
    [
        Input("country-select-1", "value"),
        Input("feature-select-1", "value"),
        Input("year-select-1", "value"),
        Input("tabs", "active_tab"),
    ],
)
def build_overall_graph(country_list, feat_list, year_list, active_tab):
    """Builds a bar chart summarizing certain countries, feature names (columns in the df)
    and a time frame

    Parameters
    ----------
    country_list : list
        List of country names to filter `summary_df` on
    feat_list : list
        List of features (column names in `summary_df`). If `None` use all 7 contributing features to happiness score
    year_list : list
        List of years to filter on
    active_tab : string
        Name of active tab in content area. Used to short circuit callback if detail content isn't active

    Returns
    -------
    fig : plotly.express.Figure
    """
    # Short circuit if detail tab isn't active
    if active_tab != "summary_view":
        return {}

    if feat_list is None:
        feat_list = feature_dict.values

    # Filter to specified data, calculate means
    filtered_df = (
        filter_df(summary_df, country_list, feat_list, year_list)
        .groupby("country")
        .mean()
        .reset_index()
        .sort_values("happiness_score", ascending=True)
    )
    cols = list(set(feat_list).intersection(filtered_df.columns))
    title_string = (
        f"Average Happiness Score by Contributing Factors: {min(year_list)} to {max(year_list)}"
        if len(year_list) > 1
        else f"Happiness Score by Contributing Factor: {year_list[0]}"
    )

    fig = px.bar(
        filtered_df,
        x=cols,
        y="country",
        title=title_string,
        color_discrete_sequence=discrete_color_scheme,
        labels={
            "value": "Happiness Score",
            "country": "Country",
            "variable": "Features",
        },
        orientation="h",
    )

    ### Code adapted from https://stackoverflow.com/questions/64371174/plotly-how-to-change-variable-label-names-for-the-legend-in-a-plotly-express-li
    def customLegend(fig, nameSwap):
        for i, dat in enumerate(fig.data):
            for elem in dat:
                if elem == "name":
                    fig.data[i].name = nameSwap[fig.data[i].name]
        return fig

    fig = customLegend(
        fig=fig,
        nameSwap={
            "value": "Happiness Score",
            "country": "Country",
            "variable": "Features",
            "gdp_per_capita": "GDP Per Capita",
            "family": "Family",
            "health_life_expectancy": "Life Expectancy",
            "freedom": "Freedom",
            "perceptions_of_corruption": "Corruption",
            "generosity": "Generosity",
            "dystopia_residual": "Dystopia baseline + residual",
        },
    )

    ## If wanting to move legend around, update layout
    # fig.update_layout({"legend_orientation": "h", "margin": {"t": 40, "l": 50}})

    return fig


# Callback to allow clicks on the map to add countries to filter
@app.callback(
    Output("country-select-1", "value"),
    [
        Input("happiness-map", "clickData"),
    ],
    [State("country-select-1", "value")],
)
def country_click(click_data, current_countries):
    """Gets click data from happiness map - adds to countries in `country-select-1` drop down box.
    Uses State to get current countries already in box

    Parameters
    ----------
    click_data : dict
        dictionary corresponding to the points click on `happiness-map`
    """
    if click_data is not None:
        country_code_selected = click_data["points"][0]["location"]

        new_country = list(
            summary_df.loc[
                summary_df.country_code == country_code_selected, "country"
            ].unique()
        )

        if current_countries is None:
            return new_country
        elif new_country not in current_countries:
            return current_countries + new_country
        else:
            return current_countries

    else:
        return current_countries


# Callback for showing help on country selection
@app.callback(
    Output("popover", "is_open"),
    [Input("country-help", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
