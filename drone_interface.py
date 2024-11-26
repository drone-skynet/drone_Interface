# drone_interface.py

import paho.mqtt.client as mqtt
from pymavlink import mavutil
import json

# MQTT 브로커 정보
MQTT_BROKER = 'localhost'
def pub_topic(sys_id) :
    return f'/Mobius/SJ_Skynet/GCS_Data/TestDrone{251-int(sys_id)}/sitl'

SUB_TOPIC = '/Mobius/SJ_Skynet/Drone_Control/Commands'  # Mobius로부터 받을 토픽

# SUB_TOPIC = '/Mobius/SJ_Skynet/GCS_Data/TestDrone{251-int(sys_id)}/sitl'    

# MQTT 클라이언트 설정
client = mqtt.Client()

# MQTT 연결 콜백
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")

        client.subscribe(SUB_TOPIC)  # Mobius로부터 명령 수신
    else:
        print(f"Connection failed with code {rc}")

# MQTT 메시지를 수신할 때 호출되는 콜백
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')  # 수신한 메시지 디코딩
    print(f"Received message: {payload}")
    
    try:
        command_data = json.loads(payload)  # JSON 형식으로 파싱
        publish_control_command(command_data)  # 명령 발행
    except json.JSONDecodeError:
        print("Failed to decode JSON.")

# MQTT 메시지 발행 함수
def publish_control_command(command_data):
    command = command_data.get("command")
    sys_id = command_data.get("sys_id")
    
    mav_msg = None


    if command == "SET_MODE":
        mode = command_data.get("mode")
        if mode == "AUTO":
            custom_mode = 3  # AUTO 모드
            
        elif mode == "BREAK":
            custom_mode = 17  # BREAK 모드 (예시, 실제 값은 드론의 설정에 따라 다를 수 있음)
        else:
            print("Invalid mode specified.")
            return  # 잘못된 모드가 지정된 경우 함수 종료

        base_mode = mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED  # 커스텀 모드 플래그
        mav_msg = mavutil.mavlink.MAVLink_set_mode_message(
        target_system=sys_id,
        base_mode=base_mode,
        custom_mode=custom_mode
    )

    elif command == "destinations":
        destinations = command_data.get("destinations")  
        

    elif command == "TAKEOFF":
        altitude = command_data.get("altitude", 10)  # 기본 이륙 고도

        mav_msg = mavutil.mavlink.MAVLink_command_long_message(
            target_system=sys_id,
            target_component=0,  # 기본 컴포넌트 ID
            command=mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            confirmation=0,
            param1=0, param2=0, param3=0, param4=0,
            param5=0, param6=0,  # 위도/경도는 생략
            param7=altitude  # 목표 고도
        )
    
    elif command == "MOVE_TO":            
        # 웨이포인트에 대한 메시지 발행
        for waypoint in destinations:
            mav_msg = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
                0,  # time_boot_ms
                sys_id,
                0,  # 컴포넌트 ID (0은 기본)
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
                0b0000111111111000,  # type_mask (위치만 사용)
                int(waypoint['latitude'] * 1e7),  # 위도
                int(waypoint['longitude'] * 1e7),  # 경도
                waypoint['altitude'],  # 고도
                0, 0, 0,  # 속도 (not used)
                0, 0, 0,  # 가속도 (not used)
                0, 0  # yaw, yaw_rate (not used)
            )



    elif command == "LAND":
        mav_msg = mavutil.mavlink.MAVLink_command_long_message(
            target_system=sys_id,
            target_component=0,
            command=mavutil.mavlink.MAV_CMD_NAV_LAND,
            confirmation=0,
            param1=0, param2=0, param3=0, param4=0,
            param5=0, param6=0, param7=0
        )

    elif command == "ARM":
        mav_msg = mavutil.mavlink.MAVLink_command_long_message(
            target_system=sys_id,
            target_component=0,
            command=mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            confirmation=0,
            param1=1,  # ARM
            param2=0, param3=0, param4=0, param5=0, param6=0, param7=0
        )

    pub_topic1 = pub_topic(command_data.get("sys_id"))
    # 메시지 발행
    if mav_msg:
        mavlink_msg_bytes = mav_msg.pack(mavutil.mavlink.MAVLink('', 255, 190))
        client.publish(pub_topic1, mavlink_msg_bytes)
        print(f"Published MAVLink command: {mavlink_msg_bytes}")

# 메인 함수
def main():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER)
    client.loop_start()

    # MQTT 클라이언트 루프 유지
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
