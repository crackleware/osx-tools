#!/usr/bin/env python

# for alternative see: https://pypi.python.org/pypi/PyAutoGUI

# -------------------------------------------------------------------------------------- #

# from: http://stackoverflow.com/a/8202674

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID

from AppKit import NSWorkspace, NSEvent
import time
import sys

def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(
            None, 
            type, 
            (posx,posy), 
            kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);

def mouseclick(posx,posy):
    # uncomment this line if you want to force the mouse 
    # to MOVE to the click location first (I found it was not necessary).
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
    mouseEvent(kCGEventLeftMouseUp, posx,posy);

# -------------------------------------------------------------------------------------- #

if len(sys.argv) >= 2 and sys.argv[1] == 'list':
    winList = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly,
                                         kCGNullWindowID)
    for win in winList:
        print win
    sys.exit(0)

else:
    pid = None
    while 1:
        app = NSWorkspace.sharedWorkspace().activeApplication()
        if pid != app['NSApplicationProcessIdentifier']:
            pid = app['NSApplicationProcessIdentifier']
            winList = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly,
                                                 kCGNullWindowID)
            activeWin = None
            for win in winList:
                if win['kCGWindowOwnerName'] == app['NSApplicationName'] and \
                   win['kCGWindowAlpha'] != 0 and win['kCGWindowLayer'] == 0:
                    print win
                    activeWin = win
                    break
            if activeWin:
                bounds = activeWin['kCGWindowBounds']
                loc = NSEvent.mouseLocation()
                loc.y = 1080 - loc.y # this might need to be tweaked depending on layout of displays
                print (app['NSApplicationName'], bounds['X'], bounds['Y'], bounds['Width'], bounds['Height']), (loc.x, loc.y)
                if loc.x < bounds['X'] or loc.x >= bounds['X'] + bounds['Width'] or \
                   loc.y < bounds['Y'] or loc.y >= bounds['Y'] + bounds['Height']:
                    x = bounds['X'] + bounds['Width']/2
                    y = bounds['Y'] + bounds['Height']/2
                    print 'move to', (x, y)
                    mousemove(x, y)

        time.sleep(0.2)

