# ttt_2022

running
```shell
docker-compose up --build --force-recreate --remove-orphans --detach && docker logs gridsolver_backend_1 -f
```

### About Robot Arm

Used an Adeept "Arduino Compatible DIY 5-DOF Robotic Arm Kit", which was the cheapest arm I thought looked like it would actually work
- https://smile.amazon.com/gp/product/B09PQFF912/ ($76 shipped after some discounts)
- https://www.adeept.com/adeept-arduino-compatible-diy-5-dof-robotic-arm-kit-for-arduino-uno-r3-steam-robot-arm-kit-with-arduino-and-processing-code_p0118.html
- 9-DOF is an [Adafruit BNO055](https://www.adafruit.com/product/2472) pinched from a defunct project (expect $35) .. should help deal with the _incredible_ joint slop (maybe 1cm) by placing it as close to the pen tip as possible (at least on the plate, hopefully near the pen tip)
