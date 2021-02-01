"""
Rough code to build callbacks in the happy-dash dashboard
By: Dustin Andrews
Date: 2020-01-18
"""
#%%
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


#%%
def build_overall_graph(summary_df, country_list, feat_list, year_list):
    """Builds a bar chart summarizing certain countries, feature names (columns in the df)
    and a time frame

    Parameters
    ----------
    summary_df : Pandas.DataFrame
        Dataframe with columns
    country_list : list
        List of country names to filter `summary_df` on
    feat_list : list
        List of features (column names in `summary_df`). If `None` use all 7 contributing features to happiness score
    year_list : list
        List of years to filter on

    Returns
    -------
    fig : plotly.express.Figure
    """
    # ALl features to consider
    all_feats = [
        "gdp_per_capita",
        "family",
        "health_life_expectancy",
        "freedom",
        "perceptions_of_corruption",
        "generosity",
        "dystopia_residual",
    ]

    if feat_list is None:
        feat_list = all_feats

    # Filter to specified data, calculate means
    filtered_df = (
        filter_df(summary_df, country_list, feat_list, year_list)
        .groupby("country")
        .mean()
        .reset_index()
        .sort_values("happiness_score", ascending=True)
    )
    cols = list(set(all_feats).intersection(filtered_df.columns))
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
        orientation="h",
    )

    ## If wanting to move legend around, update layout
    # fig.update_layout({"legend_orientation": "h", "margin": {"t": 40, "l": 50}})

    return fig


#%% For use in VS Code Interactive window
summary_df = pd.read_csv("../data/processed/summary_df.csv")


#%%
fig = px.choropleth(
    data_frame=summary_df,
    # locationmode="ISO-3",
    locations="country_code",
    color="happiness_score",
    animation_frame="year",
    animation_group="country",
    # text=summary_df["country"],
)

fig.update_layout(
    title_text="Happiness Score Worldwide on 10 Point Scale",
    geo=dict(showframe=False, showcoastlines=False, projection_type="equirectangular"),
)

fig.show()


#%%
overall_graph = build_overall_graph(
    summary_df,
    ["Canada", "Switzerland", "China", "France"],
    feat_list=None,  # ["gdp_per_capita", "generosity", "freedom"],
    year_list=[2018, 2019],
)

figs = build_detail_plots(
    summary_df,
    ["Canada", "Switzerland", "China", "France"],
    feat_list=None,  # ["gdp_per_capita", "generosity", "freedom"],
    year_list=[2016, 2017, 2018, 2019],
)

for f in figs:
    f.show()
