# Windows Activity Tracker

This is a local only way to track your activity on Windows. It runs in the background and periodicaly checks for which window is active and logs it to a local sqlite database.

The code for this is short and easy to modify.

There is also a configuration file `patterns.json` that allows you to specify which patterns to match for. I should create a tool to more easily debug this.
I basically ran a modified main that looked at the current window every second only printed the result of the regex match. If it did not match it wrote the window title and the classname. That way you can quickly debug which patterns you need to add/change for the tools you are using daily.

Then there are some tools to visualise the data. But with chatGPT it should be easy to generate your own if I never get around to improve these myself.

## Setup

```bash
pip install .
activity_tracker
# this will now run and track your activity and store it.
# Data is store to the local file: time_tracking_data.sqlite
```
