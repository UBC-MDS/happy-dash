"""
Preprocessing of World Happiness Report Data
For data from :https://www.kaggle.com/unsdsn/world-happiness.
Download all csv's and place into `data/raw` folder, specify this as `base_path`
Check `years` list to contain all files you wish to process.

Due to poor Kaggle data quality `Dystopia + Residual` is missing in 2018, 2019. These were accessed from:
2019: https://s3.amazonaws.com/happiness-report/2019/Chapter2OnlineData.xls
2018: https://s3.amazonaws.com/happiness-report/2018/WHR2018Chapter2OnlineData.xls


By: Dustin Andrews
Date: Jan 18,2021
"""
import pandas as pd
import os

base_path = "../data/raw/"
dystopia_file_2018 = "../data/raw/2018_dystopia_residual.csv"
dystopia_file_2019 = "../data/raw/2019_dystopia_residual.csv"

path_write_out = "../data/processed/"
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
    # print(cols)


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
yearly_dict["2015"].drop(columns=["standard_error"], inplace=True)


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
    columns=["whisker_low", "whisker_high"],
    inplace=True,
)

# Because of janky Kaggle standards, join in `dystopia_residual` from separate file
# For 2018 and 2019 data.....
dystopia_2018 = pd.read_csv(dystopia_file_2018)
dystopia_2018.columns = ["country", "dystopia_residual"]

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

df_2018 = yearly_dict["2018"]
yearly_dict["2018"] = pd.merge(df_2018, dystopia_2018, on="country")


dystopia_2019 = pd.read_csv(dystopia_file_2019)
dystopia_2019.columns = ["country", "dystopia_residual"]
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
df_2019 = yearly_dict["2019"]
yearly_dict["2019"] = pd.merge(df_2019, dystopia_2019, on="country")


# Stick them together in one big dataframe
summary_df = pd.DataFrame()
for k, v in yearly_dict.items():
    temp_df = v
    v["year"] = k
    summary_df = pd.concat([summary_df, v], axis=0)
    print(v.columns)

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
