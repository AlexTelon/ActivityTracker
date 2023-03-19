from collections import Counter
import matplotlib.pyplot as plt

import database

def calculate_usage_percentages(data):
    data = [name for _, name in data if name != 'idle']
    total_count = len(data)
    usage = Counter(data)

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
    data = database.read_all()
    percentages = calculate_usage_percentages(data)
    display_pie_chart(percentages)
