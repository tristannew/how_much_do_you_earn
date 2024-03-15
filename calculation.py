from scipy import stats
import pandas as pd
import numpy as np
import geopandas as gpd
import math

population = pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_85.csv", skiprows=[0,1,2])

population.rename(columns={"Country Name":"country", "Country Code":"iso", "2022":"population"}, inplace=True)

latest_population = population[["country", "iso", "population"]]

income_data = pd.read_html("https://www.worlddata.info/average-income.php")[0]

income_data.rename(columns={"Ø Annual income":"annual_income", "Country/Region":"country"}, inplace=True)

income_data["annual_income"] = income_data["annual_income"].str.replace("$", "").str.replace(",", "").astype(int)

income_population = latest_population.merge(income_data, on="country")

income_population["scaled_pop"] = income_population["population"] / income_population["population"].max()

income_population["scaled_pop"] = 1000 * income_population["scaled_pop"]



countries = gpd.read_file("countries.geojson")
countries["ADMIN"] = countries["ADMIN"].replace({'Czech Republic':'Czechia', 'Macedonia':'North Macedonia', 'Republic of Serbia':'Serbia', 'United States of America':'United States'})

income_population_countries = countries.merge(income_population, left_on="ADMIN", right_on="country")

def calculate_percentile_of_earners_above_you(income, countries_to_compare: list):
    if countries_to_compare:
        filtered = income_population[income_population.country.isin(countries_to_compare)]
        income_dist = np.repeat(filtered["annual_income"], filtered["scaled_pop"])
        result = 100 - stats.percentileofscore(income_dist, income)
    else:
        income_dist = np.repeat(income_population["annual_income"], income_population["scaled_pop"])
        result = 100 - stats.percentileofscore(income_dist, income)
    return result

def round_to_sf(num, significant_figures):
    if num == 0:
        return 0.0
    decimal_places = max(significant_figures - int(math.floor(math.log10(abs(num)))), 1)
    return round(num, decimal_places)