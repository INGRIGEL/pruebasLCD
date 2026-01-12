#!/usr/bin/env python3
# Ejemplo para LCD 32x4 en modo 4-bit usando RPi.GPIO
# Requisitos: python3-rpi.gpio
# Ajusta los pines BCM si usas otros.

import RPi.GPIO as GPIO
import time

# Pines BCM (ajusta si necesitas otros)
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 11

COLS = 32
ROWS = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

def pulse_enable():
    GPIO.output(LCD_E, False)
    time.sleep(0.000001)
    GPIO.output(LCD_E, True)
    time.sleep(0.000001)
    GPIO.output(LCD_E, False)
    time.sleep(0.0001)

def write4bits(nibble):
    # nibble: alto en bits 7..4 (como hace el HD44780)
    GPIO.output(LCD_D4, bool(nibble & 0x10))
    GPIO.output(LCD_D5, bool(nibble & 0x20))
    GPIO.output(LCD_D6, bool(nibble & 0x40))
    GPIO.output(LCD_D7, bool(nibble & 0x80))
    pulse_enable()

def send_byte(bits, mode):
    # mode = True -> data, False -> command
    GPIO.output(LCD_RS, mode)
    high = (bits & 0xF0)
    low  = ((bits << 4) & 0xF0)
    write4bits(high)
    write4bits(low)

def lcd_init():
    time.sleep(0.05)
    GPIO.output(LCD_RS, False)
    # secuencia de inicialización (HD44780)
    for _ in range(3):
        write4bits(0x30)
        time.sleep(0.005)
    write4bits(0x20)
    time.sleep(0.005)
    send_byte(0x28, False)  # 4-bit, 2 lines (compatible)
    send_byte(0x08, False)  # display off
    send_byte(0x01, False)  # clear display
    time.sleep(0.002)
    send_byte(0x06, False)  # entry mode
    send_byte(0x0C, False)  # display on, cursor off, blink off

def lcd_clear():
    send_byte(0x01, False)
    time.sleep(0.002)

def lcd_write_string(text, row=0):
    row_offsets = [0x00, 0x40, 0x14, 0x54]  # mapeo típico 32x4
    if row >= ROWS:
        row = ROWS - 1
    addr = 0x80 + row_offsets[row]
    send_byte(addr, False)
    for ch in text.ljust(COLS)[:COLS]:
        send_byte(ord(ch), True)

if __name__ == "__main__":
    try:
        lcd_init()
        lcd_clear()
        lcd_write_string("Hola desde Raspberry Pi", row=0)
        lcd_write_string("LCD 32x4 - GPIO 4-bit", row=1)
        lcd_write_string("Linea 3", row=2)
        lcd_write_string("Linea 4", row=3)
        time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        lcd_clear()
        GPIO.cleanup()