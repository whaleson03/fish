# To setup the USB-CAN adapter, run the following commands:
# sudo ip link set can0 up type can bitrate 1000000
# sudo ifconfig can0 up

from pylkmotor import LKMotor
import time

motor1 = LKMotor(bus_interface="socketcan", bus_channel="can0", motor_id=1, bitrate=1000000)
motor2 = LKMotor(bus_interface="socketcan", bus_channel="can0", motor_id=2, bitrate=1000000)

print("------------ Motor Run ------------")
motor1.motor_run()
time.sleep(1)
motor2.motor_run()
time.sleep(1)

# print("------------ read_motor_status_1 ------------")
# temperature, voltage, current, motor_state, error_state = motor.read_motor_status_1()
# print(f"Temperature: {temperature} °C")
# print(f"Voltage: {voltage} V")
# print(f"Current: {current} A")
# print(f"Motor state: {motor_state}")
# print(f"Error state: {error_state}")

# print("------------ read_motor_status_2 ------------")
# temperature, iq, speed, encoder_val = motor.read_motor_status_2()
# print(f"Temperature: {temperature} °C")
# print(f"Iq: {iq}")
# print(f"Speed: {speed} deg/s")
# print(f"Encoder value: {encoder_val}")

# print("------------ read_motor_status_3 ------------")
# temperature, current_A, current_B, current_C = motor.read_motor_status_3()
# print(f"Motor temperature: {temperature} °C")
# print(f"Current A: {current_A} A")
# print(f"Current B: {current_B} A")
# print(f"Current C: {current_C} A")

# print("------------ read_encoder_data ------------")
# encoder_val, encoder_raw, encoder_offset = motor.read_encoder_data()
# print(f"Encoder value: {encoder_val}")
# print(f"Encoder raw value: {encoder_raw}")
# print(f"Encoder offset: {encoder_offset}")

# print("------------ Speed loop control ------------")
# motor.speed_loop_control(iq_control=1000, speed_control=5000*100)
# time.sleep(5)
# motor.speed_loop_control(iq_control=1000, speed_control=-5000*100)
# time.sleep(5)

motor1.torque_loop_control(iq_control=50)
motor2.torque_loop_control(iq_control=50)

while True:
    # print("------------ read_motor_status_1 ------------")
    # temperature, voltage, current, motor_state, error_state = motor.read_motor_status_1()
    # print(f"Temperature: {temperature} °C")
    # print(f"Voltage: {voltage} V")
    # print(f"Current: {current} A")
    # print(f"Motor state: {motor_state}")
    # print(f"Error state: {error_state}")

    # print("------------ read_motor_status_2 ------------")
    # temperature, iq, speed, encoder_val = motor.read_motor_status_2()
    # print(f"Temperature: {temperature} °C")
    # print(f"Iq: {iq}")
    # print(f"Speed: {speed} deg/s")
    # print(f"Encoder value: {encoder_val}")

    # print("------------ read_motor_status_3 ------------")
    # temperature, current_A, current_B, current_C = motor.read_motor_status_3()
    # print(f"Motor temperature: {temperature} °C")
    # print(f"Current A: {current_A} A")
    # print(f"Current B: {current_B} A")
    # print(f"Current C: {current_C} A")
    
    
    # speed1 = motor1.read_motor_status_2()[2]
    # print(f"Speed1: {speed1} deg/s")
    # time.sleep(5)
    # speed2 = motor2.read_motor_status_2()[2]
    # print(f"Speed2: {speed2} deg/s")
    # time.sleep(5)
    
    # 增加请求间隔
    status1 = motor1.read_motor_status_2()
    print(f"Motor 1: {status1}")
    time.sleep(0.1)  # 关键间隔
    
    status2 = motor2.read_motor_status_2()
    print(f"Motor 2: {status2}")
    time.sleep(5)


print("------------ Motor and CAN Shutdown ------------")
motor.motor_stop()
motor.motor_shutdown()
motor.bus.shutdown()