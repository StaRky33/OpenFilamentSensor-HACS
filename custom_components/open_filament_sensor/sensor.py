"""Sensor platform for Open Filament Sensor."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PRINT_STATUS_MAP, GRACE_STATE_MAP
from .coordinator import OFSDataCoordinator


@dataclass
class OFSSensorEntityDescription(SensorEntityDescription):
    """Describes an OFS sensor."""
    value_fn: Callable[[dict], Any] = None
    elegoo: bool = True  # whether the value is nested under data["elegoo"]


SENSOR_DESCRIPTIONS: tuple[OFSSensorEntityDescription, ...] = (
    OFSSensorEntityDescription(
        key="printer_connected",
        name="Printer Connected",
        icon="mdi:printer-3d",
        value_fn=lambda d: d.get("isWebsocketConnected"),
    ),
    OFSSensorEntityDescription(
        key="is_printing",
        name="Is Printing",
        icon="mdi:printer-3d-nozzle",
        value_fn=lambda d: d.get("isPrinting"),
    ),
    OFSSensorEntityDescription(
        key="print_status",
        name="Print Status",
        icon="mdi:information-outline",
        value_fn=lambda d: PRINT_STATUS_MAP.get(d.get("printStatus"), f"Unknown ({d.get('printStatus')})"),
    ),
    OFSSensorEntityDescription(
        key="filament_stopped",
        name="Filament Stopped",
        icon="mdi:alert",
        elegoo=False,
        value_fn=lambda d: d.get("stopped"),
    ),
    OFSSensorEntityDescription(
        key="filament_runout",
        name="Filament Runout",
        icon="mdi:alert-circle",
        elegoo=False,
        value_fn=lambda d: d.get("filamentRunout"),
    ),
    OFSSensorEntityDescription(
        key="hard_jam",
        name="Hard Jam",
        icon="mdi:alert-octagon",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("hardJamPercent", 0), 0),
    ),
    OFSSensorEntityDescription(
        key="soft_jam",
        name="Soft Jam",
        icon="mdi:alert-rhombus",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("softJamPercent", 0), 0),
    ),
    OFSSensorEntityDescription(
        key="grace_active",
        name="Grace Active",
        icon="mdi:timer-sand",
        value_fn=lambda d: d.get("graceActive"),
    ),
    OFSSensorEntityDescription(
        key="grace_state",
        name="Grace State",
        icon="mdi:timer-sand",
        value_fn=lambda d: GRACE_STATE_MAP.get(d.get("graceState"), f"Unknown ({d.get('graceState')})"),
    ),
    OFSSensorEntityDescription(
        key="expected_filament",
        name="Expected Filament",
        icon="mdi:ruler",
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("expectedFilament", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="actual_filament",
        name="Actual Filament",
        icon="mdi:ruler",
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("actualFilament", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="expected_delta",
        name="Expected Delta",
        icon="mdi:delta",
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("expectedDelta", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="current_deficit",
        name="Current Deficit",
        icon="mdi:arrow-collapse-down",
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("currentDeficitMm", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="deficit_threshold",
        name="Deficit Threshold",
        icon="mdi:arrow-collapse-down",
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        value_fn=lambda d: round(d.get("deficitThresholdMm", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="deficit_ratio",
        name="Deficit Ratio",
        icon="mdi:chart-line",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("deficitRatio", 0), 3),
    ),
    OFSSensorEntityDescription(
        key="pass_ratio",
        name="Pass Ratio",
        icon="mdi:chart-line",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("passRatio", 0), 3),
    ),
    OFSSensorEntityDescription(
        key="ratio_threshold",
        name="Ratio Threshold",
        icon="mdi:chart-line",
        value_fn=lambda d: round(d.get("ratioThreshold", 0), 3),
    ),
    OFSSensorEntityDescription(
        key="expected_rate",
        name="Expected Rate",
        icon="mdi:speedometer",
        native_unit_of_measurement="mm/s",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("expectedRateMmPerSec", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="movement_pulses",
        name="Movement Pulses",
        icon="mdi:pulse",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("movementPulses"),
    ),
    OFSSensorEntityDescription(
        key="telemetry_available",
        name="Telemetry Available",
        icon="mdi:antenna",
        value_fn=lambda d: d.get("telemetryAvailable"),
    ),
    OFSSensorEntityDescription(
        key="current_layer",
        name="Current Layer",
        icon="mdi:layers",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("currentLayer"),
    ),
    OFSSensorEntityDescription(
        key="total_layers",
        name="Total Layers",
        icon="mdi:layers-triple",
        value_fn=lambda d: d.get("totalLayer"),
    ),
    OFSSensorEntityDescription(
        key="progress",
        name="Progress",
        icon="mdi:progress-clock",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("progress"),
    ),
    OFSSensorEntityDescription(
        key="z_height",
        name="Z Height",
        icon="mdi:arrow-up-box",
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        device_class=SensorDeviceClass.DISTANCE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d.get("currentZ", 0), 2),
    ),
    OFSSensorEntityDescription(
        key="print_speed",
        name="Print Speed",
        icon="mdi:speedometer",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("PrintSpeedPct"),
    ),
    OFSSensorEntityDescription(
        key="current_ticks",
        name="Current Ticks",
        icon="mdi:counter",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("currentTicks"),
    ),
    OFSSensorEntityDescription(
        key="total_ticks",
        name="Total Ticks",
        icon="mdi:counter",
        value_fn=lambda d: d.get("totalTicks"),
    ),
    OFSSensorEntityDescription(
        key="ip_address",
        name="IP Address",
        icon="mdi:ip-network",
        elegoo=False,
        value_fn=lambda d: d.get("ip"),
    ),
    OFSSensorEntityDescription(
        key="mac_address",
        name="MAC Address",
        icon="mdi:ethernet",
        elegoo=False,
        value_fn=lambda d: d.get("mac"),
    ),
    OFSSensorEntityDescription(
        key="mainboard_id",
        name="Mainboard ID",
        icon="mdi:identifier",
        value_fn=lambda d: d.get("mainboardID"),
    ),
    OFSSensorEntityDescription(
        key="ui_refresh_interval",
        name="UI Refresh Interval",
        icon="mdi:refresh",
        native_unit_of_measurement="ms",
        value_fn=lambda d: d.get("uiRefreshIntervalMs"),
    ),
    OFSSensorEntityDescription(
        key="telemetry_stale_timeout",
        name="Telemetry Stale Timeout",
        icon="mdi:timer-off",
        native_unit_of_measurement="ms",
        value_fn=lambda d: d.get("flowTelemetryStaleMs"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up OFS sensors from a config entry."""
    coordinator: OFSDataCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OFSSensor(coordinator, description, entry)
        for description in SENSOR_DESCRIPTIONS
    )


class OFSSensor(CoordinatorEntity, SensorEntity):
    """Representation of a single OFS sensor."""

    def __init__(
        self,
        coordinator: OFSDataCoordinator,
        description: OFSSensorEntityDescription,
        entry,
    ) -> None:
        """Initialise the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = f"{entry.data['device_name']} {description.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.data["device_name"],
            manufacturer="Open Filament Sensor",
            model="OFS ESP32",
            configuration_url=f"http://{coordinator.host}",
        )

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        try:
            if self.entity_description.elegoo:
                data = self.coordinator.data.get("elegoo", {})
            else:
                data = self.coordinator.data
            return self.entity_description.value_fn(data)
        except Exception:
            return None
