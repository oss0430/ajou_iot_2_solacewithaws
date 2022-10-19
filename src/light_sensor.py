import spidev, time

class MySPIDevice():
    
    """
    Anaglod to DC converter using spi
    """

    def __init__(
        self
    ):
        spi = spidev.SpiDev()
        self.spi = spi
        self.spi.open(0,0)
        
    def analog_read(
        self,
        channel
    ):  
        """
        Specify channel to read from, recevie value from 0~1000
        """
        r = self.spi.xfer2([1, (0x08+channel) << 4 , 0])
        adc_out = ((r[1]&0x03)<<8)+r[2]
    
        return adc_out

