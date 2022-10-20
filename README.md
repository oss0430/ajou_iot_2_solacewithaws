# Ajou IoT system assignment
![System_Configuration](./img/System_Configuration.PNG)

Device 1 measures the light level and publish to Solace, While subscribed to AWS. 

Device 2 is subscribe to solace. Whenever Device 2 receive the light level by solace it checks if the light level cross certain threshold.

If the threshold is crossed takes a picture and publish it to AWS.

Device 1 then receives the picture and store it. 


## How to Run

### for device 1
```
cd src
python device_1.py
```

### for device 2
```
cd src
python device_2.py
```
