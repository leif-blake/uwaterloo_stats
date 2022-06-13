# This project imports and processes enrollment and graduation statistics from the University of Waterloo
# Initially created to determine retention rates by engineering programs by comparing first year enrollment
# to graduation numbers 5 years later

from uw_stats import UWStats
import plotly_studio as ps

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = UWStats(grad_file='data/ud_degrees_2020_0.csv',
                    enrl_file='data/pub_enrolment_heads_csv_winter2022_1.csv')

    programs = ['Mechatronics Engineering',
                'Mechanical Engineering',
                'Software Engineering',
                'Computer Engineering',
                'Civil Engineering',
                'Chemical Engineering',
                'Biomedical Engineering',
                'Electrical Engineering',
                'Geological Engineering',
                'Management Engineering',
                'Nanotechnology Engineering',
                'Systems Design Engineering']

    fig = data.retention_rates_plot(programs)

    ''' Open Figure in browser '''
    # data.show_fig()

    ''' Save Figure to plotly chart studio (requires api key)'''
    ps.set_plotly_api('plotly-api.txt')
    ps.post_plot(fig, 'retention_rates')

