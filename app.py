import streamlit as st
from calculation import calculate_percentile_of_earners_above_you, round_to_sf, income_population_countries, income_population
import matplotlib.pyplot as plt

income = st.number_input("How much do you earn in a year (roughly)?")

country_selector = []
with st.expander("Choose what countries you want for comparison here (optional) :earth_africa:"):
    for country in income_population.country.unique():
        checked = st.checkbox(country)
        if checked:
            country_selector.append(country)

result = calculate_percentile_of_earners_above_you(income, countries_to_compare=country_selector)

if income:
    st.write(f"Only {round_to_sf(result, 1)}% of THE WHOLE WORLD earns more than you!")
    with st.container():
        f, ax = plt.subplots(figsize=(15,10))
        income_population_countries.plot(column="annual_income", legend=True, cmap="viridis", ax=ax, scheme="Quantiles")
        ax.set_axis_off()
        st.pyplot(f)