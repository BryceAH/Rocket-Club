from machine import freq
from hx711 import HX711
import time
import os
from sdcard import SDCard
from machine import SoftSPI
from machine import Pin

led_pin = Pin(2, Pin.OUT)

#STRAIN
#Red to E+
#black to E-
#green to A+
#white to A-

#hx711
#dt to 33
#sck to 32
#GND to GND
#VCC to VIN

#SD CARD
#MISO TO 25
#MOSI TO 26
#SCK TO 27
#CS TO 14

def sd_card(data):
    
    spisd = SoftSPI(-1, miso=Pin(25), mosi=Pin(26), sck=Pin(27))
    sd = SDCard(spisd, Pin(14))

    vfs = os.VfsFat(sd)
    os.mount(vfs, '/sd')
    os.chdir('sd')
    #print('SD Card contains:{}'.format(os.listdir()))
    
    with open("Data.txt", "a") as file:
        file.write(f"{str(data)}\n")
        file.close()
    os.umount('/sd')

driver = HX711(d_out=32, pd_sck=33)

def one_kg(raw_value):
    weight = (0.0009482583 * raw_value) + 405.3651
    return weight
    
def twenty_kg(raw_value):
    weight = (-0.00002109 * raw_value) - 4.95878229
    return weight

def eq_maker(x1,x2,y2):
    
    point1 = x1, 0
    point2 = x2, y2
    
    # Calculate slope (m)
    m = (y2 - 0) / (x2 - x1)
    
    # Calculate y-intercept (b)
    b = 0 - m * x1
    
    print(f"Linear Equation: y = {m}x + {b}")
    print(f"weight = ({m} * raw_value) + {b}")
    
def find_eq():
    zero_av = 0
    non_zero_av = 0
    
    #enter known weight in grams
    known_weight = 50
    
    av = []
    nav = []
    print("empty The scale\nWAIT")
    time.sleep(5)
    for i in range(50):
        raw_value = driver.read()
        #print(raw_value)
        av.append(raw_value)
    average = sum(av) / len(av)
    zero_av = average
    print(f"The average value is {average}\nAdd weight\nWAIT")
    
    time.sleep(7)
    for i in range(50):
        raw_value = driver.read()
        #print(raw_value)
        nav.append(raw_value)
    average = sum(nav) / len(nav)
    non_zero_av = average
    print(f"The average value is {average}")
    
    eq_maker(zero_av,non_zero_av,known_weight)
    
    


def main():
    index = 0
    #for i in range(20):
        
    while index <= 10:
        raw_value = driver.read()
        
        if one_kg(raw_value) > .7:
            led_pin.on()
            index += 1
            mass = round(one_kg(raw_value), 2)
            print(f"{mass} grams")
            sd_card(mass)
            time.sleep(.1)
            led_pin.off()
            
        else:
            led_pin.off()
            #print("0 grams")
            #time.sleep(0.2)
        time.sleep(0.2)
    led_pin.off()
            
def main_without_sd():
    while True:
        raw_value = driver.read()
        if one_kg(raw_value) > .7:
            mass = round(one_kg(raw_value), 2)
            print(f"Raw: {raw_value}  mass: {mass} grams")
            time.sleep(0.5)
        else:
            #print("0 grams")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
    #main_without_sd()
    #find_eq()
    #sd_card()