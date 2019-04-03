import csv
from datetime import datetime
from data_process.Email import Email
import itertools
import pandas as pd
from collections import Counter
import logging

_logger = logging.getLogger(__name__)


class EmailCollectionException(Exception):
    pass

class EmailCollection:

    HEADERS = [
            'timestamp',
            'message_identifier',
            'sender',
            'recipients',
            'topic',
            'mode'
        ]

    def __init__(self):
        self.emails = []

    @property
    def email_count(self):
        return len(self.emails)

    def __repr__(self):
        return '<EmailCollection: email_count = {}>'.format(self.email_count)

    def _add_row(self, row_dict):
        ts = datetime.fromtimestamp(int(row_dict['timestamp'])/1000)
        recipients_list = list(set([r.strip() for r in row_dict['recipients'].split('|') if r.strip() != '']))
        clean_sender = row_dict['sender'].strip()
        if clean_sender == '':
            _logger.warning('Found email with id = {}, having no sender, adding to collection as unknown_sender'.format(row_dict['message_identifier']))
            clean_sender = 'unknown_sender'

        email_obj = Email(
            timestamp=ts,
            message_identifier=row_dict['message_identifier'],
            sender=clean_sender,
            recipients_list=recipients_list,
            topic=row_dict['topic'],
            mode=row_dict['mode']
        )
        self.emails.append(email_obj)

    def load_from_csv(self, csv_path):
        """
        Must have the data organised as specified in EmailCollection.HEADERS
        :param csv_path: <str> Path of CSV that includes the raw data
        """
        # Could also use Pandas, but this is more memory efficient
        with open(csv_path, "r") as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                row_dict = {col: val for col, val in zip(EmailCollection.HEADERS, row)}
                self._add_row(row_dict=row_dict)

    def load_from_db(self, db_con):
        pass

    def gen_person_activity(self, person_name):
        """
        :param person_name: <str> Name of person for whom activity needs to be generated
        :return: <pd.DataFrame> datetime indexed, with columns [sent, received, sender_name, person_name]
        """
        emails_activity = []
        for e in self.emails:
            sent = 0
            received = 0
            sender_name = None

            if e.sender == person_name or person_name in e.recipients_list:
                if e.sender == person_name:
                    sent = 1
                if person_name in e.recipients_list:
                    received = 1
                    sender_name = e.sender

                emails_activity.append({
                    'time_stamp': e.timestamp,
                    'sent': sent,
                    'received': received,
                    'sender_name': sender_name,
                    'person_name': person_name
                })

        return pd.DataFrame(emails_activity).set_index('time_stamp')


    def gen_sender_recipients_counts(self):
        """
        :return: <pd.DataFrame> With columns [person, sent, received]
        """
        if self.email_count == 0:
            raise EmailCollectionException('Collection not populated')

        all_email_recips = []
        all_email_senders = []

        for e in self.emails:
            all_email_recips.append(e.recipients_list)
            all_email_senders.append(e.sender)

        flattened_recipients_list = list(itertools.chain.from_iterable(all_email_recips))
        recip_counts = Counter(flattened_recipients_list)
        sender_counts = Counter(all_email_senders)

        all_unique_individuals = set(flattened_recipients_list + all_email_senders)

        name_counts_list = [{'person': n,
                             'sent': sender_counts[n],
                             'received': recip_counts[n]} for n in all_unique_individuals]
        counts_df = pd.DataFrame(name_counts_list)
        return counts_df.sort_values('sent', ascending=False)