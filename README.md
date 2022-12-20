# Copenhagen Airport average precipation for each weekday
Average rainfall at Copenhagen Airport

Simple script pulling data from DMI meteorological observation API.

The script fetches a year worth of hourly precipation data from the Copenhagen Airport weather station. It then sums the daily precipation and computes mean/standard deviation for each weekday.

# Result

Note it is not possible with negative precipation but the error plot simply uses the standard deviation and it may give the impression that is the case.

![Alt text](result.png?raw=true "Rainfall")
