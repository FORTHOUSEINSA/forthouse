#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
import pygame,sys
import math
#ADW_PTR7.py
#version of october 2013
#source code can probably be simplified 
 
#GPIO-Pins connected to the TLC549 
AD_Dat  = 24  # 
AD_Clk = 8
AD_CS = 7   #

#buttons HOLD1, HOLD2, RES
HOLD1=11
HOLD2=10
RES=9

#GPIO definitions
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#TLC549
GPIO.setup(AD_CS,GPIO.OUT)
GPIO.setup(AD_Dat,GPIO.IN)
GPIO.setup(AD_Clk,GPIO.OUT)
#HOLD1, HOLD2, RES
GPIO.setup(HOLD1,GPIO.IN)
GPIO.setup(HOLD2,GPIO.IN)
GPIO.setup(RES,GPIO.IN)


def ADin():
	
    GPIO.output(AD_Clk,GPIO.LOW)# AD_Clk auf 0
    AD_res=0
    for n in range(10):
        time.sleep(0.05)        		
        GPIO.output(AD_CS,GPIO.HIGH)# AD_CS auf 1
        MSB=128
        time.sleep(0.001)
        GPIO.output(AD_CS,GPIO.LOW)# AD_CS auf 0
        time.sleep(0.0005)
        AD_value=0
        for z in range(8):
            if (GPIO.input(AD_Dat)):
                AD_value=AD_value+MSB 
            GPIO.output(AD_Clk,GPIO.HIGH)# AD_Clk auf 1
            time.sleep(0.0005)
            GPIO.output(AD_Clk,GPIO.LOW)# AD_Clk auf 0	 
            MSB=MSB>>1
            time.sleep(0.0005)
            result=AD_value
        GPIO.output(AD_CS,GPIO.HIGH)# AD_CS auf 1    
        AD_res=AD_res+AD_value
    AD_res=AD_res/10
    result=AD_res    
    return result

def conversion(value0):
    value=value0
    value=value*1960 #fuer 5V  
    value=value/1000
    pic_value=value/2 #
    one=value/100
    rest_z=value % 100
    tenth=rest_z/10
    hundredth=rest_z%10
    return one, tenth, hundredth, pic_value,value
    

#Color definitions can be extended for other colors
black = (  0,   0,   0)
white = (255, 255, 255)
blue =  (  0,   0, 255)
green = (  0, 255,   0)
red =   (255,   0,   0)
yellow=(255,255,0)
magenta=(255,0,255)
cyan=(0,255,255)
orange=(255,128,64)
brown=(128,64,0)
lilac=(128,0,255)
grey=(192,192,192)



#Enter the colors and values for the representation
print "*** background color ***"
print"black,white,blue,green,red,yellow"
print"magenta,cyan,orange,brown,lilac,grey"
back_col = input("back_col:")
print
print "*** foreground color ***"
print"black,white,blue,green,red,yellow"
print"magenta,cyan,orange,brown,lilac,grey"
print
fore_col = input("fore_col:")	
print
Caption_disp=raw_input("Caption_disp: ") 
#definitions for width and height: Width:500,Height:380"
print
print"factor for the size of the representation"
dis_f=input("dis_f: ")#
#at a few factors errors in the presentation of the scale may occur
print
pygame.init()
area =pygame.display.set_mode((int(500*dis_f),int(380*dis_f)))
area.fill(back_col)
pygame.display.set_caption(Caption_disp)
#first logical states
GPIO.output(AD_CS,GPIO.LOW)# AD_CS auf 0
GPIO.output(AD_Clk,GPIO.LOW)# AD_Clk auf 0


