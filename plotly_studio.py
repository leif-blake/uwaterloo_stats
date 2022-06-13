# Chart studio functions

import chart_studio
import chart_studio.plotly as py


def set_plotly_api(api_filename):
    with open(api_filename) as f:
        username = f.readline().strip()
        api_key = f.readline().strip()

        print(username)
        print(api_key)
        chart_studio.tools.set_credentials_file(username=username,
                                            api_key=api_key)


def post_plot(fig, filename):
    py.plot(fig, filename=filename, auto_open=True)
