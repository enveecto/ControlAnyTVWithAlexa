#!/usr/bin/env python3
"""
bridge.py - Sinric Pro to Android TV Alexa Smart Home Bridge.
Exposes a single unified TV device to Amazon Alexa with Volume, Mute, Power, and App controls.
"""

import asyncio
import json
import logging
import os
import sys
from sinricpro import SinricPro, SinricProConfig, SinricProTV
from tv_controller import TVController

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s"
)
logger = logging.getLogger("AlexaTVBridge")

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"Missing config.json! Please copy config.example.json to config.json and fill in your details.")
        sys.exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

cfg = load_config()

APP_KEY = cfg.get("sinric_app_key")
APP_SECRET = cfg.get("sinric_app_secret")
DEVICE_ID = cfg.get("sinric_device_id")
TV_HOST = cfg.get("tv_host", "192.168.1.6")
TV_PORT = cfg.get("tv_port", 5555)
ADB_PATH = cfg.get("adb_path", "adb")

if not APP_KEY or "YOUR_" in APP_KEY:
    logger.error("Invalid Sinric Pro credentials in config.json. Please update with your real keys.")
    sys.exit(1)

# Initialize Controller
tv_ctrl = TVController(host=TV_HOST, port=TV_PORT, adb_path=ADB_PATH)

# Initialize Sinric Pro SDK
config = SinricProConfig(app_key=APP_KEY, app_secret=APP_SECRET)
sinric = SinricPro.get_instance()
sinric.config = config

tv_device = SinricProTV(device_id=DEVICE_ID)

@tv_device.on_power_state
async def on_power_state(state: bool) -> bool:
    logger.info(f"Power command received: {'ON' if state else 'OFF'}")
    if state:
        tv_ctrl.power_on()
    else:
        tv_ctrl.power_off()
    return True

@tv_device.on_volume
async def on_volume(volume: int) -> bool:
    logger.info(f"Set volume command received: {volume}")
    tv_ctrl.set_volume(volume)
    return True

@tv_device.on_adjust_volume
async def on_adjust_volume(volume_delta: int) -> bool:
    logger.info(f"Adjust volume command received: {volume_delta}")
    tv_ctrl.adjust_volume(volume_delta)
    return True

@tv_device.on_mute
async def on_mute(mute: bool) -> bool:
    logger.info(f"Mute command received: {mute}")
    tv_ctrl.set_mute(mute)
    return True

@tv_device.on_select_input
async def on_select_input(input_name: str) -> bool:
    logger.info(f"Select input / app command received: '{input_name}'")
    tv_ctrl.select_input(input_name)
    return True

@tv_device.on_media_control
async def on_media_control(action) -> bool:
    logger.info(f"Media control command received: {action}")
    tv_ctrl.media_control(str(action))
    return True

sinric.add(tv_device)

async def main():
    logger.info(f"Connecting to Sinric Pro for device {DEVICE_ID} (Target TV: {TV_HOST}:{TV_PORT})...")
    await sinric.begin(config)
    logger.info("Bridge is successfully running and listening for Alexa voice commands!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down bridge...")
