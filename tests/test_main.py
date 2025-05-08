import csv
from datetime import datetime
from collections import deque
from main import strip_parens, Session, Record

class TestStripParens:
    def test_strip_parens1(self):
        ssid = '( Mine )'
        assert strip_parens(ssid) == 'Mine'
    def test_strip_parens2(self):
        ssid = '(  )'
        assert strip_parens(ssid) == ''
    def test_strip_parens3(self):
        ssid = '( 00:1d:7e:66:1f:b0 )'
        assert strip_parens(ssid) == '00:1d:7e:66:1f:b0'


class TestSession:
    def test_scan_date(self):
        s = Session()
        s.scan_date = '2012-06-29'
        assert type(s.scan_date) == datetime
        assert str(s.scan_date) == '2012-06-29 00:00:00'

class TestRecord:
    csv_1 = ['N 41.5281067', 'W 72.7748850', '( liberty )', 'BSS',
            '( c0:c1:c0:01:30:c9 )', '17:12:00 (GMT)', '[ 14 63 49 ]',
            '# (  )', '0411', '00000040', '100', '540', '6']
    
    csv_2 = ['N 41.5281067', 'W 72.7748850', '( librty )', 'BSS',
            '( c0:c1:c0:01:30:c9 )', '17:12:00 (GMT)', '[ 14 63 49 ]',
            '# (  )', '0411', '00000040', '100', '540', '6']

    def test_record_init(self):
        r = Record(self.csv_1)
        assert r.lat == 'N 41.5281067'
        assert r.long == 'W 72.7748850'
        assert r.ssid == 'liberty'
        assert r.mac == 'c0:c1:c0:01:30:c9'
        assert r.time == '17:12:00 (GMT)'
        assert r.name == ''

    def test_record_hash(self):
        r = Record(self.csv_1)
        r2 = Record(self.csv_1)
        assert r.hashify() == r2.hashify()

    def test_record_hash_different(self):
        r = Record(self.csv_1)
        r2 = Record(self.csv_2)
        assert r.hashify() != r2.hashify()

    def test_record_eq_1(self):
        """ test two identical records"""
        r1 = Record(self.csv_1)
        r2 = Record(self.csv_1)
        assert r1 == r2

    def test_record_eq_2(self):
        """ test almost identical records"""
        r1 = Record(self.csv_1)
        r2 = Record(self.csv_2)
        assert r1 != r2
    
class TestDiscardDuplicates:
    """
    Remove as many duplicates as we can from scan files.
    It seems without GPS the scans have duplicate ssids. A lot of them.
    """
    def test_duplicate_record_filtering(self):
        line_queue = deque(maxlen=100)
        hash_set = set()

        s = Session()
        with open('./sample_data/session7-nogps.txt', 'r', newline='', encoding='utf-8') as f:
            for lnumber, line in enumerate(f, start=1):
                if lnumber == 4:
                    break
            reader = csv.reader(f, delimiter='\t')
            first_record = None
            current_record = None
            current_hash = None
            for row in reader:
                if not first_record:
                    first_record = True
                    current_hash = Record(row).hashify()
                    line_queue.append((Record(row), current_hash))
                    hash_set.add(current_hash)
                    continue
                    #first_record = True
                current_record = Record(row)
                current_hash = current_record.hashify()
                if current_hash in hash_set:
                    #print('Duplicate record!')
                    continue
                line_queue.append((current_record, current_hash))
                hash_set.add(current_hash)
                if len(line_queue) > 30:
                    _, old_hash = line_queue[0]
                    hash_set.discard(old_hash)
                #current_record = row
                print(row)
            #s.last_record = Record(current_record)

