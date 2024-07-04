import datetime


def preprocess_data_for_distribution(data):
    statistic = []

    for user in data:
        # Filter only online timestamps
        if user['is_online']:
            # Append each float hour.minute
            user['ts'] = user['ts'].split('.')[0]
            datetime_ts = datetime.datetime.strptime(
                user['ts'], '%Y-%m-%dT%H:%M:%S')
            statistic.append(float(f'{datetime_ts.hour}.{datetime_ts.minute}'))

    return statistic
