import sqlite3
import matplotlib.pyplot as plt

def read_data_from_db():
    with sqlite3.connect('time_tracking_data.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, window_name FROM window_data")
        data = cursor.fetchall()
    return data

def calculate_usage_percentages(data):
    total_count = len(data)
    usage = {}
    
    for _, window_name in data:
        if window_name in usage:
            usage[window_name] += 1
        else:
            usage[window_name] = 1
    
    percentages = {name: (count / total_count) * 100 for name, count in usage.items()}
    return percentages

def display_pie_chart(percentages):
    labels = list(percentages.keys())
    sizes = list(percentages.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Tool Usage")
    plt.show()

if __name__ == "__main__":
    data = read_data_from_db()
    percentages = calculate_usage_percentages(data)
    display_pie_chart(percentages)
