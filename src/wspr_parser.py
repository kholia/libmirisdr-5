#!/usr/bin/env python3

import re
import sys

import requests

# ALL.TXT for WSPR looks like:

template = """250205 0718 -19  0.54  28.1260800  G0MBA JO01 23           0  0.43  1  1    0  0   3     1   533
250205 0718 -19  0.49  28.1260900  G0PKT JO01 23           0  0.44  1  1    0  0  14     1   379
250205 0724 -15  6.30  28.1260426  PA0O JO33 37            0  0.52  1  1    0  0   5     1   553
250205 0728 -23  0.45  28.1260800  G0MBA JO01 23           0  0.30  1  1    0  0  27     1   114
250205 0728 -21  0.54  28.1260900  G0PKT JO01 23           0  0.30  1  1    0  0  11     1   419
250205 0728 -26  0.62  28.1261456  OZ7IT JO65 37           0  0.17  1  1    0  0  34     6    39
250205 0738 -15  0.45  28.1260801  G0MBA JO01 23           0  0.50  1  1    0  0   2     1   544
250205 0738 -13  0.49  28.1260915  G0PKT JO01 23           0  0.56  1  1    0  0   2     1   566
250205 0742 -19  0.58  28.1261458  OZ7IT JO65 37           0  0.40  1  1    0  0   8     1   385
250205 0746 -19  6.25  28.1260425  PA0O JO33 37            1  0.33  1  1    0  0  13     1   410
"""

def parse_wspr_message(actual_frequency, message):
    m = re.search(r'(28.12\d+?) ', message)
    if not m:
        with open("/tmp/regex_failed.txt", "w") as f:
            f.write(m)
    text_to_replace = m.group(0).lstrip().rstrip()
    ofrequency = float(text_to_replace)
    offset = int((ofrequency - 28.126000) * 1000000)  # keep wsjt-x on 10m band only ;)
    # print(offset)
    nfrequency = (int(actual_frequency) + offset) / 1000000.0
    nfrequency = "{:.7f}".format(nfrequency)
    # print(nfrequency)
    message = message.replace(text_to_replace, nfrequency)
    targetURL = 'http://wsprnet.org/post'
    wsprFile = '/tmp/all_mept.txt'
    myCall = 'VU3CER'
    myGrid = 'MK68xm'

    with open(wsprFile, "w") as f:
        f.write(message)

    files = { 'allmept': open(wsprFile, 'r') }
    params = { 'call': myCall, 'grid': myGrid }
    try:
        response = requests.post('http://wsprnet.org/post', files=files, params=params)
    except requests.ConnectionError as exception:
        with open('log.txt', 'a') as log_file:
            log_file.write(time.ctime() + ' : connection error connecting to wsprnet.org\n')
            log_file.write( str(exception) + '\n' )
            log_file.close()
            sys.exit(1)

    except requests.exceptions.Timeout:
        with open('log.txt', 'a') as log_file:
            log_file.write(time.ctime() + ' : post request timed out\n')
            log_file.close()
            sys.exit(1)

    except requests.exceptions.RequestException as exception:
        with open('log.txt', 'a') as log_file:
            log_file.write(time.ctime() + ' : catastrophic error posting to wsprnet.org\n')
            log_file.write( str(exception) + '\n' )
            log_file.close()
            sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 wspr_parser.py <F-in-Hz> <WSPR message>")
        sys.exit(1)

    f = sys.argv[1]
    wspr_message = sys.argv[2]
    parse_wspr_message(f, wspr_message)

    """
    for line in template.splitlines():
        line = line.strip()
        parse_wspr_message(line)
    """
