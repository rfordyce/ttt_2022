# ttt_2022

This is a simple project to familiarize myself again with microcontroller logic, image detection, and generally real-world robotics issues at a very small scale

It's based on Python, Docker, and the cheapest robot arm I could get my hands on quickly

## Running

WARNING this is under development and will _not_ yet work for you, even if you set your arm up like mine!

```shell
docker-compose up --build --force-recreate --remove-orphans --detach && docker logs gridsolver_backend_1 -f
```

## About Setup

The arm base is an Adeept "Arduino Compatible DIY 5-DOF Robotic Arm Kit", which was the cheapest arm I thought looked like it would actually work
- https://smile.amazon.com/gp/product/B09PQFF912/ ($76 shipped after some discounts)
- https://www.adeept.com/adeept-arduino-compatible-diy-5-dof-robotic-arm-kit-for-arduino-uno-r3-steam-robot-arm-kit-with-arduino-and-processing-code_p0118.html

Also plan to use [9-DOF Adafruit BNO055](https://www.adafruit.com/product/2472) which I pinched from a defunct project (expect $35) .. should help deal with the _incredible_ joint slop (maybe 1cm) by placing it as close to the pen tip as possible (at least on the plate, hopefully near the pen tip)

I also found a terrific 2012-era webcam in a box of parts (Logitech) to use here too

An As Seen On TV™ lightswitch provides consistent lighting from a very small gantry (also hosts webcam)

No Lego was harmed in the making of this project

## Current Development Stages and Issues!

### Successes

- Docker builds work great and can connect to the webcam from inside the backend container
- fixing rotation of board seems to work well and also returns a translation matrix from the original camera to the new board corners!
- Arduino IDE doesn't work under Ubuntu, but it was easy to fix (see robot-arm README)
- Arm was very easy to construct, a great demo, surprisingly fast, and seems sufficiently strong to draw (advertised feature)

Working Demo of workflow to get contours > rotate > crop
![contours_rotate_crop.png](/_img/contours_rotate_crop.png)

### Detection

Template discovery works incredibly well if the template is an exact match, otherwise results vary wildly

However, this is somewhat fixed by the board and possible keys being very simplistic

I strongly suspect that a workflow around some sort of bounded matrix comparison for each block and then picking the best of the three choices for it will make detection work well (surprisingly, histogram doesn't seem to work nicely, though it could be misuse on my part)
- orient and crop reasonably (working!)
- slice into 9 blocks
- compare
- select best match (beware empty may be troublesome to detect)

Exact template matching (and especially note non-detection)
![exact_template_matching.png](/_img/exact_template_matching.png)

### Arm Drawing

Arm has some deep pains, largely around it being much too cheap
- lack of encoders means the position is mostly a guess (perhaps fixed by 9-DOF)
- fairly spectacular joint slop

[![IMAGE ALT TEXT](http://img.youtube.com/vi/Q2_ObO06iwE/0.jpg)](http://www.youtube.com/watch?v=Q2_ObO06iwE "Video Title")
