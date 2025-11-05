# sudo ip link set can0 up type can bitrate 1000000
# sudo ifconfig can0 up

import keyboard
from pylkmotor import LKMotor
import time
import math
from collections import deque

global target_Speed, speed_Max, speed_Min, total_Phase_Diff, current_Phase_Diff, phase_Diff_increment, init_Torque, rotate_Torque, gearBox_Ratio
target_Speed = 0 # in degree/s
speed_Max = 720 # in degree/s
speed_Min = 0 # in degree/s
total_Phase_Diff =  180*3 # in degree.
current_Phase_Diff = 0 # in degree.
phase_Diff_increment = 10 # in degree.
init_Torque = 50
rotate_Torque = 2000
gearBox_Ratio = 36
speed_samples = deque(maxlen=5)  # Adjust the maxlen for the desired window size

def end_degree_to_0_01_dps_LSB(angle):
    # Convert angle to 0.01 dps LSB

    return int(angle * gearBox_Ratio * 100)

def end_degree_to_0_1_dps_LSB(angle):
    # Convert angle to 0.1 dps LSB

    return int(angle * gearBox_Ratio * 10)

def end_degree_to_1_dps_LSB(angle):
    # Convert angle to 0.1 dps LSB

    return int(angle * gearBox_Ratio)

