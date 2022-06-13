# Defines a class to store UWaterloo statistics

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go

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
        return self.num_grad(program, grad_year)/self.first_year_enrl(program, grad_year - 5)

    # Adds retention rates for the given program to a plot
    def _plot_retention_rate(self, fig, program):
        x = []
        y = []

        min_enrl_year = int(self.enrl_data.loc[self.enrl_data['Program Grouping'] == program]['Year'].min())
        max_grad_year = int(self.grad_data.loc[self.grad_data['Program Grouping'] == program]['Degree Year'].max())

        for year in range(min_enrl_year + 5, max_grad_year + 1):
            x.append(year)
            y.append(self.retention_rate(program, year))

        self.fig.add_trace(go.Scatter(x=x, y=y, name=program.replace('Engineering', '')))

    # Plots the retention rate for the given programs over all available years
    def retention_rates_plot(self, programs):
        programs.sort()

        self.fig = go.Figure()

        for program in programs:
            self._plot_retention_rate(self.fig, program)

        self.fig.update_layout(
            title="Retention Rates for Selected programs",
            xaxis_title="Graduation Year",
            yaxis_title="Retention Rate",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
            )
        )

        self.fig.update_layout(legend=dict(groupclick="toggleitem"))
        return self.fig

    # Shows the plot
    def show_fig(self):
        self.fig.show()
