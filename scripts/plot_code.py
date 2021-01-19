import pandas as pd
import numpy as np
import plotly.express as px


summary_df = pd.read_csv("../data/processed/summary_df.csv")

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
        List of features (column names in `summary_df`). If `None` use all 6 contributing features to happiness score
    year_list : list
        List of years to filter on
    """
    # ALl features to consider
    all_feats = [
        "gdp_per_capita",
        "family",
        "health_life_expectancy",
        "freedom",
        "perceptions_of_corruption",
        "generosity",
    ]

    if feat_list is None:
        feat_list = all_feats

    # Filter to specified data, calculate means
    filtered_df = (
        filter_df(summary_df, country_list, feat_list, year_list)
        .groupby("country")
        .mean()
        .reset_index()
    )
    cols = list(set(all_feats).intersection(filtered_df.columns))

    fig = px.bar(
        filtered_df,
        x=cols,
        y="country",
        title="Average Happiness Score by Contributing Factors",
        orientation="h",
    )

    fig.show()


build_overall_graph(
    summary_df,
    ["Canada", "Switzerland"],
    feat_list=None,  # ["gdp_per_capita", "generosity", "freedom"],
    year_list=[2019],
)

#%%
def filter_df(summary_df, country_list, feat_list, year_list):
    """Filter summary_df to countries, columns (feat_list), and list of years"""
    year_list = [int(x) for x in year_list]
    return summary_df.loc[
        ((summary_df.country.isin(country_list)) & (summary_df.year.isin(year_list))),
        feat_list + ["country"],
    ]


assert (
    filter_df(summary_df, ["Canada"], ["happiness_score"], ["2018"])
    .loc[:, "happiness_score"]
    .values
    == 7.328
)