while True:
	
    value0=ADin()
       
    value_tmp=value0
       
    #conversion(value0)
    one,tenth,hundredth,pic_value,value=conversion(value0)    
    print "mesure : value \n"
    #first delete the area of the changing display value 
    #                                  
    pygame.draw.rect(area,back_col,(int(165*dis_f),int(295*dis_f),int(175*dis_f),int(60*dis_f)))
    #represent the current value
    m_font=pygame.font.Font.set_bold
    m_font=pygame.font.SysFont("COURIERNew",int(40*dis_f))
    #digital display     
    label_H=m_font.render("  "+str(one)+"."+str(tenth)+str(hundredth)+"V",1,fore_col)
    #   
    area.blit(label_H,(int(160*dis_f),int(300*dis_f)))#
                  
    # now presentation of the pointer
        
    x1_zg=int(250*dis_f)  # beginning of the pointer
    y1_zg=int(270*dis_f)
    
    #first delete the range of motion of the pointer(area of a sector of a circle) 
    for x in range (250):
        Cosinus_L=math.cos(math.pi*x/360+math.pi*27.5/180)
        Sinus_L=math.sin(math.pi*x/360+math.pi*27.5/180)
    #       165 length of the poiner
        lpx=int(165*dis_f*Cosinus_L)#
        lpy=int(165*dis_f*Sinus_L)#
        pygame.draw.line(area,back_col,(x1_zg,y1_zg),(x1_zg-lpx,y1_zg-lpy),1) 	
    
    
    Cosinus=math.cos(math.pi*pic_value/360+math.pi*27.5/180)
    Sinus=math.sin(math.pi*pic_value/360+math.pi*27.5/180)
    #       165 length of the pointer
    #       pointer extends into the range scale in
    lpx=int(165*dis_f*Cosinus)#
    lpy=int(165*dis_f*Sinus)#
    
    #draw new line for pointer   
    pygame.draw.line(area,fore_col,(x1_zg,y1_zg),(x1_zg-lpx,y1_zg-lpy),1)   
   
   
   #represent scale
    #short strokes
    for k in range(21):
        Cosinus_s=math.cos(12.5*k*math.pi/360+math.pi*27.5/180)
    #point on a circular arc with radius 175
        lpx_s=int(175*dis_f*Cosinus_s)
        Sinus_s=math.sin(12.5*k*math.pi/360+math.pi*27.5/180)
        lpy_s=int(175*dis_f*Sinus_s)
        Cosinus=math.cos(12.5*k*math.pi/360+math.pi*27.5/180)
    # point on a circular arc with radius 150
        lpx=int(150*dis_f*Cosinus)
        Sinus=math.sin(12.5*k*math.pi/360+math.pi*27.5/180)
        lpy=int(150*dis_f*Sinus)
        #first delete, so drawing with background color
        pygame.draw.line(area,back_col,(x1_zg-lpx_s,y1_zg-lpy_s),(x1_zg-lpx,y1_zg-lpy),1)
        # So now represent line with forground color
        pygame.draw.line(area,fore_col,(x1_zg-lpx_s,y1_zg-lpy_s),(x1_zg-lpx,y1_zg-lpy),1) 
    #long strokes
    for k in range(6):
        Cosinus_s=math.cos(50*k*math.pi/360+math.pi*27.5/180)
    #point on a circular arc with radius 185    
        lpx_s=int(185*dis_f*Cosinus_s)
        Sinus_s=math.sin(50*k*math.pi/360+math.pi*27.5/180)
        lpy_s=int(185*dis_f*Sinus_s)
        Cosinus=math.cos(50*k*math.pi/360+math.pi*27.5/180)
     #point on a circular arc with radius 150
        lpx=int(150*dis_f*Cosinus)
        Sinus=math.sin(50*k*math.pi/360+math.pi*27.5/180)
        lpy=int(150*dis_f*Sinus)
        
        
        #now line drawing with foreground color
        pygame.draw.line(area,fore_col,(x1_zg-lpx_s,y1_zg-lpy_s),(x1_zg-lpx,y1_zg-lpy),1) 
    
    if (GPIO.input(HOLD1)==0):	 
        #min display as the main display down in the middle
        
        value0=value_tmp
        one,tenth,hundredth,pic_value,value=conversion(value0) 
        #first delete subarea      
        #                               
        pygame.draw.rect(area,back_col,(int(25*dis_f),int(300*dis_f),int(120*dis_f),int(60*dis_f)))
        #then representing in writing low height  
        m_font=pygame.font.SysFont("COURIERNew",int(30*dis_f))  
        label_min=m_font.render(str(one)+"."+str(tenth)+str(hundredth)+"V",1,fore_col)
        area.blit(label_min,(int(40*dis_f),int(320*dis_f)))
        one,tenth,hundredth,pic_value,value=conversion(value0) 
        
   #marking1
        mark_value=pic_value
    
    #cosine and sine of the pointer, since the same angle 
    #
        Cosinus=math.cos(math.pi*pic_value/360+math.pi*27.5/180)
        Sinus=math.sin(math.pi*pic_value/360+math.pi*27.5/180)
     #point on a circular arc with radius 160   
        lpx=int(160*dis_f*Cosinus)
        lpy=int(160*dis_f*Sinus)
     #point on a circular arc with radius 210   
        lpx1_m=int(210*dis_f*Cosinus)
        lpy1_m=int(210*dis_f*Sinus)
     #point on a circular arc with radius 190  
        lpx2_m=int(190*dis_f*Cosinus)
        lpy2_m=int(190*dis_f*Sinus)
    #line drawing for marking                                      
        pygame.draw.line(area,fore_col,(x1_zg-lpx1_m,y1_zg-lpy1_m),(x1_zg-lpx2_m,y1_zg-lpy2_m),1)   
       
    
    if (GPIO.input(HOLD2)==0):     
        #max display
        
        value=value_tmp
        one,tenth,hundredth,pic_value,value=conversion(value) 
        #first delete subarea
        #                               
        pygame.draw.rect(area,back_col,(int(360*dis_f),int(300*dis_f),int(120*dis_f),int(60*dis_f)))
        #represent in writing low height
        #                               
        m_font=pygame.font.SysFont("COURIERNew",int(30*dis_f))  
        label_max=m_font.render(str(one)+"."+str(tenth)+str(hundredth)+"V",1,fore_col)
        area.blit(label_max,(int(370*dis_f),int(320*dis_f)))#war 40,30        
        value=value_tmp
        one,tenth,hundredth,pic_value,value=conversion(value) 
    
        mark_value=pic_value
        #marking2
        #cosine and sine of the pointer, since the same angle  
        #
        Cosinus=math.cos(math.pi*pic_value/360+math.pi*27.5/180)
        Sinus=math.sin(math.pi*pic_value/360+math.pi*27.5/180)
    # point on a circular arc with radius160
        lpx=int(160*dis_f*Cosinus)
        lpy=int(160*dis_f*Sinus)
    #point on a circular arc with radius 210     
        lpx1_m=int(210*dis_f*Cosinus)#210
        lpy1_m=int(210*dis_f*Sinus)
    #point on a circular arc with radius 190    
        lpx2_m=int(190*dis_f*Cosinus)#190
        lpy2_m=int(190*dis_f*Sinus)
    # line drawing for marking           
        pygame.draw.line(area,fore_col,(x1_zg-lpx1_m,y1_zg-lpy1_m),(x1_zg-lpx2_m,y1_zg-lpy2_m),1)   
       
    if (GPIO.input(RES)==0):
	#first delete the area with markers 
        for x in range (250):
            Cosinus_ML=math.cos(math.pi*x/360+math.pi*27.5/180)
            Sinus_ML=math.sin(math.pi*x/360+math.pi*27.5/180)
            #lpx=int(160*dis_f*Cosinus)
            #lpy=int(160*dis_f*Sinus)
            lpx1_ML=int(210*dis_f*Cosinus_ML)
            lpy1_ML=int(210*dis_f*Sinus_ML)
            lpx2_ML=int(190*dis_f*Cosinus_ML)
            lpy2_ML=int(190*dis_f*Sinus_ML)
          # delete area of marks      
            pygame.draw.line(area,back_col,(x1_zg-lpx1_ML,y1_zg-lpy1_ML),(x1_zg-lpx2_ML,y1_zg-lpy2_ML),1)   
       	
       	    # 
       	    # delete range of the left number value                               
        pygame.draw.rect(area,back_col,(int(25*dis_f),int(300*dis_f),int(120*dis_f),int(60*dis_f)))
             
            # delete range of the right number value 
            #                               
        pygame.draw.rect(area,back_col,(int(360*dis_f),int(300*dis_f),int(120*dis_f),int(60*dis_f)))
         
                
    pygame.display.update()
    
    
    
GPIO.Cleanup()	

