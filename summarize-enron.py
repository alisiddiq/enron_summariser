from data_plotting.counts_plots import plot_person_activity
from data_process.EmailCollection import EmailCollection
from utils.log_util import init_logger
import run_config
import logging, sys

_logger = logging.getLogger(__name__)

def gen_results(csv_path,
                activity_csv_save_path,
                activity_plots_html_save_path,
                top_n_activity=5):
    """
    :param csv_path: <str> Path to csv that holds the raw data
    :param activity_csv_save_path: <str> Where the activity csv should be saved
    :param activity_plots_html_save_path: <str> Where the activity plots should be saved
    :param top_n_activity: <int> When plotting the activity, how many people should be used
    """
    email_coll = EmailCollection()
    _logger.info('Loading data from {}...'.format(csv_path))
    email_coll.load_from_csv(csv_path=csv_path)
    _logger.info('Generated {} emails'.format(email_coll.email_count))
    _logger.info('Generating sent/recieved counts...')

    counts_df = email_coll.gen_sender_recipients_counts()
    _logger.info('Saving counts to {}'.format(activity_csv_save_path))
    counts_df.to_csv(activity_csv_save_path, index=False)

    top_n_senders = list(counts_df['person'].iloc[0:top_n_activity])

    # This plot opens a dialog box to save as png, as plotly does
    # not have a proper way to export as png yet, they have developed this https://plot.ly/python/static-image-export/
    # but it requires installing some external non python dependencies, hence I did not implement that
    # The plot gets stored as an interactive html file anyway
    _logger.info('Generating plots, and storing interactive version to {}'.format(activity_plots_html_save_path))
    plot_person_activity(emails_coll=email_coll,
                         person_names_list=top_n_senders,
                         image_html_save_path=activity_plots_html_save_path)
    _logger.info('DONE')


if __name__ == '__main__':
    init_logger(logging.INFO)
    raw_csv_path = sys.argv[1]
    gen_results(csv_path=raw_csv_path,
                activity_csv_save_path=run_config.activity_csv_save_path,
                activity_plots_html_save_path=run_config.interactive_plot_path,
                top_n_activity=run_config.top_n_activity)