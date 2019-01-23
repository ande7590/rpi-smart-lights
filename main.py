#!/usr/bin/env python

import os
import sys
from time import strftime
from itertools import cycle
from flux_led import WifiLedBulb, BulbScanner, LedTimer

# Time constants
utc_offset = 6
utc_time = int(strftime("%H"))

# Color constants
cool_bright = (255, 255, 255)
warm_bright = (0, 0, 0)
warm_light = (255, 187, 65)
bed_time = (255, 43, 0)

# Color change schedule
color_schedule = {3: bed_time, 5: warm_light, 8: cool_bright,\
                  18: warm_bright, 19: warm_light, 20: bed_time}

def get_hours_between(t1, t2):
    """Finds the number of hours between t2 and t1, order matters"""
    if t1 < t2:
        diff = t2 - t1
    else:
        diff = 24 - t2 + t1
    return diff

def interpolate_color(t1, color1, t2, color2):
    """Interpolate based on time between two colors"""
    curr_time =  float(strftime("%H")) + (float(strftime("%M")) / 60.0)
    numerator = float(get_hours_between(t1, curr_time))
    denominator = float(get_hours_between(t1, t2))
    wt = numerator / denominator
    return tuple(wt * col[0] + (1 - wt) * col[1] for col in zip(color1, color2))

def main():
    """Find lightbulbs on LAN, update their colors according to schedule.  Grade
        between the colors via linear interpolation"""
    # hack to convert UTC to local time
    if utc_time < utc_offset:
        local_time = 24 - utc_offset + utc_time
    else:
        local_time = utc_time - utc_offset
    
    # figure out what the next / last color is so that
    # we can gradually change colors
    color_change_times = list(color_schedule.keys())
    color_change_times.sort()

    last_time = color_change_times[0]
    next_time = color_change_times[len(color_change_times) - 1]
    for change_time in color_change_times:
        if local_time <= change_time:
            last_time = change_time
        if local_time > change_time:
            next_time = change_time

    # get the last / next color
    last_color = color_schedule[last_time]
    next_color = color_schedule[next_time]

    # interpolate the color
    new_color = interpolate_color(last_time, last_color, next_time, next_color)
    print ("Changing color to %s at %s o'clock" % (str(new_color), str(local_time)))

    # Look for bulbs on the LAN
    print "Scanning for bulbs..."
    scanner = BulbScanner()
    num_scan_retries = 10
    while num_scan_retries > 0 and len(scanner.found_bulbs) == 0:        
        scanner.scan(timeout=4)
        num_scan_retries = num_scan_retries - 1

    # print found bulbs
    print "found bulbs:"
    for bulb_info in scanner.found_bulbs:
        print "\t%(id)s: %(ipaddr)s" % bulb_info

    if len(scanner.found_bulbs) > 0:
        for bulb_info in scanner.found_bulbs:
            bulb = WifiLedBulb(bulb_info["ipaddr"])
            bulb.refreshState()
            bulb.setRgb(*new_color, persist=True)

    else:
        print("Can't any find bulbs")

if __name__ == '__main__':
    main()
