import hid
import json
import time

VID = 0x0EB7
PID = 0x0005

BASELINE = [
    1, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33,
    0, 0, 128, 255, 255, 255, 255, 255, 255, 255, 255,
    255, 0, 1, 27, 0, 181, 2
]


def bit_changed(data, byte_idx, bit_idx):
    return bool((data[byte_idx] ^ BASELINE[byte_idx]) & (1 << bit_idx))


def rotary_l(data):
    states = [
        (6, 0), (6, 1), (6, 2), (6, 3),
        (6, 4), (6, 5), (6, 6), (6, 7),
        (7, 0), (7, 1), (7, 2), (7, 3),
    ]

    for idx, (byte_idx, bit_idx) in enumerate(states, start=1):
        if bit_changed(data, byte_idx, bit_idx):
            return idx

    return None


def rotary_r(data):
    states = [
        (7, 4), (7, 5), (7, 6), (7, 7),
        (8, 0), (8, 1), (8, 2), (8, 3),
        (8, 4), (8, 5), (8, 6), (8, 7),
    ]

    for idx, (byte_idx, bit_idx) in enumerate(states, start=1):
        if bit_changed(data, byte_idx, bit_idx):
            return idx

    return None


def get_state(data):
    state = {}

    state["button_01"] = bit_changed(data, 2, 3)
    state["button_02"] = bit_changed(data, 2, 2)
    state["button_03"] = bit_changed(data, 1, 7)
    state["button_04"] = bit_changed(data, 1, 6)
    state["button_05"] = bit_changed(data, 1, 4)
    state["button_06"] = bit_changed(data, 1, 5)
    state["button_07"] = bit_changed(data, 2, 4)
    state["button_08"] = bit_changed(data, 2, 5)
    state["button_09"] = bit_changed(data, 4, 0)
    state["button_10"] = bit_changed(data, 4, 6)
    state["button_11"] = bit_changed(data, 5, 7)
    state["button_12"] = bit_changed(data, 5, 6)
    state["button_13"] = bit_changed(data, 2, 1)
    state["button_14"] = bit_changed(data, 2, 0)

    dpad_base = bit_changed(data, 1, 3)
    dpad_right = bit_changed(data, 1, 1)
    dpad_down = bit_changed(data, 1, 2)

    state["button_15"] = dpad_base and not dpad_right and not dpad_down
    state["button_16"] = dpad_base and dpad_right and not dpad_down
    state["button_17"] = dpad_base and not dpad_right and dpad_down
    state["button_18"] = dpad_base and dpad_right and dpad_down
    state["button_19"] = bit_changed(data, 4, 1)

    state["button_20"] = bit_changed(data, 14, 7) # right scroll up
    state["button_21"] = bit_changed(data, 14, 6) # right scroll down
    state["button_22"] = bit_changed(data, 13, 3) # left scroll up
    state["button_23"] = bit_changed(data, 13, 2) # left scroll down
    state["button_24"] = bit_changed(data, 4, 7) # horn

    state["rotary_l"] = rotary_l(data)
    state["rotary_r"] = rotary_r(data)

    return state


devices = list(hid.enumerate(VID, PID))
if not devices:
    raise RuntimeError("Fanatec not found")

dev = hid.device()
dev.open_path(devices[0]["path"])
dev.set_nonblocking(True)

last_state = None

try:
    while True:
        data = dev.read(64)

        if data:
            state = get_state(data)

            if state != last_state:
                print(json.dumps(state, indent=2))
                last_state = state

        time.sleep(0.001)

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    dev.close()