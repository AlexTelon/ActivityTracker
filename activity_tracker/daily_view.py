import matplotlib.pyplot as plt
import datetime
from itertools import groupby
import matplotlib.cm as cm

from database import read_data_from_date

def plot_daily_schedule_chart(filtered_data, date=None):
    fig = generate_daily_schedule_chart(filtered_data, date)
    plt.show()

def generate_daily_schedule_chart(filtered_data, date=None):
    if date is None:
        date = datetime.date.today()

    activity_colors = {
        'offline': 'lightgrey',
        'idle': 'darkgrey'
    }

    activity_names = sorted(list(set([x[1] for x in filtered_data if x[1] not in activity_colors])))
    num_activities = len(activity_names)
    color_map = cm.get_cmap('Set3', num_activities)
    for activity_idx, activity_name in enumerate(activity_names):
        activity_colors[activity_name] = color_map(activity_idx)

    fig, ax = plt.subplots(figsize=(10, 7))

    for activity_name, activity_group in groupby(filtered_data, key=lambda x: x[1]):
        activity_list = list(activity_group)
        start_dt, _ = activity_list[0]
        end_dt, _ = activity_list[-1]

        duration = (end_dt - start_dt).seconds / 3600
        color = activity_colors.get(activity_name, 'black')

        ax.bar(date, duration, bottom=start_dt.hour + start_dt.minute / 60, width=0.8, color=color, label=activity_name, alpha=0.7)

    # Set the y-axis limits to display only the 06:00 - 24:00 range
    ax.set_ylim(6, 24)
    ax.invert_yaxis()
    ax.set_yticks(range(6, 25))
    ax.set_yticklabels([f"{i:02d}:00" for i in range(6, 25)])
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

    return fig



def main():
    date = datetime.date(2023, 3, 19)  # Replace with the desired date or None for the current day
    filtered_data = read_data_from_date(date)
    plot_daily_schedule_chart(filtered_data, date)

if __name__ == "__main__":
    main()
