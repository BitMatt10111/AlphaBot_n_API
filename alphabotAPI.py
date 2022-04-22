import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for, make_response
app = Flask(__name__)

sec=3
DR = 16
DL = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

class AlphaBot(object): #classe per gestire il moviemento dell'AlphaBot
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 25
        self.PB  = 25
        
        #setup iniziale del bot
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def right(self, sec): #funzione che ruota sul posto verso destra il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def stop(self): #funzione che ferma il bot
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self, sec): #funzione che ruota sul posto verso sinistra il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def forward(self, sec, speed=30): #funzione che muove avanti il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def backward(self, sec, speed=30): #funzione che muove indietro il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma
	    
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

a=AlphaBot()

@app.route('/api/v1/sensors/obstacles', methods=["GET"])
def sensors_api():
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    sDict={"left":DL_status,"right":DR_status}
    return sDict

@app.route('/api/v1/motors/both', methods=["GET"])    #/api/v1/motors/both?pwmL={pwmL}&pwmR={pwmR}&time={time}
def motors_api():
    pwmL=int(request.args["pwmL"])
    pwmR=int(request.args["pwmR"])
    #t=int(request.args["time"])
    a.set_motor(pwmL,pwmR)

if __name__=="__main__":
    app.run(debug=True, host='192.168.0.141')
