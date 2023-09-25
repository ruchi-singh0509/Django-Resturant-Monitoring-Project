STORE-MONITORING-PROJECT:

A backend system built using Python Django framework and MySQL database to monitor the status(online/offline) of several restaurants in the US. The system keep the tracks whether the stores are online or not during their business hours and provides restaurant owners with detailed reports on store uptime and downtime.


PROBLEM STATEMENT:

This system monitors several restaurants in the US and needs to monitor if the store is online or not. All restaurants are supposed to be online during their business hours.Due to some unknown reasons, a store might go inactive for a few hours.Restaurant owners want to get a report of the how often this happened in the past.
Build backend APIs that will help the restaurant owners achieve this goal.


DATA SOURCE:
CSV files be found in  /StoreProject/CSV_data

We poll every store roughly every hour and have data about whether the store was active or not in a CSV.The CSV has 3 columns (store_id, timestamp_utc, status) where status is active or inactive. All timestamps are in UTC.
We have the business hours of all the stores - schema of this data is store_id, dayOfWeek(0=Monday, 6=Sunday), start_time_local, end_time_local.These times are in the local time zone.
>If data is missing for a store, assume it is open 24*7.
Timezone for the stores - schema is store_id, timezone_str.
>If data is missing for a store, assume it is America/Chicago.
This is used so that data sources 1 and 2 can be compared against each other.

APIs to output a csv file to the user that has the following schema.
Uptime and downtime should only include observations within business hours store_id, uptime_last_hour(in minutes), uptime_last_day(in hours), update_last_week(in hours), downtime_last_hour(in minutes), downtime_last_day(in hours), downtime_last_week(in hours).


LOGIC(Uptime & Downtime):

1.Initialize a dictionary last_one_day_data with keys "uptime", "downtime", and "unit". The values for "uptime" and "downtime" are set to 0, and "unit" is set to "hours".
2.Calculate one_day_ago as the day of the week one day before the current_day. If current_day is 0 (Monday), set one_day_ago to 6 (Sunday).
3.Check if the store is open during the last one day (one_day_ago to current_day) at the current time (current_time).This is done by querying the store.timings to see if there is any entry that matches the conditions for day and time.
4.If the store is not open during the last one day, return the initialized last_one_day_data.
5.If the store is open during the last one day, query the store.Store_status_logs to get all the logs within the last one day (utc_time - 1 day to utc_time) and order by timestamp.
6.Loop through each log in last_one_day_logs:
7.Check if the log's timestamp falls within the store's business hours on that day (log_in_Store_business_hours). This is done by querying the store.timings to see if there is any entry that matches the conditions for day and time.
8.If the log is not within the store's business hours, skip it and move to the next log.
9.If the log's status is "active", increment the "uptime" value in last_one_day_data by 1 hour.
10.If the log's status is not "active", increment the "downtime" value in last_one_day_data by 1 hour.
11.Same logic has been applied for last one hour and last one week uptime and downtime.


APIs:

Trigger Report- Request GET
1. /trigger_report endpoint that will trigger report generation from the data (stored in DB)
    1. No input 
    2. Output - report_id (random string) 
    3. report_id is used for polling the status of report completion

Get Report - Request POST

2. /get_report endpoint that will return the status of the report or the csv
    1. Input - report_id
    2. Output
        >if report generation is not complete, return “Running” as the output
        >if report generation is complete, return “Complete” along with the CSV file

        
TECH-TOOLS-USED:
Python Django rest framework and MySQL databse

SERVER:
to start the server, run the following command in project directory:
python manage.py runserver

The server will start running on
http://localhost:8000


Note: Project is ongoing(resolving minor server issues)
