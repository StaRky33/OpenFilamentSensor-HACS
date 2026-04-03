"""Constants for the Open Filament Sensor integration."""

DOMAIN = "open_filament_sensor"
DEFAULT_SCAN_INTERVAL = 5  # seconds
CONF_DEVICE_NAME = "device_name"
CONF_CAMERA_ENTITY = "camera_entity"

API_ENDPOINT = "/sensor_status"

PRINT_STATUS_MAP = {
    0: "Idle",
    1: "Homing",
    2: "Descending",
    3: "Exposing",
    4: "Lifting",
    5: "Pausing",
    6: "Paused",
    7: "Stopping",
    8: "Stopped",
    9: "Complete",
    10: "File Checking",
    13: "Printing",
    16: "Heating",
    20: "Bed Leveling",
}

GRACE_STATE_MAP = {
    0: "Idle",
    1: "Start Grace",
    2: "Resume Grace",
    3: "Active",
    4: "Jammed",
}
