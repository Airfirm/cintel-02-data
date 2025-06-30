import palmerpenguins
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguin Exploratory Data Analysis - Femi", fillable=True)

# Sidebar
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select Plotly Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )
    ui.input_numeric("plotly_bin_count", "Plotly Histogram Bin Count", 20)
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 5, 100, 20)
    ui.input_checkbox_group(
        "selected_species_list",
        "Filter by Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=True
    )
    ui.hr()
    ui.a("GitHub Repo URL", href="https://github.com/Airfirm/cintel-02-data", target="_blank")

# Main layout - Data Table and Data Grid
with ui.layout_columns():
    @render.data_frame
    def data_table():
        return render.DataTable(penguins_df)

    @render.data_frame
    def data_grid():
        return render.DataGrid(penguins_df)

# Main layout - Histograms and Scatterplot
with ui.layout_columns():
    @render_plotly
    def plot1():
        return px.histogram(penguins_df, y="species")

    @render.plot(alt="Seaborn Histogram")
    def seaborn_hist():
        np.random.seed(1)
        data = penguins_df.dropna(subset=["body_mass_g"])
        values = data["body_mass_g"]
        bins = input.seaborn_bin_count()
        plt.hist(values, bins=bins, density=True)
        plt.title("Seaborn Histogram")
        plt.xlabel("Body Mass (g)")
        plt.ylabel("Density")

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            penguins_df,
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            title="Penguins Plot (Plotly Express)",
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)"
            },
            size_max=8
        )
