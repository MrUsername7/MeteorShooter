def check_device():
    device, deviceint = 'Error', -1
    try:
        import Chatter
        device = 'Generic Chatter or other device'
        deviceint = 1
        chatterpins = [Chatter.blPin, Chatter.revision, Chatter.Pins.__dict__]
        chatter2pins = "[Pin(32), 1, {'LORA_MISO': 17, 'INP_PL': 21, 'BATT': 34, 'BUZZ': 19, 'LORA_SCK': 16, 'I2C_SCL': 2, 'LORA_MOSI': 5, 'LORA_DIO1': 18, 'TFT_RST': 15, 'TFT_CS': 0, '__module__': 'Chatter.Pins', 'INP_SCK': 22, 'I2C_SDA': 13, 'TFT_MOSI': 26, '__qualname__': 'Pins', 'LORA_CS': 14, 'TFT_DC': 33, 'TFT_SCK': 27, 'BL': 32, 'INP_DATA': 23}]"
        if str(chatterpins) == chatter2pins:
            device = 'Chatter 2.0'
    except ImportError:
        try:
            import Bit, Codee
            currentmaps = [Bit.pins.currentMap, Codee.pins.currentMap]
            bit1maps = [Bit.pins.Rev1_2Map, Codee.pins.Rev1Map]
            bit2maps = [] #nagovorim tatu da mi kupi
            codee1maps = [] #nagovorim tatu da mi kupi
            codee2maps = [Bit.pins.Rev1_2Map, Codee.pins.Rev2Map]
            if currentmaps == bit1maps:
                device = 'Bit 1.0'
                deviceint = 0
            elif currentmaps == bit2maps:
                device = 'Bit 2.0'
                deviceint = 0
            elif currentmaps == codee1maps:
                device = 'Codee 1.0'
                deviceint = 2
            elif currentmaps == codee2maps:
                device = 'Codee 2.0'
                deviceint = 2
        except ImportError:
            device = 'Other'
            deviceint = 3
    return [device, deviceint]
