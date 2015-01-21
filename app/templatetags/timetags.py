from django import template
import datetime, time
register = template.Library()

def print_timestamp(timestamp):
    try:
        #assume, that timestamp is given in seconds with decimal point
        ts = float(timestamp/1000.0) + 19800.0
    except ValueError:
        return None

    return time.strftime("%a, %b %d, %I:%M %p", time.gmtime(ts))
    return datetime.datetime.fromtimestamp(ts)

register.filter(print_timestamp)