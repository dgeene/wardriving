# Wardriving
A database for storing netstumbler captures.

## Schema

Session
A session has data about the capture session
It has a list of mac discovered in that session
```plain
session_id
date
creator
format
start_time = first record
end_time = last record
length - calculated
```


session captures
the capture logs. a mac addr might be seen in multiple captures
possible duplicate macs in 1 session if no gps. we could hash the ssid, mac and time and if the hashes match its a dupe
```plain
capture_id
ssid name
lat
long
time
snr
channelbits
flags
bcn intvl
datarate
lastchannel
fk mac_id
fk session_id
```


Mac
A mac address is seen at a location and with a ssid name at a specific time
```plain
mac_id
mac
```