def create_key_press_callback(motor_Front, motor_Rear):
    """Factory function to create callback with motor references"""
    def on_key_press(event):
        global target_Speed, speed_Max, speed_Min, total_Phase_Diff, current_Phase_Diff, phase_Diff_increment, init_Torque, rotate_Torque, gearBox_Ratio
        """
        Callback function that is called whenever a key is pressed.
        """
        print(f"Key {event.name} was pressed")
        if event.name == 'w':  # Check if the pressed key is 'w'
            print("Increase speed")
            if target_Speed + 10 < speed_Max:
                target_Speed += 10
            else:
                target_Speed = speed_Max
            print(f"Target speed set to: {target_Speed} deg/s")
            motor_Front.speed_loop_control(iq_control=rotate_Torque, speed_control=end_degree_to_0_01_dps_LSB(target_Speed))
            motor_Rear.speed_loop_control(iq_control=rotate_Torque, speed_control=-end_degree_to_0_01_dps_LSB(target_Speed))

        elif event.name == 'x':  # Check if the pressed key is 'a'
            print("Decrease speed")
            if target_Speed - 10 > speed_Min:
                target_Speed -= 10
            else:
                target_Speed = speed_Min
            motor_Front.speed_loop_control(iq_control=rotate_Torque, speed_control=end_degree_to_0_01_dps_LSB(target_Speed))
            motor_Rear.speed_loop_control(iq_control=rotate_Torque, speed_control=-end_degree_to_0_01_dps_LSB(target_Speed))
            print(f"Target speed set to: {target_Speed} deg/s")

        elif event.name == 'a':  # Check if the pressed key is 'a'
            print("Increase Phase Diff")
            motor_Front.motor_stop()
            motor_Rear.motor_stop()
            if abs(current_Phase_Diff + phase_Diff_increment) < total_Phase_Diff/2:
                current_Phase_Diff += phase_Diff_increment
            else:
                current_Phase_Diff = total_Phase_Diff/2
            print(f"Phase Diff set to: {current_Phase_Diff} deg")
            motor_Rear.incremental_position_control(angle_increment=end_degree_to_0_01_dps_LSB(phase_Diff_increment), max_speed=end_degree_to_1_dps_LSB(90))
            time_cycle_out = 0
            while motor_Front.read_motor_status_2()[2] > 0.01 or motor_Rear.read_motor_status_2()[2] > 0.01:
                print(f"Speed Front: {motor_Front.read_motor_status_2()[2]} deg/s")
                print(f"Speed Rear: {motor_Rear.read_motor_status_2()[2]} deg/s")
                time.sleep(0.1)
                time_cycle_out += 1
                print(f"Time cycle out: {time_cycle_out}")
                if time_cycle_out == 50:
                    print("Wait Motor Stop Time Out!")
                    break
            motor_Front.speed_loop_control(iq_control=rotate_Torque, speed_control=end_degree_to_0_01_dps_LSB(target_Speed))
            motor_Rear.speed_loop_control(iq_control=rotate_Torque, speed_control=-end_degree_to_0_01_dps_LSB(target_Speed))

        elif event.name == 'd':  # Check if the pressed key is 'a'
            print("Decrease Phase Diff")
            motor_Front.motor_stop()
            motor_Rear.motor_stop()
            if abs(current_Phase_Diff + phase_Diff_increment) < total_Phase_Diff/2:
                current_Phase_Diff -= phase_Diff_increment
            else:
                current_Phase_Diff = -total_Phase_Diff/2
            print(f"Phase Diff set to: {current_Phase_Diff} deg")
            motor_Rear.incremental_position_control(angle_increment=end_degree_to_0_01_dps_LSB(-phase_Diff_increment), max_speed=end_degree_to_1_dps_LSB(90))
            time_cycle_out = 0
            while motor_Front.read_motor_status_2()[2] > 0.01 or motor_Rear.read_motor_status_2()[2] > 0.01:
                print(f"Speed Front: {motor_Front.read_motor_status_2()[2]} deg/s")
                print(f"Speed Rear: {motor_Rear.read_motor_status_2()[2]} deg/s")
                time.sleep(0.1)
                time_cycle_out += 1
                print(f"Time cycle out: {time_cycle_out}")
                if time_cycle_out == 50:
                    print("Wait Motor Stop Time Out!")
                    break
            motor_Front.speed_loop_control(iq_control=rotate_Torque, speed_control=end_degree_to_0_01_dps_LSB(target_Speed))
            motor_Rear.speed_loop_control(iq_control=rotate_Torque, speed_control=-end_degree_to_0_01_dps_LSB(target_Speed))

        elif event.name == 's':  # Check if the pressed key is 'a'
            print("Phase Diff set to 0")
            motor_Front.motor_stop()
            motor_Rear.motor_stop()

            motor_Rear.incremental_position_control(angle_increment=end_degree_to_0_01_dps_LSB(current_Phase_Diff), max_speed=end_degree_to_1_dps_LSB(90))
            time_cycle_out = 0
            while motor_Front.read_motor_status_2()[2] > 0.01 or motor_Rear.read_motor_status_2()[2] > 0.01:
                print(f"Speed Front: {motor_Front.read_motor_status_2()[2]} deg/s")
                print(f"Speed Rear: {motor_Rear.read_motor_status_2()[2]} deg/s")
                time.sleep(0.1)
                time_cycle_out += 1
                print(f"Time cycle out: {time_cycle_out}")
                if time_cycle_out == 50:
                    print("Wait Motor Stop Time Out!")
                    break
            current_Phase_Diff = 0

            motor_Front.speed_loop_control(iq_control=rotate_Torque, speed_control=end_degree_to_0_01_dps_LSB(target_Speed))
            motor_Rear.speed_loop_control(iq_control=rotate_Torque, speed_control=-end_degree_to_0_01_dps_LSB(target_Speed))

        elif event.name == 'z':  # Check if the pressed key is 'a'
            print("Phase Diff set to 0 and stop motors")
            motor_Front.motor_stop()
            motor_Rear.motor_stop()

            motor_Rear.incremental_position_control(angle_increment=end_degree_to_0_01_dps_LSB(current_Phase_Diff), max_speed=end_degree_to_1_dps_LSB(90))
            time_cycle_out = 0
            while motor_Front.read_motor_status_2()[2] > 0.01 or motor_Rear.read_motor_status_2()[2] > 0.01:
                print(f"Speed Front: {motor_Front.read_motor_status_2()[2]} deg/s")
                print(f"Speed Rear: {motor_Rear.read_motor_status_2()[2]} deg/s")
                time.sleep(0.1)
                time_cycle_out += 1
                print(f"Time cycle out: {time_cycle_out}")
                if time_cycle_out == 50:
                    print("Wait Motor Stop Time Out!")
                    break
            current_Phase_Diff = 0

            motor_Front.motor_stop()
            motor_Rear.motor_stop()

        elif event.name == 'r':  # Check if the pressed key is 'a'
            print("Redo Initialization")
            print("Start Fish Tail Position Initialization")
            motor_Front.torque_loop_control(iq_control=init_Torque)
            motor_Rear.torque_loop_control(iq_control=-init_Torque)

            # Wait for the motor to got stuck and stop
            print("Wait for the motor to got stuck and stop")
            time_cycle_out = 0
            while motor_get_speed(motor_Front) > 0.01 or motor_get_speed(motor_Rear) > 0.01 or time_cycle_out < 30:
                time.sleep(0.1)

            # Stop the motor
            motor_Front.motor_stop()
            motor_Rear.motor_stop()
            print("Motor Stopped")
            time.sleep(0.5)

            # Set the current position to 0
            motor_Front.set_position_to_angle(0)
            motor_Rear.set_position_to_angle(0)
            time.sleep(0.5)

            motor_Front.multi_turn_position_control(angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
            motor_Rear.multi_turn_position_control(angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
            time.sleep(0.5)

            motor_Rear.multi_turn_position_control(angle_control=end_degree_to_0_01_dps_LSB(total_Phase_Diff), max_speed=end_degree_to_1_dps_LSB(90))
            motor_Rear.set_position_to_angle(0)
            time.sleep(0.5)
            motor_Rear.multi_turn_position_control(angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
            time.sleep(0.5)
            print("Finished Position Initialization")
    return on_key_press

def on_key_release(event):
    """
    Callback function that is called whenever a key is released.
    """
    print(f"Key {event.name} was released")

def motor_status(motor):
    temperature, voltage, current, motor_state, error_state = motor.read_motor_status_1()
    temperature, iq, speed, encoder_val = motor.read_motor_status_2()
    temperature, current_A, current_B, current_C = motor.read_motor_status_3()
    multi_turn_angle = motor.read_multi_turn_angle()
    print(f"Temperature: {temperature} °C")
    print(f"Voltage: {voltage} V")
    print(f"Current: {current} A")
    print(f"Motor state: {motor_state}")
    print(f"Error state: {error_state}")
    print(f"Iq: {iq}")
    print(f"Speed: {speed} deg/s")
    print(f"Encoder value: {encoder_val}")
    return temperature, voltage, current, motor_state, error_state, iq, speed, encoder_val, current_A, current_B, current_C, multi_turn_angle

def motor_get_speed(motor):
    temperature, iq, speed, encoder_val = motor.read_motor_status_2()
    time.sleep(0.1)
    print(f"Speed: {speed} deg/s")
    return speed

def main():

    print("------------ Initialization ------------")
    print("Start Motor Initialization")
    motor_Front = LKMotor(bus_interface="socketcan", bus_channel="can0", motor_id=1)
    motor_Rear = LKMotor(bus_interface="socketcan", bus_channel="can0", motor_id=2)
    motor_Front.motor_shutdown()
    motor_Rear.motor_shutdown()
    motor_Front.motor_run()
    motor_Rear.motor_run()
    motor_status(motor_Front)
    motor_status(motor_Rear)
    print("Finished Motor Initialization")
    time.sleep(1)

    # Set the current position to 0
    print("Set the current position to 0")
    motor_Front.set_position_to_angle(0)
    time.sleep(2)
    motor_Rear.set_position_to_angle(0)
    time.sleep(2)
    print("set_position_to_angle 0 Finished")

    print("Start Multi Turn Position Control")
    motor_Front.multi_turn_position_control(angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
    time.sleep(2)
    motor_Rear.multi_turn_position_control(angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
    time.sleep(2)
    print("multi_turn_position_control Finished")

    print("Finished Position Initialization")

    print("------------ Start Keyboard Control ------------")
    # Create callback with motor references
    key_press_callback = create_key_press_callback(motor_Front, motor_Rear)
    
    # Hook into key press events
    keyboard.on_press(key_press_callback)
    
    print("Listening for keyboard input. Press 'Esc' to exit.")
    # Keep the program running until 'Esc' is pressed
    keyboard.wait('esc')
    print("Exiting...")

    print("------------ Return to Middle Position ------------")
    # Stop the motor
    motor_Front.motor_stop()
    motor_Rear.motor_stop()
    print("Motor Stopped")
    time.sleep(0.5)

    motor_Front.single_turn_position_control(spin_direction=0, angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
    motor_Rear.single_turn_position_control(spin_direction=0, angle_control=end_degree_to_0_01_dps_LSB(0), max_speed=end_degree_to_1_dps_LSB(90))
    
    time_cycle_out = 0
    while motor_Front.read_motor_status_2()[2] > 0.01 or motor_Rear.read_motor_status_2()[2] > 0.01:
        print(f"Speed Front: {motor_Front.read_motor_status_2()[2]} deg/s")
        print(f"Speed Rear: {motor_Rear.read_motor_status_2()[2]} deg/s")
        time.sleep(0.1)
        time_cycle_out += 1
        print(f"Time cycle out: {time_cycle_out}")
        if time_cycle_out == 100:
            print("Wait Motor Stop Time Out!")
            break

    print("------------ Motor and CAN Shutdown ------------")
    motor_Front.motor_stop()
    motor_Rear.motor_stop()

    motor_Front.motor_shutdown()
    motor_Rear.motor_shutdown()

    motor_Front.bus.shutdown()
    motor_Rear.bus.shutdown()

    print("------------ Thank you and Goodbye! ------------")

if __name__ == "__main__":
    main()