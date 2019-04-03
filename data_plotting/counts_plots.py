import plotly.graph_objs as go
import pandas as pd
from plotly import offline
import matplotlib.pyplot as plt

def gen_n_rgb_colors(n, color_map_name='jet'):
    cm = plt.get_cmap(color_map_name)
    rgb_list = [cm(1.*i/n) for i in range(n)]
    rgb_str_list = ['rgba({}, {}, {}, {})'.format(int(r[0]*255), int(r[1]*255), int(r[2]*255), r[3]) for r in rgb_list]
    return rgb_str_list

def plot_person_activity(emails_coll, image_html_save_path, person_names_list, activity_agg_freq_str='M'):
    """
    :param emails_coll: <data_process.EmailCollection> Populated collection
    :param image_html_save_path: <str> How many prolific senders' activity to plot
    :param person_names_list: <list [str, ..]> List of senders who's activity to plot
    :param activity_agg_freq_str: <str> pandas frequency string for aggregation, defaults to Month
    """
    traces = []
    colors_list = gen_n_rgb_colors(len(person_names_list))
    for ind, p in enumerate(person_names_list):
        p_activity = emails_coll.gen_person_activity(person_name=p)
        sent_agg = p_activity['sent'].groupby(pd.Grouper(freq=activity_agg_freq_str)).sum()
        received_from_unique_agg = p_activity['sender_name'].groupby(pd.Grouper(freq=activity_agg_freq_str)).nunique()

        traces.extend([
            go.Scatter(
                x=sent_agg.index,
                y=sent_agg,
                legendgroup=p,
                mode='lines',
                name='{} sent'.format(p),
                marker=dict(color=colors_list[ind])
            ),
            go.Scatter(
                x=received_from_unique_agg.index,
                y=received_from_unique_agg,
                legendgroup=p,
                mode='lines',
                yaxis='y2',
                name='{} unique received'.format(p),
                marker=dict(color=colors_list[ind])
            ),
        ])

    layout = go.Layout(
        yaxis=dict(title='Sent Count', domain=[0,0.48]),
        yaxis2 = dict(title='Unique Received Count', domain=[0.52, 1]),
        title='Activity Plot'
    )

    fig = go.Figure(data=traces, layout=layout)
    offline.plot(fig,
                 filename=image_html_save_path,
                 image='png',
                 auto_open=True,
                 image_width=1280, image_height=800,
                 )












