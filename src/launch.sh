# while true; do ./miri_fm -e 2 -g 10 -f 28074000 -M usb -w 8000000 | play -t raw -r24k -es -b 16 -c 1 -V1 - lowpass 3k; done

./miri_fm -e 2 -g 10 -f 28074000 -M usb -w 8000000 | play -t raw -r24k -es -b 16 -c 1 -V1 - lowpass 3k
