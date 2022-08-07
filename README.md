# pvmonitor
Easy to use, continuous python monitor for epics pv's

Usage:
 ```
 from pvmonitor import PvMonitor
 my_pvs = ["pv1","pv2"]
 monitor = PvMonitor(my_pvs)
 
 # get data in the form of a dataframe
 my_data = monitor.data
