"""
Preprocessing of World Happiness Report Data
For data from :https://www.kaggle.com/unsdsn/world-happiness.
Download all csv's and place into `data/raw` folder, specify this as `base_path`
Check `years` list to contain all files you wish to process
By: Dustin Andrews
Date: Jan 18,2021
"""
import pandas as pd
import os

base_path = "../data/raw/"
path_out = "../data/processed/"
years = ["2015", "2016", "2017", "2018", "2019"]
yearly_dict = {}

for y in years:
    # Get csv and rename messy columns to start
    yearly_df = pd.read_csv(os.path.join(base_path, y + ".csv"))
    yearly_df.columns = (
        yearly_df.columns.str.lower()
        .str.replace("[()]", "", regex=True)
        .str.replace(" |[.]", "_")
    )
    yearly_dict[y] = yearly_df
    cols = list(yearly_dict[y].columns)


# Have to manually fix each year in a different way
yearly_dict["2015"].rename(
    columns=(
        {
            "economy_gdp_per_capita": "gdp_per_capita",
            "trust_government_corruption": "perceptions_of_corruption",
        }
    ),
    inplace=True,
)
yearly_dict["2015"].drop(columns=["dystopia_residual", "standard_error"], inplace=True)


yearly_dict["2016"].rename(
    columns=(
        {
            "economy_gdp_per_capita": "gdp_per_capita",
            "trust_government_corruption": "perceptions_of_corruption",
        }
    ),
    inplace=True,
)
yearly_dict["2016"].drop(
    columns=[
        "lower_confidence_interval",
        "upper_confidence_interval",
        "dystopia_residual",
    ],
    inplace=True,
)


yearly_dict["2017"].rename(
    columns=(
        {
            "economy__gdp_per_capita_": "gdp_per_capita",
            "health__life_expectancy_": "health_life_expectancy",
            "trust__government_corruption_": "perceptions_of_corruption",
        }
    ),
    inplace=True,
)

yearly_dict["2017"].drop(
    columns=[
        "whisker_low",
        "whisker_high",
        "dystopia_residual",
    ],
    inplace=True,
)


yearly_dict["2018"].rename(
    columns=(
        {
            "overall_rank": "happiness_rank",
            "score": "happiness_score",
            "healthy_life_expectancy": "health_life_expectancy",
            "country_or_region": "country",
            "social_support": "family",
            "freedom_to_make_life_choices": "freedom",
        }
    ),
    inplace=True,
)

yearly_dict["2019"].rename(
    columns=(
        {
            "overall_rank": "happiness_rank",
            "score": "happiness_score",
            "healthy_life_expectancy": "health_life_expectancy",
            "country_or_region": "country",
            "social_support": "family",
            "freedom_to_make_life_choices": "freedom",
        }
    ),
    inplace=True,
)

# Stick them together in one big dataframe
summary_df = pd.DataFrame()
for k, v in yearly_dict.items():
    temp_df = v
    v["year"] = k
    summary_df = pd.concat([summary_df, v], axis=0)
    # print(v.columns)

# Fix some country names
summary_df.loc[summary_df.country == "Hong Kong S.A.R., China", "country"] = "Hong Kong"
summary_df.loc[
    summary_df.country == "Somaliland region", "country"
] = "Somaliland Region"

# Fix region missing in some years. Drop the column then rejoin a lookup table onto full dataframe
region_lookup = summary_df.loc[:, ["country", "region"]].drop_duplicates().dropna()
summary_df.drop(columns=["region"], inplace=True)
summary_df = pd.merge(summary_df, region_lookup, on="country")

summary_df.to_csv(os.path.join(path_out, "summary_df.csv"), index=False)
