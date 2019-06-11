import RPi.GPIO as GPIO
import time

def ADin(AD_Clk, AD_CS, AD_Dat):
    """ 50 mesures = 5 sec """

    GPIO.output(AD_Clk,GPIO.LOW) # AD_Clk sur 0
    AD_res=0
    for n in range(10): 
        time.sleep(0.0001)        		
        GPIO.output(AD_CS,GPIO.HIGH) # AD_CS sur 1
        MSB=128
        time.sleep(0.0001)
        GPIO.output(AD_CS,GPIO.LOW) # AD_CS sur 0
        time.sleep(0.0001)
        AD_value0=0
        for z in range(8):
            if (GPIO.input(AD_Dat)):
                AD_value0=AD_value0+MSB 
            GPIO.output(AD_Clk,GPIO.HIGH) # AD_Clk sur 1
            time.sleep(0.0004)
            GPIO.output(AD_Clk,GPIO.LOW) # AD_Clk sur 0, mesure prise pour 1 bit	 
            MSB=MSB>>1
            time.sleep(0.0004)
            result=AD_value0
        GPIO.output(AD_CS,GPIO.HIGH) # AD_CS sur 1    
        AD_res=AD_res+AD_value0
    AD_res=AD_res/10
    result=AD_res    
    return result
	

def conversion(value0):
	COEFF = 0.0196
	OLD_COEFF = 1960/1000
	result = value0*COEFF
	return result
