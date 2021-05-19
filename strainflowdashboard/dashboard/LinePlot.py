import pandas as pd
import datetime
import plotly.graph_objects as go
from plotly.offline import plot

countries = ['Australia', 'Brazil', 'Canada', 'China', 'England', 'France', 'Germany', 'India', 'Italy',
             'Japan', 'Mexico', 'Northern-Ireland', 'Scotland', 'South-Africa', 'USA', 'Wales']

__base_dict = {}

def read_monthly_csv(name):
    return pd.read_csv("monthly/" + name + "_monthly.csv")  # (Point to appropriate folder)​

def load_country_wise_dataset():
    for country in countries:
        __base_dict[country] = read_monthly_csv(country)


countries_bps_m = {}

def pre_process_line_plots():
    if not __base_dict:
        load_country_wise_dataset()

    for country in countries:
        countries_bps_m[country] = __base_dict[country].loc[
            __base_dict[country].Collection_Date >= '2020-03-31']

def line_plot_1():
    """ Line Plot 1 -- Sum of blips per sample for each Dimension """
    if not countries_bps_m:
        pre_process_line_plots()

    fig = go.Figure()
    for country in countries:
        v = countries_bps_m[country].iloc[:, 0:36].sum(axis=0)
        fig.add_trace(go.Scatter(x=v.index, y=v, mode='lines',
                                 name=country,
                                 connectgaps=True,
                                 ))

    fig.update_layout(
        #title=f'Sum of blips per sample for each Dimension',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Dimension',
        xaxis=dict(
            ticktext=list(range(1, 37)),
            tickvals=list(range(36))
        ),
        yaxis_title='Sum of blips per sample',
        legend_title="Country",
        template='plotly_white',
        height=600
    )
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    #fig.show()
    return plot_div
