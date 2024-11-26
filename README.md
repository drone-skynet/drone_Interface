# drone_Interface
 드론 제어 명령 생성 인터페이스



# 드론 제어 명령 JSON 인터페이스 명세

드론 제어를 위한 JSON 명령 인터페이스의 규격을 설명합니다.

## 명령 목록

### 1. SET_MODE
- **설명**: 드론의 비행 모드를 설정합니다.
- **형식**:
  ```json
  {
    "command": "SET_MODE",
    "sys_id": <드론 ID>,
    "mode": <모드 이름>
  }
  ```
- **필드 설명**:
  - `command`: 항상 "SET_MODE"로 설정합니다.
  - `sys_id`: 제어할 드론의 ID (정수).
  - `mode`: 설정할 모드의 이름 ("AUTO" 또는 "BREAK").

### 2. destinations
- **설명**: 경유지들을 포함한 목적지 정보를 설정합니다.
- **형식**:
  ```json
  {
    "command": "destinations",
    "sys_id": <드론 ID>,
    "waypoints": [
      {
        "latitude": 37.123456,
        "longitude": 127.123456,
        "altitude": 20
      }
    ]
  }
  ```
- **필드 설명**:
  - `command`: 항상 "destinations"로 설정합니다.
  - `sys_id`: 제어할 드론의 ID (정수).
  - `waypoints`: 드론이 이동할 위치의 리스트 (배열).
    - 각 waypoint 객체는 다음 필드를 포함합니다:
      - `latitude`: 드론이 이동할 위치의 위도 (실수).
      - `longitude`: 드론이 이동할 위치의 경도 (실수).
      - `altitude`: 드론이 이동할 위치의 고도 (실수).

### 3. TAKEOFF
- **설명**: 드론을 이륙시킵니다.
- **형식**:
  ```json
  {
    "command": "TAKEOFF",
    "sys_id": <드론 ID>,
    "altitude": <이륙 고도>
  }
  ```
- **필드 설명**:
  - `command`: 항상 "TAKEOFF"로 설정합니다.
  - `sys_id`: 제어할 드론의 ID (정수).
  - `altitude`: 드론이 이륙할 고도 (기본값: 10).

### 4. MOVE_TO
- **설명**: 드론을 특정 위치로 이동시킵니다.
- **형식**:
  ```json
  {
    "command": "MOVE_TO",
    "sys_id": <드론 ID>
  }
  ```
- **필드 설명**:
  - `command`: 항상 "MOVE_TO"로 설정합니다.
  - `sys_id`: 제어할 드론의 ID (정수).

### 5. LAND
- **설명**: 드론을 착륙시킵니다.
- **형식**:
  ```json
  {
    "command": "LAND",
    "sys_id": <드론 ID>
  }
  ```
- **필드 설명**:
  - `command`: 항상 "LAND"로 설정합니다.
  - `sys_id`: 제어할 드론의 ID (정수).

### 6. ARM
- **설명**: 드론의 모터를 활성화합니다.
- **형식**:
  ```json
  {
    "command": "ARM",
    "sys_id": <드론 ID>
  }
  ```
- **필드 설명**:
  - `command`: 항상 "ARM"으로 설정합니다.
  - `sys_id`: 제어할 드론의 ID (정수).

## 예시 JSON 명령

1. **SET_MODE 예시**:
   ```json
   {
     "command": "SET_MODE",
     "sys_id": 1,
     "mode": "AUTO"
   }
   ```

2. **destinations 예시**:
   ```json
   {
     "command": "destinations",
     "sys_id": 1,
     "waypoints": [
       {
         "latitude": 37.123456,
         "longitude": 127.123456,
         "altitude": 20
       }
     ]
   }
   ```

3. **TAKEOFF 예시**:
   ```json
   {
     "command": "TAKEOFF",
     "sys_id": 1,
     "altitude": 20
   }
   ```

4. **MOVE_TO 예시**:
   ```json
   {
     "command": "MOVE_TO",
     "sys_id": 1
   }
   ```

5. **LAND 예시**:
   ```json
   {
     "command": "LAND",
     "sys_id": 1
   }
   ```

6. **ARM 예시**:
   ```json
   {
     "command": "ARM",
     "sys_id": 1
   }
   ```
```
