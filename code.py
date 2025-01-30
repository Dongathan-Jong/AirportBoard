import time
import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import requests

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

def get_metar():
    headers = {
        'accept': '*/*',
    }
    params = {
        'ids': 'cyyz',
        'format': 'raw',
        'taf': 'false',
        'hours': '2',
    }
    response = requests.get('https://aviationweather.gov/api/data/metar', params=params, headers=headers)
    return response.content.decode('utf-8').strip()

def get_current_time():
    headers = {
        'accept': 'application/json',
    }
    params = {
        'timeZone': 'America/Toronto',
    }
    currentTime = requests.get('https://timeapi.io/api/time/current/zone', params=params, headers=headers)
    data = currentTime.json()
    return data['time']

line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xffffff,
    text="CYYZ")
line1.x = 2
line1.y = 5

metar = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xff0000,
    text="METAR:")
metar.x = 2
metar.y = 15

line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x0080ff,    
    text = get_metar())
    
line2.x = display.width
line2.y = 25

timeNow = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xffffff,
    text=get_current_time())
timeNow.x = 33
timeNow.y = 5


g = displayio.Group()
g.append(line1)
g.append(timeNow)
g.append(metar)
g.append(line2)
display.root_group = g



def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width


while True:
    scroll(line2)
    display.refresh(minimum_frames_per_second=0)
    if time.monotonic() % 60 < 1:  
        timeNow.text = get_current_time() 
        display.refresh(minimum_frames_per_second=0)
    if time.monotonic() % 500 < 1:  
        line2.text = get_metar() 
        display.refresh(minimum_frames_per_second=0)
    
