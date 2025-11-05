# Finray-Fish

## Wiring of Fish (with only motor inside the fish)

![Wiring](/assets/Fish-setting-1.png)

- Wires color for zero-buoyancy wires:
  - orange: CAN_H
  - orange-white: CAN_L
  - blue & blue-white: V+ (24V)
  - brown & brown-white: GND

## Seting up on Jetson Nano (or your own PC)

- Jetson Nano has python 2.7.18 and python 3.8.10 installed by default. If you want to use python3, you need use `python3`.

- Clone this repository to the Jetson Nano. (You might need to setup the ssh key first)

- Create a virtual environment for python3.
  ```
  python3 -m venv finray-fish
  source finray-fish/bin/activate (To deactivate, use `deactivate`)
  pip3 install -r requirements.txt

  ```

- Install the pylkmotor package. (pylkmotor==1.0.4)
  ```
  pip install pylkmotor
  ```

- To use the LK motor package, some changes are made to the original package. The changes are done on the LKMotor.py file. See LKMotor-change.py for the whole changed file.

- USB to CAN Module setup
```
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 up
```

- Run the fish-control-keyboard.py file to control the motors. You will need to use `sudo` to run the file because of the keyboard package.
  ```
  sudo finray-fish/bin/python3 Control_python-can/fish-control-keyboard.py 
  ```

## Keyboard Control

- If "w" is pressed, the motor rotating speed will increase
  - Global var `target_Speed += 5` degrees/second
  - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque` 
- If "x" is pressed, the motor rotating speed will decrease
  - Global var `target_Speed -= 5`  degrees/second
  - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque`


- If "a" is pressed, the motor phase differences will turn to the positive differences (Open Drum)
  - `motor_stop()` for front and rear motors
  - If the absolute value of `current_Phase_Diff + 20` is less than or equal to `total_Phase_Diff / 2`, `current_Phase_Diff += 20` 
  - Rear motor `motor.incremental_position_control` with `+20` angle increment
  - Wait until the rotating speed is 0
  - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed,`, and torque is set to `rotate_Torque`   
- If "d" is pressed, the motor phase differences will turn to the negative differences (Close Drum)
  - `motor_stop()` for front and rear motors
  - If the absolute value of `current_Phase_Diff + 20` is less than or equal to `total_Phase_Diff / 2`, `current_Phase_Diff -= 20` 
  - Rear motor `motor.incremental_position_control` with `-20` angle increment
  - Wait until the rotating speed is 0
  - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque` 


- If "s" is pressed, the phase differences will be eliminated
  - `motor_stop()` for front and rear motors
  - Rear motor `motor.incremental_position_control` with `- current_Phase_Diff` angle increment
  - `current_Phase_Diff` is set to 0
  - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque` 
- If "z" is pressed, the motor will stop, and the phase differences will be eliminated
  - `motor_stop()` for front and rear motors
  - Rear motor `motor.incremental_position_control` with `- current_Phase_Diff` angle increment
  - `current_Phase_Diff` is set to 0
  - Global var `target_Speed` is set to 0 degrees/second
  - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque` 
- If "r" is pressed, the system will reset
  - Redo Position Initialization


## Notes

- The motor's GREEN LED status:
  - Solid Green: Motor is powered on and enabled.
  - Blinking Green: Motor is powered on but not enabled.
  - Off: Motor is powered off.

- When the motor encounter large torque, it will automatically disable itself due to lack of power (current or voltage). Make sure that the power supply can provide enough current and voltage for the motor. If the motor is disabled, you can re-enable it by rebooting the motor (turn off and turn on the power supply).

## Bugs

- 2025-09-19: The motor sometimes cannot be enabled when starting at first.
- 2025-09-19: Keyboard input "s" seems not working sometimes.