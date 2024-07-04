import datetime


def preprocess_data(data):
    statistic = []

    for user in data:
        user['ts'] = user['ts'].split('.')[0]
        datetime_ts = datetime.datetime.strptime(
            user['ts'], '%Y-%m-%dT%H:%M:%S')
        statistic.append(float(f'{datetime_ts.hour}.{datetime_ts.minute}'))

    return statistic
