import time
import requests
import random

sel=random.randint(0,1)
while True:

    x=requests.get("http://192.168.0.141:5000/api/v1/sensors/obstacles")
    json=x.json()
    
    if json["left"]==1 and json["right"]==1:
        pwmL=25
        pwmR=25
        print("dritto")
        sel=random.randint(0,1)
    elif json["left"]==0 and json["right"]==1:
        pwmL=0
        pwmR=25
        print("Sinistra")
        sel=random.randint(0,1)
    elif json["left"]==1 and json["right"]==0:
        pwmL=25
        pwmR=0
        print("destra")
        sel=random.randint(0,1)
    elif json["left"]==0 and json["right"]==0:
        
        if sel==0:
            pwmL=-25
            pwmR=0
        else:
            pwmR=-25
            pwmL=0
        print("stop")
    x=requests.get(f"http://192.168.0.141:5000/api/v1/motors/both?pwmL={pwmL}&pwmR={-pwmR}&time={500}")
    
    #time.sleep(1000)