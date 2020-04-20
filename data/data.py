from datetime import date
import time

PATHS = {}


def paths(name):
    if not PATHS:
        pass


def construct_ref(subject: str, exp_date: float, sequence: int) -> str:
    """Constructs an experiment reference string

    constructs and returns a standard format string reference, for the experiment using the 'subject', the 'date' of
    the experiment (a timestamp), and the daily sequence number of the experiment, 'seq' (must be an integer).

    :param str subject: the subject name.
    :param float exp_date: timestamp of the experiment datetime.
    :param int sequence: daily sequence number of the experiment.
    :return: experiment reference
    :rtype: str

    :example:
    >>> construct_ref('default', time.time(), 2)
    '2020-04-12_2_default'
    """
    exp_date = date.fromtimestamp(exp_date)
    return '{}_{}_{}'.format(exp_date, sequence, subject)

