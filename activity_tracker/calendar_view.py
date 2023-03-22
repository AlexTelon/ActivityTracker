from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
from tkcalendar import *
from database import read_data_from_date
from daily_view import generate_daily_schedule_chart

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

    # Generate the daily schedule chart
    fig = generate_daily_schedule_chart(data, date)

    # Create a FigureCanvasTkAgg object from the generated plot
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()

    # Create a tkinter canvas to display the plot
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=1, padx=10, pady=10, sticky=N+S+E+W)

    # Add a navigation toolbar to the plot widget
    toolbar_frame = Frame(frame)
    toolbar_frame.grid(row=1, column=1, padx=10, pady=10, sticky=E)

    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()
    toolbar.grid(row=1, column=1, padx=10, pady=10, sticky=E)

# Bind the display_activity_data function to the <<CalendarSelected>> event
cal.bind("<<CalendarSelected>>", display_activity_data)

root.mainloop()
