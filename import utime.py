import utime 

def read_line(usb, poll, timeout_ms=20):
    deadline = utime.ticks_add(())