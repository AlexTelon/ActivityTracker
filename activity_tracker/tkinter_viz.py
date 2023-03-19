from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkcalendar import *
from database import read_data_from_date
from schedule import generate_daily_schedule_chart, merge_consecutive_activities

root = Tk()

# Create a Frame to hold the calendar and plot widgets
frame = Frame(root)
frame.pack(fill=BOTH, expand=True)

# Create a Calendar widget
cal = Calendar(frame, selectmode='day', year=2023, month=3, day=1)
cal.grid(row=0, column=0, padx=10, pady=10)

# Create a tkinter canvas to display the plot
plot_widget = None

def display_activity_data(event):
    global plot_widget

    # Get the selected date from the Calendar widget
    date = cal.selection_get()

    data = read_data_from_date(date)

    # Merge consecutive activities
    merged_data = merge_consecutive_activities(data)

    # Generate the daily schedule chart
    fig = generate_daily_schedule_chart(merged_data, date)

    # Clear the previous plot, if any
    if plot_widget is not None:
        plot_widget.grid_forget()

    # Create a FigureCanvasTkAgg object from the generated plot
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()

    # Create a tkinter canvas to display the plot
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+E+W)

# Bind the display_activity_data function to the <<CalendarSelected>> event
cal.bind("<<CalendarSelected>>", display_activity_data)

root.mainloop()
