#!/usr/bin/env python3
import subprocess, time, sys
def adb(*args): subprocess.run(['adb', *args], check=True)
def tap(x,y): adb('shell','input','tap',str(x),str(y))
def swipe(x1,y1,x2,y2,ms): adb('shell','input','swipe',str(x1),str(y1),str(x2),str(y2),str(ms))
def main():
    pass
if __name__ == '__main__':
    main()