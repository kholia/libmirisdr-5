#!/usr/bin/env python3

import sys
import re

template = """N9TTK PD0HLA -13                      a7
<JA1IHD> 7Z1AL/QRP RRR
CQ NA SQ9NKU JO90
YD2BRC RR73; LU3DYU <A43WWA> +00
UR7FM/MM <F5SYC> 73
CQ ES5QA KO38                       ? a1
CQ F5RMK IN98                         a7
EA3ISZ RR73; G8LRS <ZW5B> -10
"""

def parse_ft8_message(message):
    # remove "? a1" / "a7" stuff
    message = message.split("       ")[0].rstrip()
    # remove "<" / ">"
    message = message.replace("<", "").replace(">", "")
    if ";" in message:
        message = message.split(";")[1].lstrip().rstrip()
    values = message.split(" ")
    if len(values) == 2:
        callsign = values[1]
    elif len(values) == 3:
        callsign = values[1]
    elif len(values) == 4:
        callsign = values[2]
    else:
        callsign = "WTF"
    print(callsign)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ft8_parser.py <FT8_message>")
        sys.exit(1)

    ft8_message = sys.argv[1]
    parse_ft8_message(ft8_message)

    """
    for line in template.splitlines():
        line = line.strip()
        parse_ft8_message(line)
    """
