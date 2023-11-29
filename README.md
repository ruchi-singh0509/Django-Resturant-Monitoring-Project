# Store Monitoring Project

This is a backend system built using the Python Django framework and a MySQL database to monitor the status (online/offline) of several restaurants in the US. The system keeps track of whether the stores are online or not during their business hours and provides restaurant owners with detailed reports on store uptime and downtime.

## Problem Statement

This system monitors several restaurants in the US and needs to monitor if the store is online or not. All restaurants are supposed to be online during their business hours. Due to some unknown reasons, a store might go inactive for a few hours. Restaurant owners want to get a report of how often this happened in the past. Build backend APIs that will help the restaurant owners achieve this goal.

## Data Source

CSV files can be found in the `/StoreProject/CSV_data` directory.

We poll every store roughly every hour and have data about whether the store was active or not in a CSV file. The CSV has 3 columns (`store_id`, `timestamp_utc`, `status`) where `status` is active or inactive. All timestamps are in UTC.

We have the business hours of all the stores - the schema of this data is `store_id`, `dayOfWeek` (0=Monday, 6=Sunday), `start_time_local`, `end_time_local`. These times are in the local time zone. If data is missing for a store, assume it is open 24*7.

The timezone for the stores - the schema is `store_id`, `timezone_str`. If data is missing for a store, assume it is America/Chicago. This is used so that data sources 1 and 2 can be compared against each other.

## Logic (Uptime & Downtime)

1. Initialize a dictionary `last_one_day_data` with keys "uptime", "downtime", and "unit". The values for "uptime" and "downtime" are set to 0, and "unit" is set to "hours".
2. Calculate `one_day_ago` as the day of the week one day before the `current_day`. If `current_day` is 0 (Monday), set `one_day_ago` to 6 (Sunday).
3. Check if the store is open during the last one day (from `one_day_ago` to `current_day`) at the `current_time`. This is done by querying the store timings to see if there is any entry that matches the conditions for the day and time.
4. If the store is not open during the last one day, return the initialized `last_one_day_data`.
5. If the store is open during the last one day, query the store `Store_status_logs` to get all the logs within the last one day (from `utc_time - 1 day` to `utc_time`) and order by timestamp.
6. Loop through each log in `last_one_day_logs`:
    - Check if the log's timestamp falls within the store's business hours on that day (`log_in_Store_business_hours`). This is done by querying the store timings to see if there is any entry that matches the conditions for the day and time.
    - If the log is not within the store's business hours, skip it and move to the next log.
    - If the log's status is "active", increment the "uptime" value in `last_one_day_data` by 1 hour.
    - If the log's status is not "active", increment the "downtime" value in `last_one_day_data` by 1 hour.
7. The same logic has been applied for the last one hour and last one week uptime and downtime.

## APIs

1. Trigger Report - Request GET
    - Endpoint: `/trigger_report`
    - Description: This endpoint triggers the generation of a report from the data stored in the database.
    - Input: None
    - Output: report_id (random string)
    - Comment: The `report_id` is used for polling the status of the report completion.

2. Get Report - Request POST
    - Endpoint: `/get_report`
    - Description: This endpoint returns the status of the report or the CSV file.
    - Input: report_id
    - Output:
        - If the report generation is not complete, return "Running" as the output.
        - If the report generation is complete, return "Complete" along with the CSV file.

## Tech Tools Used

- Python Django REST Framework
- MySQL Database

## Running the Server

To start the server, run the following command in the project directory:

```
python manage.py runserver
```

The server will start running on `http://localhost:8000`.

Website: `http://127.0.0.1:3000/StoreProject/README.html`

Note: The project is ongoing and we are resolving minor server issues.
