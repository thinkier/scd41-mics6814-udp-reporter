import math
import time

import pimoroni_i2c
import breakout_scd41
from breakout_mics6814 import BreakoutMICS6814

from machine import Timer


PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
i2c = pimoroni_i2c.PimoroniI2C(**PINS_BREAKOUT_GARDEN)

class CO2Sensor:
    co2 = 0
    temp = 0
    hum = 0
    
    def __init__(self, task=False):
        global i2c
        breakout_scd41.init(i2c)
        breakout_scd41.start()

        if task:
            self.sensor_timer = Timer(period=1000, mode=Timer.PERIODIC, callback=self.measure_task)

    def measure(self):
        self.co2, self.temp, self.hum = breakout_scd41.measure()

    def measure_wait(self):
        while not breakout_scd41.ready():
            time.sleep_ms(10)
        self.co2, self.temp, self.hum = breakout_scd41.measure()

    def measure_task(self, timer: Timer):
        if not breakout_scd41.ready():
            return # Avoid backpressure issues with time.sleep_ms()
        self.measure()
    

class COSensor:
    co = 0
    
    def __init__(self, task=False):
        global i2c
        self.gas = BreakoutMICS6814(i2c)
        
        if task:
            self.sensor_timer = Timer(period=1000, mode=Timer.PERIODIC, callback=self.measure_task)
        
    def measure_task(self, timer: Timer):
        self.measure()
    
    def measure(self):
        # https://github.com/Seeed-Studio/Mutichannel_Gas_Sensor/blob/master/MutichannelGasSensor.cpp#L333
        red = self.gas.read_reducing()
        self.co = math.pow(red, -1.179) * 4.385 * 1e3


