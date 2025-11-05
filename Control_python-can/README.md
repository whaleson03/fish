# Using Python and CAN bus to control the motors

## USB to CAN Module
In this implementation, we use the [LK TECH USB to CAN Module](https://item.taobao.com/item.htm?_u=j2m1kl5mb3e3&id=724178861547&pisk=gEfLsMDWMlq3oO5pSwyiZsK7AazgoRbF7M7jZ3xnFGIO2Z3hKLxkFQIVDLGuLBvJwGtGtHbHOU95qi6HA9xow_INvXckOgVJVZWazHYht4L5CMhlKwxhB4dFs9ckxkRRPiA8moV0iw7e_QZ0m5nP1tOXkeTIqL961QYRIwMnlw7ea3giV-X180HdXf3BP3a91ULmVQ9BFVM6bUYWRgtBCcTvuQO5VeMs1E8oRvtBVPn6yETIAbGSCCTDlDOWNg__WU-6RQOSwuwpPvtmwtiWKzIgWcZ821Lpp3hHXbezreJpSwKTcl5tgpKfRhh70J2kj3KNGl2O7iBCxFS8MldPbTsWyGi_qp75BGLdxonyq67hwHbLdk79wHd1Ot3SNNdpYKfpLDE9c671gC9gGrQ1_MbF6a07NFjDfw5BwSa29BtB6F5ubXtRCT1HLQoQmp75BGLpGgJlisKCQmxvrvaTWYkydFzmwnhoZWezTFK0urkrUdewWn4deYkyQsY9myBmUYJTe&spm=a1z09.2.0.0.6cbd2e8d9GRzOi) but other opensource USB to CAN module should work

## pyLKMotor: Control the LK motor with Python
PyLKMotor is a Python library to control the LK motor. It provides a simple interface to control the motor and read its status. The library supports:
- Link to repo: [pyLKMotor](https://github.com/han-xudong/pyLKMotor)

## Environment
For this implementation, we use the following environment:
- Ubuntu 22.04
- Python 3.12 (VENV) (see requirements.txt for required packages)

## USB to CAN Module
```
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 up
```

## Keyboard Fish Control: Control Flow
- Global Variables
  - `total_Phase_Diff` (degrees): A positive number that describes the total phase difference.
  - `current_Phase_Diff` (degrees)
  - `target_Speed` (degrees/second)
  - `init_Torque`
  - `rotate_Torque`
- Initiating CAN bus and motors
  - Initiating CAN bus for front motor (CAN ID:1)
  - Initiating CAN bus for Rear motor (CAN ID:2)
  - Set to `motor_run()` mode for font and rear motor
- Position Initialization
  - Two motors spin in the opposite direction in `motor.torque_loop_control`, torque is set to `init_Torque`
  - if the rotating speed is not 0, then wait until the rotating speed is 0
  - Set front and rear motor current multi-turn position to 0
  - Set front and rear motor target multi-turn position to 0
  - Rear motor rotates half of `total_Phase_Diff`
  - `phase_Diff` set to 0
  - `target_Speed` is set to 0 degrees/second， the front and rear motor is set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque` 


- Keyboard controlling

  - If "w" is pressed, the motor rotating speed will increase
    - Global var `target_Speed += 5` degrees/second
    - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque` 
  - If "x" is pressed, the motor rotating speed will decrease
    - Global var `target_Speed -= 5`  degrees/second
    - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed` and torque is set to `rotate_Torque`


  - If "a" is pressed, the motor phase differences will turn to the positive differences
    - `motor_stop()` for front and rear motors
    - If the absolute value of `current_Phase_Diff + 20` is less than or equal to `total_Phase_Diff / 2`, `current_Phase_Diff += 20` 
    - Rear motor `motor.incremental_position_control` with `+20` angle increment
    - Wait until the rotating speed is 0
    - The front and rear motors are set to `speed_loop_control` mode. Speed is set to `target_Speed,`, and torque is set to `rotate_Torque`   
  - If "d" is pressed, the motor phase differences will turn to the negative differences
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
 

- Shutting down
  - Two motors spin in the opposite direction in torque mode
  - if the rotating speed is not 0, then wait until the rotating speed is 0
  - Set front and rear motor current multi-turn position to 0
  - Set front and rear motor target multi-turn position to 0
  - Rear motor rotates half of `Total phase difference`
  - Set to `motor_shutdown()` mode for front and rear motor
  - Close CAN bus for front and rear motor

# Change LK Motor Package
To use the LK motor package, some changes are made to the original package. The changes are done on the LKMotor.py file. See LKMotor-change.py for the whole changed file.