import matplotlib.pyplot as plt
import datetime

from database import read_data_from_date

from itertools import groupby

def merge_consecutive_activities(filtered_data):
    merged_data = []

    for _, group in groupby(filtered_data, key=lambda x: x[1]):
        group_list = list(group)
        start_dt, window_name = group_list[0]
        end_dt, _ = group_list[-1]
        merged_data.append((start_dt, end_dt, window_name))

    return merged_data


def generate_daily_schedule_chart(filtered_data, date=None):
    if date is None:
        date = datetime.date.today()

    fig, ax = plt.subplots(figsize=(10, 7))

    for start_dt, end_dt, window_name in filtered_data:
        if window_name != "offline":
            duration = (end_dt - start_dt).seconds / 3600
            ax.bar(date, duration, bottom=start_dt.hour + start_dt.minute / 60, width=0.8, label=window_name, alpha=0.7)


    ax.set_ylim(0, 24)
    ax.set_yticks(range(25))
    ax.set_yticklabels([f"{i:02d}:00" for i in range(25)])
    ax.set_ylabel("Time")
    ax.set_title(f"Daily Tool Usage Schedule ({date.strftime('%Y-%m-%d')})")

    ax.set_xticks([date])
    ax.set_xticklabels([date.strftime('%Y-%m-%d')])

    plt.tight_layout()

    handles, labels = [], []
    for bar in ax.containers:
        label = bar.get_label()
        if label not in labels:
            handles.append(bar)
            labels.append(label)
    ax.legend(handles, labels, loc='upper right')

    plt.show()

def main():
    date = datetime.date(2023, 3, 19)  # Replace with the desired date or None for the current day
    filtered_data = read_data_from_date(date)
    merged_data = merge_consecutive_activities(filtered_data)
    generate_daily_schedule_chart(merged_data, date)

if __name__ == "__main__":
    main()
