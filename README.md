# ControlAnyTVWithAlexa 📺🎙️

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Sinric Pro SDK](https://img.shields.io/badge/SinricPro-v6.0-orange)](https://sinric.pro)
[![Platform](https://img.shields.io/badge/platform-Android%20TV%20%7C%20Google%20TV-green)](https://android.com/tv/)

Turn **any Android TV or Google TV** into a native, full-featured **Smart TV in Amazon Alexa**—without Home Assistant, paid cloud hubs, or external dongles.

Control power, adjust exact volume levels, mute, launch streaming apps (Netflix, YouTube, Prime Video, Disney+ Hotstar, Spotify), and control playback with natural voice commands through any Amazon Echo speaker or the Alexa mobile app.

---

## ✨ Features

- **Single Unified TV Device:** Discovered natively as a real **TV** in Alexa (not messy separate on/off switches).
- **Exact Volume & Steps:** *"Alexa, set volume to 30 on TV"* or *"Alexa, volume up on TV"*.
- **Mute / Unmute:** *"Alexa, mute the TV"*.
- **Direct App Launching:** *"Alexa, change input to Netflix on TV"* or *"Alexa, open YouTube on TV"*.
- **HDMI Input Switching:** *"Alexa, switch to HDMI 1 on TV"*.
- **Media Controls:** *"Alexa, pause / resume / stop on TV"*.
- **Zero Cost & Free Forever:** Powered by Sinric Pro's free tier and Android ADB over Wi-Fi.
- **Ultra Lightweight:** Runs seamlessly on any computer, home server, or Raspberry Pi (Zero W, 3, 4, 5).

---

## 🛠️ Supported TVs

Works on any TV or streaming stick running **Android TV** or **Google TV** with Network ADB enabled:

| Brand / Platform | Compatibility |
| :--- | :---: |
| **Sony BRAVIA** (All Android TV / Google TV models) | ✅ Supported |
| **Xiaomi / Mi TV / Redmi** | ✅ Supported |
| **TCL** (Android TV / Google TV) | ✅ Supported |
| **Hisense** (Android TV / Google TV) | ✅ Supported |
| **OnePlus TV** | ✅ Supported |
| **Philips Android TV** | ✅ Supported |
| **Chromecast with Google TV** | ✅ Supported |
| **Nvidia Shield TV** | ✅ Supported |
| **Realme / Vu / Nokia TV** | ✅ Supported |

*(Note: Samsung Tizen and LG webOS do not run Android and are not supported by ADB).*

---

## 🗣️ Voice Commands Reference

| Action | Voice Command |
| :--- | :--- |
| **Power On** | *"Alexa, turn on the TV"* |
| **Power Off** | *"Alexa, turn off the TV"* |
| **Volume Level** | *"Alexa, set volume to 25 on TV"* (0 to 100) |
| **Volume Step** | *"Alexa, volume up on TV"* / *"Alexa, volume down on TV"* |
| **Mute / Unmute** | *"Alexa, mute TV"* / *"Alexa, unmute TV"* |
| **Launch Netflix** | *"Alexa, change input to Netflix on TV"* |
| **Launch YouTube** | *"Alexa, change input to YouTube on TV"* |
| **Launch Prime Video** | *"Alexa, change input to Prime Video on TV"* |
| **Launch Hotstar / Disney+** | *"Alexa, change input to Hotstar on TV"* |
| **Launch Spotify** | *"Alexa, change input to Spotify on TV"* |
| **HDMI Inputs** | *"Alexa, switch to HDMI 1 on TV"* |
| **Media Playback** | *"Alexa, pause on TV"* / *"Alexa, play on TV"* |

---

## 🚀 Quick Start Guide

### Step 1: Enable Network Debugging on your TV
1. On your TV remote, open **Settings** → **About** (or **Device Preferences** → **About**).
2. Scroll to **Build** and press the **OK / Select** button **7 times** until you see *"You are now a developer!"*.
3. Go back one screen and open **Developer options**.
4. Turn **USB debugging** (and **Network / ADB debugging** if shown) to **ON**.
5. Note your TV's local IP address from **Settings** → **Network & Internet** (e.g. `192.168.1.50`).

### Step 2: Create a free Sinric Pro TV Device
1. Sign up for a free account at **[portal.sinric.pro](https://portal.sinric.pro)**.
2. In the sidebar, click **Credentials**:
   - Copy your **App Key**
   - Copy your **App Secret**
3. In the sidebar, click **Devices** → **Add Device**:
   - Device Name: `TV`
   - Device Type: `TV`
   - Click **Save**, then copy the generated **Device ID**.

### Step 3: Link Sinric Pro in the Alexa App
1. Open the **Amazon Alexa** app on your phone.
2. Go to **More** → **Skills & Games** → search for **Sinric Pro**.
3. Tap **Enable to Use** and sign in with your Sinric Pro account.
4. Say: *"Alexa, discover devices"*. Alexa will discover your **TV**.

### Step 4: Install and Run the Bridge

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ControlAnyTVWithAlexa.git
cd ControlAnyTVWithAlexa

# Run setup script
chmod +x install.sh
./install.sh
```

Edit `config.json` with your credentials:

```json
{
  "sinric_app_key": "YOUR_SINRIC_APP_KEY",
  "sinric_app_secret": "YOUR_SINRIC_APP_SECRET",
  "sinric_device_id": "YOUR_SINRIC_DEVICE_ID",
  "tv_host": "192.168.1.50",
  "tv_port": 5555,
  "adb_path": "adb"
}
```

Start the bridge:
```bash
./venv/bin/python bridge.py
```

---

## ⚙️ Running as a Background Service (Linux / Raspberry Pi)

To keep the bridge running automatically on boot:

```bash
mkdir -p ~/.config/systemd/user
cp systemd/alexa-tv-bridge.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now alexa-tv-bridge.service
```

Check logs anytime:
```bash
journalctl --user -u alexa-tv-bridge.service -f
```

---

## 🏗️ Architecture

```
┌─────────────────┐             ┌────────────────────┐
│ Amazon Echo /   │   Cloud     │ Sinric Pro Cloud   │
│ Alexa App       │────────────▶│ (Smart Home Skill) │
└─────────────────┘             └─────────┬──────────┘
                                          │ WebSockets (TLS)
                                          ▼
                                ┌────────────────────┐
                                │ ControlAnyTVWithAlexa│
                                │ (bridge.py Daemon) │
                                └─────────┬──────────┘
                                          │ Local Wi-Fi (ADB)
                                          ▼
                                ┌────────────────────┐
                                │ Android TV /       │
                                │ Google TV          │
                                └────────────────────┘
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
