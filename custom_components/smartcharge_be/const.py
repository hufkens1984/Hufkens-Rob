"""Constants for SmartCharge BE."""

DOMAIN = "smartcharge_be"

PLATFORMS = ["sensor"]

P1_POWER_ENTITY = "sensor.p1_meter_vermogen"
SELECTED_CAR_ENTITY = "input_select.geselecteerde_auto"
MAX_GRID_POWER_ENTITY = "input_number.maximaal_netverbruik_laden"
MAX_CURRENT_OMODA_ENTITY = "input_number.max_laadstroom_omoda"
MAX_CURRENT_BYD_ENTITY = "input_number.max_laadstroom_byd"

CAR_OMODA = "Omoda 9"
CAR_BYD = "BYD Seal"