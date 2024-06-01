import pyfirmata2 as pyfirmata
import time

comport = 'COM5'
board = pyfirmata.Arduino(comport)

led_pins = [12, 8, 9, 10, 11]
leds = [board.get_pin('d:{}:o'.format(pin)) for pin in led_pins]

buzzer_pin = 5
buzzer = board.get_pin('d:{}:o'.format(buzzer_pin))

locker_pin = 7
locker = board.get_pin('d:{}:o'.format(locker_pin))

def led(fingerUp):
    for i, status in enumerate(fingerUp):
        leds[i].write(status)
        
def buzz(duration=1):
    buzzer.write(1)
    time.sleep(duration)
    buzzer.write(0)
    
def open_door():
    print("Cửa đã được mở!")
    locker.write(1)
    buzz()
    time.sleep(2)  
    locker.write(0)
    print("Cửa đã được đóng!")

    
             

