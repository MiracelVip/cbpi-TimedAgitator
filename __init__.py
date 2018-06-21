from modules import cbpi
from modules.core.props import Property
from modules.core.hardware import ActorBase
import time

# test

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print (e)
    pass



@cbpi.actor
class TimedAgitator(ActorBase):

    gpio = Property.Select("GPIO", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], description="GPIO to which the actor is connected")
    ta_start = Property.Number("Running Timer", configurable=True, description="Defines how long the Agitator should run before pause.")
    ta_stop  = Property.Number("Pause Timer", configurable=True, description="Defines how long the Agitator should stop before run again.")
    started = 0
    
    def init(self):
        GPIO.setup(int(self.gpio), GPIO.OUT)
        GPIO.output(int(self.gpio), 0)

    def on(self, power=0):
        print ("GPIO ON %s" % str(self.gpio))
        GPIO.output(int(self.gpio), 1)


    def off(self):
        print ("GPIO OFF")
        GPIO.output(int(self.gpio), 0)
        
   

    def timedAggitator (self):
         while (self.started == 1):
            self.api.cache.get("actors").get(int(self.id)).timer =  int(time.time()) + int(self.ta_start) -1
            self.api.switch_actor_on(self.id)
            self.sleep(int(self.ta_start))
            
            self.api.cache.get("actors").get(int(self.id)).timer = int(time.time()) + int(self.ta_stop) -1
            self.api.switch_actor_off(self.id)
            self.sleep(int(self.ta_stop))
                    
         else:
            self.api.cache.get("actors").get(int(self.id)).timer =  None
            self.api.switch_actor_on(self.id)
            self.api.switch_actor_off(self.id)

    
    @cbpi.action("Start Agitator Timer")        
    def start(self):
        self.started = 1
        self.api.notify(headline="Timed Agitator", message="Timed Agitator started", type="info")
        self.timedAggitator()
        
        
    @cbpi.action("Stop Agitator Timer")        
    def stop(self):
        self.api.notify(headline="Timed Agitator", message="Timed Agitator will be stopped after one cycle.", type="info")
        self.started = 0
    
