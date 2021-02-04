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
