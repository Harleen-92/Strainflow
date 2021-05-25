import pandas as pd
import datetime
import plotly.graph_objects as go

# --------------------------------------Common Data--------------------------------------#
# Below code is commonly accessed by all plots.
countries = ['Australia', 'Brazil', 'Canada', 'China', 'England', 'France', 'Germany', 'India', 'Italy',
             'Japan', 'Mexico', 'Northern-Ireland', 'Scotland', 'South-Africa', 'USA', 'Wales']
__base_dict = {}


def read_monthly_csv(name):
    return pd.read_csv("monthly/" + name + "_monthly.csv")  # (Point to appropriate folder)


def load_country_wise_dataset():
    for country in countries:
        __base_dict[country] = read_monthly_csv(country)


# --------------------------------------Line Plot specific--------------------------------------#
countries_bps_m = {}


def pre_process_blip_line_plot():
    # This code filters the full data from March, 2020 and saves to countries_bps_m
    if not __base_dict:
        load_country_wise_dataset()

    for country in countries:
        countries_bps_m[country] = __base_dict[country].loc[
            __base_dict[country].Collection_Date >= '2020-03-31']


def sum_blip_for_all_dimensions_line():
    """ Line Plot 1 -- Sum of blips per sample for each Dimension
     Create a line plot for sum of blips for each country vs dimensions 0 to 36
     This function returns the plot object"""

    if not countries_bps_m:
        pre_process_blip_line_plot()

    fig = go.Figure()
    for country in countries:
        v = countries_bps_m[country].iloc[:, 0:36].sum(axis=0)
        fig.add_trace(go.Scatter(x=v.index, y=v, mode='lines',
                                 name=country,
                                 connectgaps=True,
                                 ))

    fig.update_layout(
        title=f'Sum of blips per sample for each Dimension',
        xaxis_title='Dimension',
        xaxis=dict(
            ticktext=list(range(1, 37)),
            tickvals=list(range(36))
        ),
        yaxis_title='Sum of blips per sample',
        legend_title="Country",
        template='plotly_white'
    )

    # fig.show()
    return fig


def cumulative_blips_time_for_dimension_line():
    """ Line Plot(s)  2 -- Cumulative blips per sample vs. Time
    Create a line plot for cumulative blips for each country vs {dimension}, passed as an argument.
    This function returns the plot object"""

    if not countries_bps_m:
        pre_process_blip_line_plot()

    countries_cum_blips = {}
    for country in countries:
        countries_cum_blips[country] = countries_bps_m[country].iloc[:, 0:37].cumsum(axis=0)
    
    print("countries_cum_blips: ",countries_cum_blips)

    fig = go.Figure()
    allDims = []
    for dim in range(1, 37):
        countryDims = []
        for country in countries:
            countryDims.append(countries_cum_blips[country][f'Blip_Dim{dim}'])
        allDims.append(countryDims)
    
    # for country in countries:
    #     v = countries_bps_m[country].iloc[:, 0:36].sum(axis=0)
    #     fig.add_trace(go.Scatter(x=allDims[0].index, y=allDims[0], mode='lines',
    #                              name=country,
    #                              connectgaps=True,
    #                              ))

    for country in countries:
        v = countries_cum_blips[country][f'Blip_Dim{1}']
        fig.add_trace(go.Scatter(x=v.index, y=v, mode='lines',
                                 name=country,
                                 connectgaps=True,
                                 ))
    
    
    fig.update_layout(
        # title=f'Cumulative blips per sample vs. Time (Embedding Dim {str(dimension)})',
        xaxis_title='Time (months)',
        yaxis_title='Cumulative sum of blips per sample',
        legend_title="Country",
        width=700,
        height=500,
        template='plotly_white'
    )

    dimensions_dropdown = []
    for d in range(0, 36):
        dimensions_dropdown.append(dict(
                        args=[{'y': allDims[d] }],
                        label= 'Blip_Dim' + str(d+1),
                        method='update'
                    ))

    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list(dimensions_dropdown),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="center",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Plot Month:", showarrow=False,
            x=0, y=1.085, yref="paper", align="left")
        ]
    )

    # fig.show()
    return fig


