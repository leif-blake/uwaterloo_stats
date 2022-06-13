# Defines a class to store UWaterloo statistics

import numpy as np
import pandas as pd
import plotly.graph_objects as go

colors = ['#800000', '#20B2AA', '#FF4500', '#556B2F', '#8A2BE2', '#FF00FF', '#8B4513', '#708090', '#7CFC00', '#48D1CC',
          '#DC143C', '#00FA9A', '#FFA500', '#808000', '#483D8B', '#DA70D6', '#D2691E', '#B0C4DE', '#DAA520', '#BA55D3',
          '#CD5C5C', '#008080', '#B8860B', '#9ACD32', '#8B008B', '#FF1493', '#F4A460', '#696969', '#8FBC8F', '#DB7093',
          '#FA8072', '#00FFFF', '#FFD700', '#008000', '#800080', '#FF69B4', '#CD853F', '#A9A9A9', '#48D1CC', '#000000',
          ]

class UWStats():

    def __init__(self,
                 enrl_file='',
                 grad_file=''):
        self.grad_data = pd.read_csv(grad_file)
        self.enrl_data = pd.read_csv(enrl_file)

        # Convert from fiscal year to year in enrolment stats
        # ex: 2008/09 to 2008 (S/F) or 2009 (W)
        self.enrl_data['Fiscal Year'] = np.where(self.enrl_data['Term Type'] == 'Winter term',
                                                 (self.enrl_data['Fiscal Year'].str[:2]
                                                  + self.enrl_data['Fiscal Year'].str[5:]
                                                  ).astype(int),
                                                 (self.enrl_data['Fiscal Year'].str[:4]).astype(int))
        self.enrl_data.rename(columns={'Fiscal Year': 'Year'}, inplace=True)

        self.fig = ''

    # Returns the number of students in their 1A academic term for a given program and year
    def first_year_enrl(self, program, year):
        subset_enrl_data = self.enrl_data.loc[(self.enrl_data['Program Grouping'] == program)
                                              & (self.enrl_data['Year'] == year)
                                              & (self.enrl_data['Study Year'] == '1')
                                              & (self.enrl_data['Term Type'] == 'Fall term')
                                              & (self.enrl_data['Work Term'] == 'Academic Term')
                                              ]

        return subset_enrl_data['Student Headcounts'].sum()

    # Returns the number of students graduating from a given program in a given year
    def num_grad(self, program, year):
        subset_grad_data = self.grad_data.loc[(self.grad_data['Program Grouping'] == program)
                                              & (self.grad_data['Degree Year'] == year)
                                              & (self.grad_data['Degree Career'] == 'Undergraduate')
                                              ]
        return subset_grad_data['Number of Degrees'].sum()

    # Returns the retention rate for a given program in a given graduation year
    # Calculated as the number graduating divided by the first year enrolment 5 years prior
    def retention_rate(self, program, grad_year):
        return self.num_grad(program, grad_year) / self.first_year_enrl(program, grad_year - 5)

    # Adds retention rates for the given program to a plot
    def _plot_retention_rate(self, fig, program, hex_color='#ffe476'):
        x = []
        y = []

        min_enrl_year = int(self.enrl_data.loc[self.enrl_data['Program Grouping'] == program]['Year'].min())
        max_grad_year = int(self.grad_data.loc[self.grad_data['Program Grouping'] == program]['Degree Year'].max())

        for year in range(min_enrl_year + 5, max_grad_year + 1):
            x.append(year)
            y.append(self.retention_rate(program, year))

        self.fig.add_trace(go.Scatter(x=x, y=y, name=program.replace('Engineering', ''), line=dict(color=hex_color)))

    # Plots the retention rate for the given programs over all available years
    def retention_rates_plot(self, programs):
        programs.sort()

        self.fig = go.Figure()

        i = 0
        for program in programs:
            self._plot_retention_rate(self.fig, program, hex_color=colors[i])
            i += 1

        self.fig.update_layout(
            title="Retention Rates for Selected Programs",
            xaxis_title="Graduation Year",
            yaxis_title="Retention Rate",
            font=dict(
                family="Open Sans",
                size=16,
                color="RebeccaPurple"
            ),
            legend_font_size=14
        )

        return self.fig

    # Shows the plot
    def show_fig(self):
        self.fig.show()
