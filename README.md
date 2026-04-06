# Open Filament Sensor — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

A Home Assistant integration for the [Open Filament Sensor](https://github.com/harpua555/OpenFilamentSensor) — an ESP32-based filament jam detector for resin 3D printers.

All sensors are grouped as a single **device** in Home Assistant. No manual `configuration.yaml` editing required.

---

## Features

- Auto-discovers all OFS sensors as a named HA device
- Supports multiple OFS devices (one per printer)
- Optional camera linking for snapshot notifications (works with [Elegoo Printers for Home Assistant](https://github.com/lookingforgroup/ha-elegoo-printer))
- Includes automation blueprints for jam and print complete notifications

---

## Installation

### Via HACS (recommended)

1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/StaRky33/ofs-hacs` as an **Integration**
3. Install "Open Filament Sensor"
4. Restart Home Assistant

### Manual

Copy `custom_components/open_filament_sensor/` into your HA `custom_components/` folder and restart.

---

## Setup

1. Go to **Settings → Integrations → Add Integration**
2. Search for **Open Filament Sensor**
3. Enter your device IP (e.g. `192.168.1.25`) and a friendly name (e.g. `Centauri Carbon`)
4. Optionally select a camera entity from your Elegoo integration for snapshot notifications
5. Done — all sensors appear under a single device entry

---

## Automation Blueprints

Two blueprints are included:

### Filament Jam Notification
Sends a push notification with a camera snapshot when a jam is detected.

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/StaRky33/OpenFilamentSensor-HACS/main/blueprints/ofs_notify_jam.yaml)

### Print Complete Notification
Sends a push notification with print duration and a camera snapshot when a print finishes.

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/StaRky33/OpenFilamentSensor-HACS/main/blueprints/ofs_notify_complete.yaml)

---

## Sensors

| Sensor | Description | Unit |
|--------|-------------|------|
| Printer Connected | WebSocket connection status | — |
| Is Printing | Whether a print is active | — |
| Print Status | Human-readable print status | — |
| Filament Stopped | Jam detected flag | — |
| Filament Runout | Runout detected flag | — |
| Hard Jam % | Hard jam confidence | % |
| Soft Jam % | Soft jam confidence | % |
| Grace Active | Grace period active | — |
| Grace State | Human-readable grace state | — |
| Expected Filament | Expected filament fed | mm |
| Actual Filament | Actual filament fed | mm |
| Expected Delta | Expected vs actual delta | mm |
| Current Deficit | Current filament deficit | mm |
| Progress | Print progress | % |
| Current Layer | Current print layer | — |
| Total Layers | Total print layers | — |
| Z Height | Current Z height | mm |
| Print Speed | Print speed | % |
| Expected Rate | Expected flow rate | mm/s |
| IP Address | Device IP | — |
| MAC Address | Device MAC | — |

---

## Requirements

- Home Assistant 2024.1.0 or newer
- OFS device running firmware with `/sensor_status` endpoint
- HACS installed

---

## License

MIT
