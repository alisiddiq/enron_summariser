class Email:

    def __init__(self,
                 timestamp,
                 message_identifier,
                 sender,
                 recipients_list,
                 topic=None,
                 mode=None):
        """
        :param timestamp: <datetime> timestamp of message
        :param message_identifier: <str>
        :param sender: <str>
        :param recipients_list: <list [str, ..]> List of recipients
        :param topic: <str>
        :param mode: <str>
        """
        self.timestamp = timestamp
        self.message_identifier = message_identifier
        self.sender = sender
        self.recipients_list = recipients_list
        self.topic = topic
        self.mode = mode

    def __repr__(self):
        return '<ts: {}, from: {}, to: {} recipients>'.format(self.timestamp,
                                                              self.sender,
                                                              len(self.recipients_list))

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'message_identifier': self.message_identifier,
            'sender': self.sender,
            'recipients_list': self.recipients_list,
            'topic': self.topic,
            'mode': self.mode,
        }