# --------------------------------------Radar Plot specific--------------------------------------#
def make_equal(dic):
    minimum = 20
    selected_dates = []
    for key, val in dic.items():
        if val.shape[0] < minimum:
            minimum = val.shape[0]
            selected_dates = list(val['Collection_Date'])
    print("\nMinimum value:", minimum)
    print(selected_dates)

    for key, val in dic.items():
        df = val[val['Collection_Date'].isin(selected_dates)].reset_index(drop=True)
        dic[key] = df
        print(key, df.shape)
    return dic


def take_lists(dic, cols, month):
    for key, val in dic.items():
        df = val[cols]
        df = df[df['Collection_Date'] == month]
        df = df.drop('Collection_Date', axis=1)
        df = df.reset_index(drop=True)
        dic[key] = list(df.iloc[0])
    return dic


# def plotly_radar(categories, dic, flag, month):
#     fig = go.Figure()

#     if flag == 1:
#         for key, val in dic.items():
#             fig.add_trace(go.Scatterpolar(r=val, theta=categories, name=key.capitalize()))
#     else:
#         for key, val in dic.items():
#             fig.add_trace(go.Scatterpolar(r=val, theta=categories, fill='toself', name=key.capitalize()))

#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 1]
#             )),
#         showlegend=True,
#         title={
#             'text': month,
#             'x': 0.5,
#         },
#     )
#     # fig.show()
#     return fig


select_month = ['2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31', '2020-08-31', '2020-09-30',
                '2020-10-31', '2020-11-30', '2020-12-31', '2021-01-31']


def blips_for_month():
    """Create a Radar plot of blips of all countries for the {month}, passed as an argument.
    This function returns the plot object"""

    if not __base_dict:
        load_country_wise_dataset()

    df_dic = make_equal(__base_dict)

    select_dimensions = ['Collection_Date', 'Blip_Dim1', 'Blip_Dim2', 'Blip_Dim3', 'Blip_Dim4', 'Blip_Dim5']
    # month = select_month[len(select_month)-1]
    month = select_month[0]

    dictionary = take_lists(df_dic.copy(), select_dimensions, month)
    mo = int(month.split("-")[1])
    m = datetime.date(1900, mo, 1).strftime('%B')
    y = month.split("-")[0]
    print("-----------", m, y, "-----------")
    print("\t", dictionary)
    # fig = plotly_radar(select_dimensions[1:], dictionary, 1, m + " " + y)


    fig = go.Figure()
    for key, val in dictionary.items():
        fig.add_trace(go.Scatterpolar(r=val, theta=select_dimensions[1:], name=key.capitalize()))


    months_dropdown = []
    for mon in select_month:
        dictionary = take_lists(df_dic.copy(), select_dimensions, mon)
        mo = int(mon.split("-")[1])
        m = datetime.date(1900, mo, 1).strftime('%B')
        y = mon.split("-")[0]
        print("-----------", m, y, "-----------")
        print("\t", dictionary)
        
        rval = []
        for key, val in dictionary.items():
            rval.append(val)
        print("RVAL: ", rval)
        months_dropdown.append(dict(
                        args=[{'r': rval }],
                        label= m + ' ' + y,
                        method='update'
                    ))


    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list(months_dropdown),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        # title={
        #     'text': m + " " + y,
        #     'x': 0.5,
        # },
    )

    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="Plot Month:", showarrow=False,
            x=0, y=1.085, yref="paper", align="left")
        ]
    )

    return fig


# --------------------------------------Start Plotting--------------------------------------#
# sum_blip_for_all_dimensions_line().show()
# cumulative_blips_time_for_dimension_line().show()
# blips_for_month().show()
