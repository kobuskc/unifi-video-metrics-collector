CAMERA_VALID_RESPONSE = {
    "data": [
        {
            "name": "Demo Camera",
            "host": "123.123.123.123",
            "model": "UVC G3 Dome",
            "uptime": 1681208349266,
            "firmwareVersion": "v4.23.8",
            "systemInfo": {
                "cpuName": "ARMv7 Processor rev 1 (v7l)",
                "cpuLoad": 30,
                "memory": {"used": 57061376, "total": 358748160},
            },
            "mac": "A4BCD4AA9E12",
            "managed": True,
            "lastSeen": 1687410872750,
            "state": "CONNECTED",
            "lastRecordingId": "64d9a3e19008aa6cee0b20de",
            "lastRecordingStartTime": 1691984863143,
            "recordingSettings": {
                "motionRecordEnabled": True,
                "fullTimeRecordEnabled": False,
                "channel": "1",
                "prePaddingSecs": 0,
                "postPaddingSecs": 0,
                "storagePath": None,
            },
            "networkStatus": {
                "connectionState": 2,
                "connectionStateDescription": "CONNECTED",
                "linkSpeedMbps": 100,
                "ipAddress": "123.123.123.123",
            },
            "_id": "5d3e6f6ee4b028f8be5259de",
        }
    ],
    "meta": {"totalCount": 1, "filteredCount": 1},
}

CAMERA_BAD_RESPONSE = {
    "cam_data": [
        {
            "name": "Demo Camera",
            "host": "123.123.123.123",
            "model": "UVC G3 Dome",
            "uptime": 1681208349266,
            "firmwareVersion": "v4.23.8",
            "systemInfo": {
                "cpuName": "ARMv7 Processor rev 1 (v7l)",
                "cpuLoad": 30,
                "memory": {"used": 57061376, "total": 358748160},
            },
            "mac": "A4BCD4AA9E12",
            "managed": True,
            "lastSeen": 1687410872750,
            "state": "CONNECTED",
            "lastRecordingId": "64d9a3e19008aa6cee0b20de",
            "lastRecordingStartTime": 1691984863143,
            "recordingSettings": {
                "motionRecordEnabled": True,
                "fullTimeRecordEnabled": False,
                "channel": "1",
                "prePaddingSecs": 0,
                "postPaddingSecs": 0,
                "storagePath": None,
            },
            "networkStatus": {
                "connectionState": 2,
                "connectionStateDescription": "CONNECTED",
                "linkSpeedMbps": 100,
                "ipAddress": "123.123.123.123",
            },
            "_id": "5d3e6f6ee4b028f8be5259de",
        }
    ],
    "meta": {"totalCount": 1, "filteredCount": 1},
}

CAMERA_MISSING_KEY_RESPONSE = {
    "data": [
        {
            "name": "Demo Camera",
            "host": "123.123.123.123",
            "model": "UVC G3 Dome",
            "uptime": 1681208349266,
            "firmwareVersion": "v4.23.8",
            "_id": "5d3e6f6ee4b028f8be5259de",
        }
    ],
    "meta": {"totalCount": 1, "filteredCount": 1},
}

CAMERA_EMPTY_NAME_RESPONSE = {
    "data": [
        {
            "name": None,
            "host": "123.123.123.123",
            "model": "UVC G3 Dome",
            "firmwareVersion": "v4.23.8",
            "systemInfo": {
                "cpuName": "ARMv7 Processor rev 1 (v7l)",
                "cpuLoad": 30,
                "memory": {"used": 57061376, "total": 358748160},
            },
            "mac": "A4BCD4AA9E12",
            "managed": True,
            "lastSeen": 1687410872750,
            "state": "CONNECTED",
            "lastRecordingStartTime": 1691984863143,
        }
    ],
    "meta": {"totalCount": 1, "filteredCount": 1},
}

CAMERA_EMPTY_HOST_RESPONSE = {
    "data": [
        {
            "name": "Demo Camera",
            "host": None,
            "model": "UVC G3 Dome",
            "firmwareVersion": "v4.23.8",
            "systemInfo": {
                "cpuName": "ARMv7 Processor rev 1 (v7l)",
                "cpuLoad": 30,
                "memory": {"used": 57061376, "total": 358748160},
            },
            "mac": "A4BCD4AA9E12",
            "managed": True,
            "lastSeen": 1687410872750,
            "state": "CONNECTED",
            "lastRecordingStartTime": 1691984863143,
        }
    ],
    "meta": {"totalCount": 1, "filteredCount": 1},
}

MOCK_METRICS = {
    "g_name": [({"name": "Demo Camera"},), 1],
    "g_model": [({"name": "Demo Camera"},), {"camera_model": "UVC G3 Dome"}],
    "g_cpu_load": [({"name": "Demo Camera"},), 30],
    "g_memory_used": [({"name": "Demo Camera"},), 57061376],
    "g_memory_total": [({"name": "Demo Camera"},), 358748160],
    "g_host": [({"name": "Demo Camera"},), {"camera_host": "123.123.123.123"}],
    "g_mac": [({"name": "Demo Camera"},), {"camera_mac": "A4BCD4AA9E12"}],
    "g_firmware_version": [({"name": "Demo Camera"},), {"camera_firmware_version": "v4.23.8"}],
    "g_managed": [({"name": "Demo Camera"},), 1],
    "g_last_seen": [({"name": "Demo Camera"},), 1687410872750],
    "g_state": [({"name": "Demo Camera", "state": "CONNECTED"},), 1],
    "g_last_recording_start_time": [({"name": "Demo Camera"},), 1691984863143],
}

MOCK_TOML_DATA_DEV = {
    "Dev": {
        "api_host": "localhost",
        "api_port": 8080,
        "api_key": "test_key",
        "http_port": 9090,
        "refresh_rate": 60,
        "push": True,
        "gateway": "gateway_host",
        "gateway_port": 7070,
        "job": "test_job",
    }
}

MOCK_TOML_DATA_PROD = {
    "Prod": {
        "api_host": "mock.production.host",
        "api_port": 8080,
        "api_key": "test_key",
        "http_port": 9090,
        "refresh_rate": 60,
        "push": True,
        "gateway": "gateway_host",
        "gateway_port": 7070,
        "job": "test_job",
    }
}

MOCK_TOML_DATA_MISSING_KEYS = {
    "Prod": {
        "api_host": "mock.production.host",
        "api_port": 8080,
        "api_key": "test_key",
        "http_port": 9090,
        "refresh_rate": 60,
        "gateway_port": 7070,
        "job": "test_job",
    }
}
