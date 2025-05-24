"""
Ingest netstumbler data.
When GPS is inactive we seem to pick up multiples ofthe same SSID.
So filter those out.

csv value positions
0=latitude
1=longitude
2=SSID
3=type
4=BSSID or mac address
5=time spotted in gmt
6=signal to noise
7=name - no idea what this is
8=flags
9=channel bits
10=bcn interval
11=data rate
12=last channel
"""
import re
import csv
import hashlib
from datetime import datetime
from collections import deque
from sqlalchemy import create_engine
import models

pdate = r'\d{4}-\d{2}-\d{2}'
pdata_field = r'\(\s*(.*?)\s*\)' # used for stripping away () from strings

def strip_parens(str) -> str:
    m = re.search(pdata_field, str)
    return m.group(1)


class Record:
    def __init__(self, c: list):
        self.lat = c[0]
        self.long = c[1]
        self.ssid = strip_parens(c[2])
        self.type = c[3]
        self.mac = strip_parens(c[4])
        self.time = c[5]
        self.snr = c[6]
        self.name = strip_parens(c[7])
        self.flags = c[8]
        self.chl_bits = c[9]
        self.bcn_intvl = c[10]
        self.data_rate = c[11]
        self.last_channel = c[12]

    def __eq__(self, value):
        r1 = self.mac + self.ssid + self.time
        r2 = value.mac + value.ssid + value.time
        return r1 == r2
    
    def __repr__(self):
        return f'( {self.ssid} ) - ({self.mac})'

    def hashify(self):
        return hashlib.md5(
            self.mac.encode()+self.ssid.encode()).hexdigest()

class Session:

    @property
    def scan_date(self):
        return self._scan_date
    @scan_date.setter
    def scan_date(self, value):
        self._scan_date = datetime.strptime(value, '%Y-%m-%d')
    @property
    def first_record(self):
        return self._first_record
    @first_record.setter
    def first_record(self, value):
        self._first_record = value
    @property
    def last_record(self):
        return self._last_record
    @last_record.setter
    def last_record(self, value):
        self._last_record = value
    @property
    def duration(self):
        start = datetime.strptime(self.first_record.time, '%H:%M:%S (%Z)')
        start = datetime.combine(self.scan_date, start.time())
        end = datetime.strptime(self.last_record.time, '%H:%M:%S (%Z)')
        end = datetime.combine(self.scan_date, end.time())
        duration = end - start
        return duration


def main(filename):
    queue_depth = 100
    line_queue = deque(maxlen=queue_depth)
    hash_set = set()

    s = Session()
    with open(filename, 'r', newline='', encoding='utf-8') as f:
        for lnumber, line in enumerate(f, start=1):
            if lnumber == 4:
                dmatch = re.search(pdate, line)
                date = dmatch.group()
                s.scan_date = date
                break
            #print(line)
        reader = csv.reader(f, delimiter='\t')
        #reader = itertools.islice(reader, 2, None)
        first_record = None
        current_record = None
        current_hash = None
        duplicates = 0
        for row in reader:
            if not first_record:
                first_record = True
                s.first_record = Record(row)
                current_hash = s.first_record.hashify()
                line_queue.append((s.first_record, current_hash))
                hash_set.add(current_hash)
                continue
            current_record = Record(row)
            current_hash = current_record.hashify()
            if current_hash in hash_set:
                # skip duplicate entries
                duplicates += 1
                continue
            line_queue.append((current_record, current_hash))
            hash_set.add(current_hash)
            if len(line_queue) > queue_depth:
                _, old_hash = line_queue[0]
                hash_set.discard(old_hash)
            print(current_record)
        s.last_record = current_record
        print(f"Scan stats - Date:'{s.scan_date}' Scan Duration: '{s.duration}'")
        print(f"Duplicate entries: {duplicates}")



if __name__ == '__main__':
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
    # prints the DDL for table creation
    print(models.Base.metadata.create_all(engine))
    #main('/home/anon/python/wardriving/sample_data/session1')
    #main('/home/anon/python/wardriving/sample_data/session7-nogps.txt')
