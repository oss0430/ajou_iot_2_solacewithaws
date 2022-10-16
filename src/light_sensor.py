import spidev, time

class MySPIDevice():
    
    def __init__(
        self
        #config_max_speed_hz
        ):
        spi = spidev.SpiDev()
        #spi.max_speed_hz = config_max_speed_hz
        self.spi = spi
        self.spi.open(0,0)
        
    def analog_read(
        self,
        channel
        ):
        r = self.spi.xfer2([1, (0x08+channel) << 4 , 0])
        adc_out = ((r[1]&0x03)<<8)+r[2]
    
        return adc_out


"""
spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz = 1000000


    
while True :

    reading = analog_read(1)
    print(reading)
    time.sleep(1)
"""