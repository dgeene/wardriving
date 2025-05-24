# Wardriving
A database for storing netstumbler captures. (Or captures from other wardriving programs down the road)

A 'Session' is an output file produced by running the scanner for a period of time.

I want the database to serve a few purposes.
- Store a list of mac addresses.
- Provide coordinates on when and where this mac address was 'seen' at
- What the name of the network was called at the time that it was seen.'

A few other considerations
- A mac address could technically be seen in multiple sessions. Or locations.
- No duplicates in the master mac address table.

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

## Running tests
From the project root
```shell
python -m pytest -vs tests/test_main.py
```