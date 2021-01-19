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

    fig.show()


build_overall_graph(
    summary_df,
    ["Canada", "Switzerland", "China", "France"],
    feat_list=None,  # ["gdp_per_capita", "generosity", "freedom"],
    year_list=[2018, 2019],
)

#%%
def filter_df(summary_df, country_list, feat_list, year_list):
    """
    Filter summary_df to countries, columns (feat_list), and list of years.
    Keep "country", "happiness_score", "year" for downstream tasks
    """
    year_list = [int(x) for x in year_list]
    return summary_df.loc[
        ((summary_df.country.isin(country_list)) & (summary_df.year.isin(year_list))),
        feat_list + ["country", "happiness_score", "year"],
    ]


assert (
    filter_df(summary_df, ["Canada"], ["happiness_score"], ["2018"])
    .loc[:, "happiness_score"]
    .values
    == 7.328
)

# %%
def build_detail_plots(summary_df, country_list, feat_list, year_list):
    """Builds a list of bar charts summarizing certain countries, feature names (columns in the df)
    and a time frame.

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
    list : List[plotly.express.Figure]
        First chart: Happiness score over time by country
        Second - Eigth chart: Contributing factor trend over time by country.
        Empty charts appended at end if all features aren't specified.
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

    # Filter to specified data
    # Improve year formatting for datetime x-axis
    filtered_df = filter_df(summary_df, country_list, feat_list, year_list).assign(
        year=lambda x: pd.to_datetime(x.year, format="%Y")
    )
    cols = list(set(all_feats).intersection(filtered_df.columns))

    fig_list = []
    # Build first plot - happiness scores over time
    happiness_plot = px.line(
        filtered_df,
        x="year",
        y="happiness_score",
        color="country",
        title="Happiness Score Over Time by Country",
    ).update_layout(
        {
            "xaxis": {
                # "tickformat": "%Y",
                "tickmode": "array",
                "tickvals": filtered_df.year.dt.year.unique(),
                "ticktext": [str(x) for x in filtered_df.year.dt.year.unique()],
            }
        }
    )
    fig_list.append(happiness_plot)

    # Build rest of selected plots by features
    for c in cols:
        fig_list.append(
            px.line(
                filtered_df,
                x="year",
                y=c,
                color="country",
                title=f"Impact of {c} over time on Happiness Score",
            ).update_layout(
                {
                    "xaxis": {
                        # "tickformat": "%Y",
                        "tickmode": "array",
                        "tickvals": filtered_df.year.dt.year.unique(),
                        "ticktext": [str(x) for x in filtered_df.year.dt.year.unique()],
                    }
                }
            )
        )

    return fig_list


figs = build_detail_plots(
    summary_df,
    ["Canada", "Switzerland", "China", "France"],
    feat_list=None,  # ["gdp_per_capita", "generosity", "freedom"],
    year_list=[2016, 2017, 2018, 2019],
)

for f in figs:
    f.show()
# %%
