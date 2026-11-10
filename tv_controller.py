#!/usr/bin/env python3
"""
tv_controller.py - Unified ADB TV Controller for Android TV & Google TV.
Supports Sony BRAVIA, TCL, Hisense, Xiaomi, OnePlus, Philips, Chromecast, Nvidia Shield, etc.
"""

import os
import re
import subprocess
import logging

logger = logging.getLogger("TVController")

# Key Android TV app package mappings
DEFAULT_APPS = {
    "netflix": "com.netflix.ninja",
    "youtube": "com.google.android.youtube.tv",
    "prime": "com.amazon.amazonvideo.livingroom",
    "amazon": "com.amazon.amazonvideo.livingroom",
    "prime video": "com.amazon.amazonvideo.livingroom",
    "hotstar": "in.startv.hotstar",
    "disney": "in.startv.hotstar",
    "disney+": "in.startv.hotstar",
    "spotify": "com.spotify.tv.android",
    "hulu": "com.hulu.livingroomplus",
    "apple": "com.apple.atve.androidtv.appletv",
    "apple tv": "com.apple.atve.androidtv.appletv",
    "hbo": "com.hbo.hbonow",
    "max": "com.wbd.stream",
    "plex": "com.plexapp.android",
    "kodi": "org.xbmc.kodi",
    "home": "com.gathin.tvhome"
}

class TVController:
    def __init__(self, host: str, port: int = 5555, adb_path: str = "adb"):
        self.host = host
        self.port = port
        self.adb_path = adb_path
        self.device_serial = f"{host}:{port}"
        self._ensure_connected()

    def _ensure_connected(self):
        try:
            # Check or trigger adb connect
            subprocess.run(
                [self.adb_path, "connect", self.device_serial],
                capture_output=True,
                text=True,
                timeout=5
            )
        except Exception as e:
            logger.warning(f"ADB connect warning: {e}")

    def shell(self, command: str) -> str:
        """Run a shell command on the TV via ADB."""
        try:
            res = subprocess.run(
                [self.adb_path, "-s", self.device_serial, "shell", command],
                capture_output=True,
                text=True,
                timeout=8
            )
            return res.stdout.strip()
        except Exception as e:
            logger.error(f"Error running ADB command '{command}': {e}")
            return ""

    # ==========================
    # Power Controls
    # ==========================
    def is_awake(self) -> bool:
        out = self.shell("dumpsys power | grep -i 'mWakefulness='")
        return "Awake" in out

    def power_on(self):
        logger.info("Powering on TV (Wakeup)")
        self.shell("input keyevent 224")

    def power_off(self):
        logger.info("Powering off TV (Sleep)")
        self.shell("input keyevent 223")

    # ==========================
    # Audio & Volume Controls
    # ==========================
    def get_volume(self) -> int:
        out = self.shell("media volume --stream 3 --get")
        m = re.search(r"volume is (\d+)", out)
        if m:
            return int(m.group(1))
        return 20

    def set_volume(self, volume: int):
        vol = max(0, min(100, volume))
        logger.info(f"Setting TV volume to {vol}")
        self.shell(f"media volume --show --stream 3 --set {vol}")

    def adjust_volume(self, delta: int):
        logger.info(f"Adjusting volume by {delta}")
        curr = self.get_volume()
        new_vol = max(0, min(100, curr + delta))
        self.set_volume(new_vol)

    def is_muted(self) -> bool:
        out = self.shell("media volume --stream 3 --get")
        return "muted" in out.lower()

    def set_mute(self, mute: bool):
        logger.info(f"Setting mute state: {mute}")
        self.shell("input keyevent 164")

    # ==========================
    # App & Input Launching
    # ==========================
    def launch_app(self, app_name: str) -> bool:
        norm = app_name.strip().lower()
        pkg = DEFAULT_APPS.get(norm)
        if not pkg:
            # Substring match
            for k, v in DEFAULT_APPS.items():
                if k in norm:
                    pkg = v
                    break

        if pkg:
            logger.info(f"Launching app '{pkg}' for request '{app_name}'")
            self.shell(f"monkey -p {pkg} -c android.intent.category.LEANBACK_LAUNCHER 1")
            return True
        else:
            logger.warning(f"Unknown app request: '{app_name}'")
            return False

    def select_input(self, input_name: str) -> bool:
        norm = input_name.strip().lower()
        if "hdmi" in norm:
            m = re.search(r"(\d+)", norm)
            port_num = m.group(1) if m else "1"
            logger.info(f"Switching to HDMI {port_num}")
            self.shell(f"cmd package resolve-activity -a android.intent.action.VIEW -d 'content://android.media.tv/passthrough/com.sony.dtv.tvinput.external%2F.ExternalTvInputService%2FHW{port_num}'")
            return True
        return self.launch_app(input_name)

    # ==========================
    # Media Playback Controls
    # ==========================
    def media_control(self, action: str):
        act = action.strip().lower()
        logger.info(f"Media control action: {act}")
        if "play" in act or "resume" in act:
            self.shell("input keyevent 126")
        elif "pause" in act:
            self.shell("input keyevent 127")
        elif "stop" in act:
            self.shell("input keyevent 86")
        elif "next" in act or "forward" in act:
            self.shell("input keyevent 87")
        elif "prev" in act or "rewind" in act:
            self.shell("input keyevent 88")
