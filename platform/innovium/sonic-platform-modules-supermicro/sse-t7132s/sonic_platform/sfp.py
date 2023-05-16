
#!/usr/bin/env python

#############################################################################
# SuperMicro SSE-T7132S
#
# Sfp contains an implementation of SONiC Platform Base API and
# provides the sfp status which are available in the platform
#
#############################################################################

import time
import struct
import syslog

try:
    from sonic_platform_base.sfp_base import SfpBase
    from sonic_platform_base.sonic_sfp.sff8472 import sff8472InterfaceId
    from sonic_platform_base.sonic_sfp.sff8472 import sff8472Dom
    from sonic_platform_base.sonic_sfp.sff8436 import sff8436InterfaceId
    from sonic_platform_base.sonic_sfp.sff8436 import sff8436Dom
    from sonic_platform_base.sonic_sfp.inf8628 import inf8628InterfaceId
    from sonic_platform_base.sonic_sfp.qsfp_dd import qsfp_dd_InterfaceId
    from sonic_platform_base.sonic_sfp.qsfp_dd import qsfp_dd_Dom
    from sonic_platform_base.sonic_sfp.sff8024 import type_of_media_interface
    from sonic_platform_base.sonic_sfp.sfputilhelper import SfpUtilHelper
    from .helper import APIHelper
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

from sonic_py_common import logger
import inspect

# definitions of the offset and width for values in XCVR info eeprom
XCVR_INTFACE_BULK_OFFSET = 0
XCVR_INTFACE_BULK_WIDTH_QSFP = 20
XCVR_INTFACE_BULK_WIDTH_SFP = 21
XCVR_TYPE_OFFSET = 0
XCVR_TYPE_WIDTH = 1
XCVR_EXT_TYPE_OFFSET = 1
XCVR_EXT_TYPE_WIDTH = 1
XCVR_CONNECTOR_OFFSET = 2
XCVR_CONNECTOR_WIDTH = 1
XCVR_COMPLIANCE_CODE_OFFSET = 3
XCVR_COMPLIANCE_CODE_WIDTH = 8
XCVR_ENCODING_OFFSET = 11
XCVR_ENCODING_WIDTH = 1
XCVR_NBR_OFFSET = 12
XCVR_NBR_WIDTH = 1
XCVR_EXT_RATE_SEL_OFFSET = 13
XCVR_EXT_RATE_SEL_WIDTH = 1
XCVR_CABLE_LENGTH_OFFSET = 14
XCVR_CABLE_LENGTH_WIDTH_QSFP = 5
XCVR_CABLE_LENGTH_WIDTH_SFP = 6
XCVR_VENDOR_NAME_OFFSET = 20
XCVR_VENDOR_NAME_WIDTH = 16
XCVR_VENDOR_OUI_OFFSET = 37
XCVR_VENDOR_OUI_WIDTH = 3
XCVR_VENDOR_PN_OFFSET = 40
XCVR_VENDOR_PN_WIDTH = 16
XCVR_HW_REV_OFFSET = 56
XCVR_HW_REV_WIDTH_OSFP = 2
XCVR_HW_REV_WIDTH_QSFP = 2
XCVR_HW_REV_WIDTH_SFP = 4
XCVR_EXT_SPECIFICATION_COMPLIANCE_OFFSET = 64
XCVR_EXT_SPECIFICATION_COMPLIANCE_WIDTH = 1
XCVR_VENDOR_SN_OFFSET = 68
XCVR_VENDOR_SN_WIDTH = 16
XCVR_VENDOR_DATE_OFFSET = 84
XCVR_VENDOR_DATE_WIDTH = 8
XCVR_DOM_CAPABILITY_OFFSET = 92
XCVR_DOM_CAPABILITY_WIDTH = 2

XCVR_INTERFACE_DATA_START = 0
XCVR_INTERFACE_DATA_SIZE = 92

QSFP_DOM_BULK_DATA_START = 22
QSFP_DOM_BULK_DATA_SIZE = 36
SFP_DOM_BULK_DATA_START = 96
SFP_DOM_BULK_DATA_SIZE = 10
QSFP_DD_DOM_BULK_DATA_START = 14
QSFP_DD_DOM_BULK_DATA_SIZE = 4

# definitions of the offset for values in OSFP info eeprom
OSFP_TYPE_OFFSET = 0
OSFP_VENDOR_NAME_OFFSET = 129
OSFP_VENDOR_PN_OFFSET = 148
OSFP_HW_REV_OFFSET = 164
OSFP_VENDOR_SN_OFFSET = 166

# definitions of the offset for values in QSFP_DD info eeprom
QSFP_DD_TYPE_OFFSET = 0
QSFP_DD_VENDOR_NAME_OFFSET = 1
QSFP_DD_VENDOR_PN_OFFSET = 20
QSFP_DD_VENDOR_SN_OFFSET = 38
QSFP_DD_VENDOR_OUI_OFFSET = 17

# definitions of the offset and width for values in XCVR_QSFP_DD info eeprom
XCVR_EXT_TYPE_OFFSET_QSFP_DD = 72
XCVR_EXT_TYPE_WIDTH_QSFP_DD = 2
XCVR_CONNECTOR_OFFSET_QSFP_DD = 75
XCVR_CONNECTOR_WIDTH_QSFP_DD = 1
XCVR_CABLE_LENGTH_OFFSET_QSFP_DD = 74
XCVR_CABLE_LENGTH_WIDTH_QSFP_DD = 1
XCVR_HW_REV_OFFSET_QSFP_DD = 36
XCVR_HW_REV_WIDTH_QSFP_DD = 2
XCVR_VENDOR_DATE_OFFSET_QSFP_DD = 54
XCVR_VENDOR_DATE_WIDTH_QSFP_DD = 8
XCVR_DOM_CAPABILITY_OFFSET_QSFP_DD = 2
XCVR_DOM_CAPABILITY_WIDTH_QSFP_DD = 1
XCVR_MEDIA_TYPE_OFFSET_QSFP_DD = 85
XCVR_MEDIA_TYPE_WIDTH_QSFP_DD = 1
XCVR_FIRST_APPLICATION_LIST_OFFSET_QSFP_DD = 86
XCVR_FIRST_APPLICATION_LIST_WIDTH_QSFP_DD = 32
XCVR_SECOND_APPLICATION_LIST_OFFSET_QSFP_DD = 351
XCVR_SECOND_APPLICATION_LIST_WIDTH_QSFP_DD = 28

# Offset for values in QSFP eeprom
QSFP_DOM_REV_OFFSET = 1
QSFP_DOM_REV_WIDTH = 1
QSFP_TEMPE_OFFSET = 22
QSFP_TEMPE_WIDTH = 2
QSFP_VOLT_OFFSET = 26
QSFP_VOLT_WIDTH = 2
QSFP_VERSION_COMPLIANCE_OFFSET = 1
QSFP_VERSION_COMPLIANCE_WIDTH = 2
QSFP_CHANNL_MON_OFFSET = 34
QSFP_CHANNL_MON_WIDTH = 16
QSFP_CHANNL_MON_WITH_TX_POWER_WIDTH = 24
QSFP_CHANNL_DISABLE_STATUS_OFFSET = 86
QSFP_CHANNL_DISABLE_STATUS_WIDTH = 1
QSFP_CHANNL_RX_LOS_STATUS_OFFSET = 3
QSFP_CHANNL_RX_LOS_STATUS_WIDTH = 1
QSFP_CHANNL_TX_FAULT_STATUS_OFFSET = 4
QSFP_CHANNL_TX_FAULT_STATUS_WIDTH = 1
QSFP_CONTROL_OFFSET = 86
QSFP_CONTROL_WIDTH = 8
QSFP_MODULE_MONITOR_OFFSET = 0
QSFP_MODULE_MONITOR_WIDTH = 9
QSFP_POWEROVERRIDE_OFFSET = 93
QSFP_POWEROVERRIDE_WIDTH = 1
QSFP_POWEROVERRIDE_BIT = 0
QSFP_POWERSET_BIT = 1
QSFP_OPTION_VALUE_OFFSET = 192
QSFP_OPTION_VALUE_WIDTH = 4
QSFP_MODULE_UPPER_PAGE3_START = 384
QSFP_MODULE_THRESHOLD_OFFSET = 128
QSFP_MODULE_THRESHOLD_WIDTH = 24
QSFP_CHANNL_THRESHOLD_OFFSET = 176
QSFP_CHANNL_THRESHOLD_WIDTH = 24

SFP_MODULE_ADDRA2_OFFSET = 256
SFP_MODULE_THRESHOLD_OFFSET = 0
SFP_MODULE_THRESHOLD_WIDTH = 56
SFP_CHANNL_THRESHOLD_OFFSET = 112
SFP_CHANNL_THRESHOLD_WIDTH = 2

SFP_TEMPE_OFFSET = 96
SFP_TEMPE_WIDTH = 2
SFP_VOLT_OFFSET = 98
SFP_VOLT_WIDTH = 2
SFP_CHANNL_MON_OFFSET = 100
SFP_CHANNL_MON_WIDTH = 6
SFP_CHANNL_STATUS_OFFSET = 110
SFP_CHANNL_STATUS_WIDTH = 1

QSFP_DD_TEMPE_OFFSET = 14
QSFP_DD_TEMPE_WIDTH = 2
QSFP_DD_VOLT_OFFSET = 16
QSFP_DD_VOLT_WIDTH = 2
QSFP_DD_TX_BIAS_OFFSET = 42
QSFP_DD_TX_BIAS_WIDTH = 16
QSFP_DD_RX_POWER_PAGE = 0x11
QSFP_DD_RX_POWER_OFFSET = 186
QSFP_DD_RX_POWER_WIDTH = 16
QSFP_DD_TX_POWER_PAGE = 0x11
QSFP_DD_TX_POWER_OFFSET = 154
QSFP_DD_TX_POWER_WIDTH = 16
QSFP_DD_CHANNL_MON_PAGE = 0x11
QSFP_DD_CHANNL_MON_OFFSET = 154
QSFP_DD_CHANNL_MON_WIDTH = 48
QSFP_DD_CHANNL_DISABLE_STATUS_OFFSET = 86
QSFP_DD_CHANNL_DISABLE_STATUS_WIDTH = 1
QSFP_DD_CHANNL_TX_FAULT_STATUS_OFFSET = 7
QSFP_DD_CHANNL_TX_FAULT_STATUS_WIDTH = 1
QSFP_DD_MODULE_THRESHOLD_OFFSET = 0
QSFP_DD_MODULE_THRESHOLD_WIDTH = 72
QSFP_DD_CHANNL_STATUS_OFFSET = 26
QSFP_DD_CHANNL_STATUS_WIDTH = 1
QSFP_DD_TX_DISABLE_PAGE = 0x10
QSFP_DD_TX_DISABLE_OFFSET = 130
QSFP_DD_TX_DISABLE_WIDTH = 1
QSFP_DD_LANE_MON_ADVT_PAGE = 0x01
QSFP_DD_LANE_MON_ADVT_OFFSET = 160
QSFP_DD_LANE_MON_ADVT_WIDTH = 1
QSFP_DD_RX_FLAGS_ADVT_PAGE = 0x01
QSFP_DD_RX_FLAGS_ADVT_OFFSET = 158
QSFP_DD_RX_FLAGS_ADVT_WIDTH = 1
QSFP_DD_RX_LOS_PAGE = 0x11
QSFP_DD_RX_LOS_OFFSET = 147
QSFP_DD_RX_LOS_WIDTH = 1
QSFP_DD_TX_FLAGS_ADVT_PAGE = 0x01
QSFP_DD_TX_FLAGS_ADVT_OFFSET = 157
QSFP_DD_TX_FLAGS_ADVT_WIDTH = 1
QSFP_DD_TX_FAULT_PAGE = 0x11
QSFP_DD_TX_FAULT_OFFSET = 135
QSFP_DD_TX_FAULT_WIDTH = 1
QSFP_DD_CTRLS_ADVT_PAGE = 0x01
QSFP_DD_CTRLS_ADVT_OFFSET = 155
QSFP_DD_CTRLS_ADVT_WIDTH = 1


sfp_cable_length_tup = (
    'LengthSMFkm-UnitsOfKm', 'LengthSMF(UnitsOf100m)',
    'Length50um(UnitsOf10m)', 'Length62.5um(UnitsOfm)',
    'LengthCable(UnitsOfm)', 'LengthOM3(UnitsOf10m)'
)

sfp_compliance_code_tup = (
    '10GEthernetComplianceCode', 'InfinibandComplianceCode',
    'ESCONComplianceCodes', 'SONETComplianceCodes',
    'EthernetComplianceCodes', 'FibreChannelLinkLength',
    'FibreChannelTechnology', 'SFP+CableTechnology',
    'FibreChannelTransmissionMedia', 'FibreChannelSpeed'
)

qsfp_compliance_code_tup = (
    '10/40G Ethernet Compliance Code', 'SONET Compliance codes',
    'SAS/SATA compliance codes', 'Gigabit Ethernet Compliant codes',
    'Fibre Channel link length/Transmitter Technology',
    'Fibre Channel transmission media', 'Fibre Channel Speed'
)

qsfp_dd_dom_capability_tup = ('Tx_bias_support', 'Tx_power_support', 'Rx_power_support',
                              'Voltage_support', 'Temp_support')
qsfp_dom_capability_tup = ('Tx_power_support', 'Rx_power_support',
                           'Voltage_support', 'Temp_support')
# Add an EOL to prevent this being viewed as string instead of list
sfp_dom_capability_tup = ('sff8472_dom_support', 'EOL')

info_dict_keys = [
    'type', 'hardware_rev', 'serial', 'manufacturer',
    'model', 'connector', 'encoding', 'ext_identifier',
    'ext_rateselect_compliance', 'cable_type', 'cable_length',
    'nominal_bit_rate', 'specification_compliance', 'vendor_date',
    'vendor_oui', 'application_advertisement', 'type_abbrv_name'
]

qsfp_cable_length_tup = ('Length(km)', 'Length OM3(2m)',
                         'Length OM2(m)', 'Length OM1(m)',
                         'Length Cable Assembly(m)')

dom_info_dict_keys = [
    'rx_los', 'tx_fault', 'reset_status', 'lp_mode',
    'tx_disable', 'tx_disabled_channel', 'temperature', 'voltage',
    'rx1power', 'rx2power', 'rx3power', 'rx4power',
    'rx5power', 'rx6power', 'rx7power', 'rx8power',
    'tx1bias', 'tx2bias', 'tx3bias', 'tx4bias',
    'tx5bias', 'tx6bias', 'tx7bias', 'tx8bias',
    'tx1power', 'tx2power', 'tx3power', 'tx4power',
    'tx5power', 'tx6power', 'tx7power', 'tx8power']

threshold_dict_keys = [
    'temphighalarm', 'temphighwarning',
    'templowalarm', 'templowwarning',
    'vcchighalarm', 'vcchighwarning',
    'vcclowalarm', 'vcclowwarning',
    'rxpowerhighalarm', 'rxpowerhighwarning',
    'rxpowerlowalarm', 'rxpowerlowwarning',
    'txpowerhighalarm', 'txpowerhighwarning',
    'txpowerlowalarm', 'txpowerlowwarning',
    'txbiashighalarm', 'txbiashighwarning',
    'txbiaslowalarm', 'txbiaslowwarning']

SFP_TYPE_CODE_LIST = [
    '03'  # SFP/SFP+/SFP28
]
QSFP_TYPE_CODE_LIST = [
    '0d',  # QSFP+ or later
    '11'  # QSFP28 or later
]
QSFP_DD_TYPE_CODE_LIST = [
    '18'  # QSFP-DD Double Density 8X Pluggable Transceiver
]

SFP_TYPE = "SFP"
QSFP_TYPE = "QSFP"
OSFP_TYPE = "OSFP"
QSFP_DD_TYPE = "QSFP_DD"

NULL_VAL = 'N/A'

PORT_START = 0
PORT_END = 34
QSFP_PORT_START = 0
QSFP_PORT_END = 32

#SFP_I2C_START = 0
I2C_EEPROM_PATH = '/sys/bus/i2c/devices/i2c-{0}/{0}-0050/eeprom'
PORT_INFO_PATH= '/sys/class/t7132s_cpld'

class Sfp(SfpBase):
    """Platform-specific Sfp class"""
    PLATFORM = "x86_64-supermicro_sse_t7132s-r0"
    HWSKU = "Supermicro_sse_t7132s"

    _port_to_offset = [11, 30, 12, 29, 13, 28, 14, 27, 15, 34,
                       16, 33, 17, 32, 18, 31, 19, 38, 20, 37,
                       21, 36, 22, 35, 23, 42, 24, 41, 25, 40,
                       26, 39,
                       43, 44]
    _port_to_lanes = [[241, 242, 243, 244, 245, 246, 247, 248],
                      [249, 250, 251, 252, 253, 254, 255, 256],
                      [225, 226, 227, 228, 229, 230, 231, 232],
                      [233, 234, 235, 236, 237, 238, 239, 240],
                      [217, 218, 219, 220, 221, 222, 223, 224],
                      [209, 210, 211, 212, 213, 214, 215, 216],
                      [201, 202, 203, 204, 205, 206, 207, 208],
                      [193, 194, 195, 196, 197, 198, 199, 200],
                      [185, 186, 187, 188, 189, 190, 191, 192],
                      [177, 178, 179, 180, 181, 182, 183, 184],
                      [169, 170, 171, 172, 173, 174, 175, 176],
                      [161, 162, 163, 164, 165, 166, 167, 168],
                      [153, 154, 155, 156, 157, 158, 159, 160],
                      [145, 146, 147, 148, 149, 150, 151, 152],
                      [137, 138, 139, 140, 141, 142, 143, 144],
                      [129, 130, 131, 132, 133, 134, 135, 136],
                      [121, 122, 123, 124, 125, 126, 127, 128],
                      [113, 114, 115, 116, 117, 118, 119, 120],
                      [105, 106, 107, 108, 109, 110, 111, 112],
                      [ 97,  98,  99, 100, 101, 102, 103, 104],
                      [ 89,  90,  91,  92,  93,  94,  95,  96],
                      [ 81,  82,  83,  84,  85,  86,  87,  88],
                      [ 73,  74,  75,  76,  77,  78,  79,  80],
                      [ 65,  66,  67,  68,  69,  70,  71,  72],
                      [ 57,  58,  59,  60,  61,  62,  63,  64],
                      [ 49,  50,  51,  52,  53,  54,  55,  56],
                      [ 41,  42,  43,  44,  45,  46,  47,  48],
                      [ 33,  34,  35,  36,  37,  38,  39,  40],
                      [ 25,  26,  27,  28,  29,  30,  31,  32],
                      [ 17,  18,  19,  20,  21,  22,  23,  24],
                      [  9,  10,  11,  12,  13,  14,  15,  16],
                      [  1,   2,   3,   4,   5,   6,   7,   8],
                      [257],
                      [258]]

    def __init__(self, sfp_index=0, sfp_name=None, lanes=[]):
        SfpBase.__init__(self)

        self._index = sfp_index
        self._lanes = lanes
        self._master_port = self._get_master_port(self._lanes)
        self._port_num = self._master_port + 1
        self._api_helper = APIHelper()
        self._name = sfp_name
        self.sfp_type = QSFP_DD_TYPE
        #port_type is the native port type and sfp_type is the transceiver type
        #sfp_type will be detected in get_transceiver_info
        if self._master_port < QSFP_PORT_END:
            self.port_type = QSFP_DD_TYPE
            self.NUM_CHANNELS = 8
            self.port_name = "QSFP" + str(self._port_num)
        else:
            self.port_type = SFP_TYPE
            self.NUM_CHANNELS = 1
            self.port_name = "SFP" + str(self._port_num - QSFP_PORT_END)
        self.sfp_type = self.port_type

        self.dom_supported = False
        self.dom_temp_supported = False
        self.dom_volt_supported = False
        self.dom_rx_power_supported = False
        self.dom_tx_power_supported = False
        self.dom_tx_bias_power_supported = False
        self.calibration = 0

        self._eeprom_path = self._get_eeprom_path()
        self._dom_capability_detect()

        self._thermal_list = []    # to make each SFP has it's own thermal list

    def _get_master_port(self, lanes):
        for port_index, port_lanes in enumerate(self._port_to_lanes):
            # use lanes[0] only, because others should have the same master port
            if lanes[0] in port_lanes:
                return port_index
        return None

    def _get_path_to_port_config_file(self):
        host_platform_root_path = '/usr/share/sonic/device'
        docker_hwsku_path = '/usr/share/sonic/hwsku'

        host_platform_path = "/".join([host_platform_root_path, self.PLATFORM])
        hwsku_path = "/".join([host_platform_path, self.HWSKU]) \
            if self._api_helper.is_host() else docker_hwsku_path

        return "/".join([hwsku_path, "port_config.ini"])

    def _convert_string_to_num(self, value_str):
        if "-inf" in value_str:
            return 'N/A'
        elif "Unknown" in value_str:
            return 'N/A'
        elif 'dBm' in value_str:
            t_str = value_str.rstrip('dBm')
            return float(t_str)
        elif 'mA' in value_str:
            t_str = value_str.rstrip('mA')
            return float(t_str)
        elif 'C' in value_str:
            t_str = value_str.rstrip('C')
            return float(t_str)
        elif 'Volts' in value_str:
            t_str = value_str.rstrip('Volts')
            return float(t_str)
        else:
            return 'N/A'

    def _read_eeprom_specific_bytes(self, offset, num_bytes):
        sysfs_sfp_i2c_client_eeprom_path = self._get_eeprom_path()
        eeprom_raw = []
        try:
            eeprom = open(
                sysfs_sfp_i2c_client_eeprom_path,
                mode="rb", buffering=0)
        except IOError:
            return None

        for i in range(0, num_bytes):
            eeprom_raw.append("0x00")

        try:
            eeprom.seek(offset)
            raw = eeprom.read(num_bytes)
        except IOError:
            eeprom.close()
            return None

        try:
            if isinstance(raw, str):
                for n in range(0, num_bytes):
                    eeprom_raw[n] = hex(ord(raw[n]))[2:].zfill(2)
            else:
                for n in range(0, num_bytes):
                    eeprom_raw[n] = hex(raw[n])[2:].zfill(2)

        except BaseException:
            eeprom.close()
            return None

        eeprom.close()
        return eeprom_raw

    def _detect_sfp_type(self):
        eeprom_raw = []
        eeprom_ready = True

        time_begin = time.time()
        eeprom_ready = False
        while (time.time() - time_begin) < 4:
            # read 2 more bytes to check eeprom ready
            eeprom_raw = self._read_eeprom_specific_bytes(
                XCVR_TYPE_OFFSET, XCVR_TYPE_WIDTH + 2)

            if eeprom_raw:
                if eeprom_raw[0] in SFP_TYPE_CODE_LIST:
                    self.sfp_type = SFP_TYPE
                    eeprom_ready = True
                elif eeprom_raw[0] in QSFP_TYPE_CODE_LIST:
                    self.sfp_type = QSFP_TYPE
                    eeprom_ready = True
                elif eeprom_raw[0] in QSFP_DD_TYPE_CODE_LIST:
                    self.sfp_type = QSFP_DD_TYPE
                    eeprom_ready = True
                else:
                    self.sfp_type = self.port_type
                    if all([b == '00' for b in eeprom_raw]):
                        logger.Logger('SFP').log_warning(
                            "_detect_sfp_type: {} index {} by {} eeprom all 0".
                            format(self._name, self._index,
                                   inspect.currentframe().f_back.f_code.co_name))
                    else:
                        eeprom_ready = True
            else:
                logger.Logger('SFP').log_warning(
                    "_detect_sfp_type: {} index {} by {} eeprom none".
                    format(self._name, self._index,
                           inspect.currentframe().f_back.f_code.co_name))
                self.sfp_type = self.port_type

            if not eeprom_ready:
                # retry after sleep
                time.sleep(1)
            else:
                break;

        if self.sfp_type == QSFP_DD_TYPE:
            self.NUM_CHANNELS = 8
        elif self.sfp_type == QSFP_TYPE:
            self.NUM_CHANNELS = 4
        elif self.sfp_type == SFP_TYPE:
            self.NUM_CHANNELS = 1

        return eeprom_ready

    def _get_eeprom_path(self):
        #port_to_i2c_mapping = SFP_I2C_START + self._index
        port_eeprom_path = I2C_EEPROM_PATH.format(self._port_to_offset[self._master_port])
        return port_eeprom_path

    def _dom_capability_detect(self, check_presence=True):
        if check_presence:
            if not self.get_presence() or self.get_reset_status() or not self._detect_sfp_type():
                self.dom_supported = False
                self.dom_temp_supported = False
                self.dom_volt_supported = False
                self.dom_rx_power_supported = False
                self.dom_tx_power_supported = False
                self.dom_tx_bias_power_supported = False
                self.calibration = 0
                return

        if self.sfp_type == QSFP_TYPE:
            self.calibration = 1
            sfpi_obj = sff8436InterfaceId()
            if sfpi_obj is None:
                self.dom_supported = False
            offset = 128

            # QSFP capability byte parse,
            # through this byte can know whether it support tx_power or not.
            # TODO: in the future when decided to migrate to support SFF-8636 instead of SFF-8436,
            # need to add more code for determining the capability and version compliance
            # in SFF-8636 dom capability definitions evolving with the versions.

            qsfp_dom_capability_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_DOM_CAPABILITY_OFFSET),
                XCVR_DOM_CAPABILITY_WIDTH)
            if qsfp_dom_capability_raw is not None:
                qsfp_version_compliance_raw = self._read_eeprom_specific_bytes(
                    QSFP_VERSION_COMPLIANCE_OFFSET,
                    QSFP_VERSION_COMPLIANCE_WIDTH)
                qsfp_version_compliance = int(
                    qsfp_version_compliance_raw[0], 16)
                dom_capability = sfpi_obj.parse_dom_capability(
                    qsfp_dom_capability_raw, 0)
                if qsfp_version_compliance >= 0x08:
                    self.dom_temp_supported = dom_capability['data']['Temp_support']['value'] == 'On'
                    self.dom_volt_supported = dom_capability['data']['Voltage_support']['value'] == 'On'
                    self.dom_rx_power_supported = dom_capability['data']['Rx_power_support']['value'] == 'On'
                    self.dom_tx_power_supported = dom_capability['data']['Tx_power_support']['value'] == 'On'
                else:
                    self.dom_temp_supported = True
                    self.dom_volt_supported = True
                    self.dom_rx_power_supported = dom_capability['data']['Rx_power_support']['value'] == 'On'
                    self.dom_tx_power_supported = True

                self.dom_supported = True
                self.calibration = 1
                sfpd_obj = sff8436Dom()
                if sfpd_obj is None:
                    return None
                qsfp_option_value_raw = self._read_eeprom_specific_bytes(
                    QSFP_OPTION_VALUE_OFFSET, QSFP_OPTION_VALUE_WIDTH)
                if qsfp_option_value_raw is not None:
                    optional_capability = sfpd_obj.parse_option_params(
                        qsfp_option_value_raw, 0)
                    self.dom_tx_disable_supported = optional_capability[
                        'data']['TxDisable']['value'] == 'On'
                dom_status_indicator = sfpd_obj.parse_dom_status_indicator(
                    qsfp_version_compliance_raw, 1)
                self.qsfp_page3_available = dom_status_indicator['data']['FlatMem']['value'] == 'Off'
            else:
                self.dom_supported = False
                self.dom_temp_supported = False
                self.dom_volt_supported = False
                self.dom_rx_power_supported = False
                self.dom_tx_power_supported = False
                self.calibration = 0
                self.qsfp_page3_available = False

        elif self.sfp_type == QSFP_DD_TYPE:
            sfpi_obj = qsfp_dd_InterfaceId()
            if sfpi_obj is None:
                self.dom_supported = False

            offset = 0
            # two types of QSFP-DD cable types supported: Copper and Optical.
            qsfp_dom_capability_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_DOM_CAPABILITY_OFFSET_QSFP_DD), XCVR_DOM_CAPABILITY_WIDTH_QSFP_DD)
            if qsfp_dom_capability_raw is not None:
                self.dom_temp_supported = True
                self.dom_volt_supported = True
                dom_capability = sfpi_obj.parse_dom_capability(
                    qsfp_dom_capability_raw, 0)
                if dom_capability['data']['Flat_MEM']['value'] == 'Off':
                    self.dom_supported = True
                    self.second_application_list = True
                    self.dom_thresholds_supported = True
                else:
                    self.dom_supported = False
                    self.second_application_list = False
                    self.dom_thresholds_supported = False

                if self.dom_supported:
                    lane_mon_advt_raw = self._read_eeprom_specific_bytes(
                        (QSFP_DD_LANE_MON_ADVT_PAGE * 128 + QSFP_DD_LANE_MON_ADVT_OFFSET),
                        QSFP_DD_LANE_MON_ADVT_WIDTH)
                    if lane_mon_advt_raw is not None:
                        lane_mon_advt_data = int(lane_mon_advt_raw[0], 16)
                    else:
                        lane_mon_advt_data = 0
                    self.dom_rx_power_supported = (lane_mon_advt_data & 0x04 != 0)
                    self.dom_tx_power_supported = (lane_mon_advt_data & 0x02 != 0)
                    self.dom_tx_bias_power_supported = (lane_mon_advt_data & 0x01 != 0)
            else:
                self.dom_supported = False
                self.dom_temp_supported = False
                self.dom_volt_supported = False
                self.dom_rx_power_supported = False
                self.dom_tx_power_supported = False
                self.dom_tx_bias_power_supported = False
                self.dom_thresholds_supported = False

        elif self.sfp_type == SFP_TYPE:
            sfpi_obj = sff8472InterfaceId()
            if sfpi_obj is None:
                return None
            sfp_dom_capability_raw = self._read_eeprom_specific_bytes(
                XCVR_DOM_CAPABILITY_OFFSET, XCVR_DOM_CAPABILITY_WIDTH)
            if sfp_dom_capability_raw is not None:
                sfp_dom_capability = int(sfp_dom_capability_raw[0], 16)
                self.dom_supported = (sfp_dom_capability & 0x40 != 0)
                if self.dom_supported:
                    self.dom_temp_supported = True
                    self.dom_volt_supported = True
                    self.dom_rx_power_supported = True
                    self.dom_tx_power_supported = True
                    if sfp_dom_capability & 0x20 != 0:
                        self.calibration = 1
                    elif sfp_dom_capability & 0x10 != 0:
                        self.calibration = 2
                    else:
                        self.calibration = 0
                else:
                    self.dom_temp_supported = False
                    self.dom_volt_supported = False
                    self.dom_rx_power_supported = False
                    self.dom_tx_power_supported = False
                    self.calibration = 0
                self.dom_tx_disable_supported = (
                    int(sfp_dom_capability_raw[1], 16) & 0x40 != 0)
        else:
            self.dom_supported = False
            self.dom_temp_supported = False
            self.dom_volt_supported = False
            self.dom_rx_power_supported = False
            self.dom_tx_power_supported = False
            self.dom_tx_bias_power_supported = False

    def get_transceiver_info(self):
        """
        Retrieves transceiver info of this SFP
        Returns:
            A dict which contains following keys/values :
        ================================================================================
        keys                       |Value Format   |Information
        ---------------------------|---------------|----------------------------
        type                       |1*255VCHAR     |type of SFP
        hardware_rev               |1*255VCHAR     |hardware version of SFP
        serial                     |1*255VCHAR     |serial number of the SFP
        manufacturer               |1*255VCHAR     |SFP vendor name
        model                      |1*255VCHAR     |SFP model name
        connector                  |1*255VCHAR     |connector information
        encoding                   |1*255VCHAR     |encoding information
        ext_identifier             |1*255VCHAR     |extend identifier
        ext_rateselect_compliance  |1*255VCHAR     |extended rateSelect compliance
        cable_length               |INT            |cable length in m
        nominal_bit_rate           |INT            |nominal bit rate by 100Mbs
        specification_compliance   |1*255VCHAR     |specification compliance
        vendor_date                |1*255VCHAR     |vendor date
        vendor_oui                 |1*255VCHAR     |vendor OUI
        application_advertisement  |1*255VCHAR     |supported applications advertisement
        ================================================================================
        """

        transceiver_info_dict = {}
        compliance_code_dict = {}
        transceiver_info_dict = dict.fromkeys(
            info_dict_keys, NULL_VAL)
        transceiver_info_dict["specification_compliance"] = '{}'
        dom_capability_dict = dict()

        if not self.get_presence():
            return transceiver_info_dict
        if not self._detect_sfp_type():
            return transceiver_info_dict
        self._dom_capability_detect(check_presence=False)

        # ToDo: OSFP tranceiver info parsing not fully supported.
        # in inf8628.py lack of some memory map definition
        # will be implemented when the inf8628 memory map ready
        if self.sfp_type == OSFP_TYPE:
            offset = 0
            vendor_rev_width = XCVR_HW_REV_WIDTH_OSFP

            sfpi_obj = inf8628InterfaceId()
            if sfpi_obj is None:
                return transceiver_info_dict

            sfp_type_raw = self._read_eeprom_specific_bytes(
                (offset + OSFP_TYPE_OFFSET), XCVR_TYPE_WIDTH)
            if sfp_type_raw is not None:
                sfp_type_data = sfpi_obj.parse_sfp_type(sfp_type_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_name_raw = self._read_eeprom_specific_bytes(
                (offset + OSFP_VENDOR_NAME_OFFSET), XCVR_VENDOR_NAME_WIDTH)
            if sfp_vendor_name_raw is not None:
                sfp_vendor_name_data = sfpi_obj.parse_vendor_name(
                    sfp_vendor_name_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_pn_raw = self._read_eeprom_specific_bytes(
                (offset + OSFP_VENDOR_PN_OFFSET), XCVR_VENDOR_PN_WIDTH)
            if sfp_vendor_pn_raw is not None:
                sfp_vendor_pn_data = sfpi_obj.parse_vendor_pn(
                    sfp_vendor_pn_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_rev_raw = self._read_eeprom_specific_bytes(
                (offset + OSFP_HW_REV_OFFSET), vendor_rev_width)
            if sfp_vendor_rev_raw is not None:
                sfp_vendor_rev_data = sfpi_obj.parse_vendor_rev(
                    sfp_vendor_rev_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_sn_raw = self._read_eeprom_specific_bytes(
                (offset + OSFP_VENDOR_SN_OFFSET), XCVR_VENDOR_SN_WIDTH)
            if sfp_vendor_sn_raw is not None:
                sfp_vendor_sn_data = sfpi_obj.parse_vendor_sn(
                    sfp_vendor_sn_raw, 0)
            else:
                return transceiver_info_dict

            transceiver_info_dict['type'] = sfp_type_data['data']['type']['value']
            transceiver_info_dict['manufacturer'] = sfp_vendor_name_data['data']['Vendor Name']['value']
            transceiver_info_dict['model'] = sfp_vendor_pn_data['data']['Vendor PN']['value']
            transceiver_info_dict['hardware_rev'] = sfp_vendor_rev_data['data']['Vendor Rev']['value']
            transceiver_info_dict['serial'] = sfp_vendor_sn_data['data']['Vendor SN']['value']

        elif self.sfp_type == QSFP_TYPE:
            offset = 128
            vendor_rev_width = XCVR_HW_REV_WIDTH_QSFP
            interface_info_bulk_width = XCVR_INTFACE_BULK_WIDTH_QSFP

            sfpi_obj = sff8436InterfaceId()
            if sfpi_obj is None:
                print("Error: sfp_object open failed")
                return transceiver_info_dict

        elif self.sfp_type == QSFP_DD_TYPE:
            offset = 128

            sfpi_obj = qsfp_dd_InterfaceId()
            if sfpi_obj is None:
                print("Error: sfp_object open failed")
                return transceiver_info_dict

            sfp_type_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_TYPE_OFFSET), XCVR_TYPE_WIDTH)
            if sfp_type_raw is not None:
                sfp_type_data = sfpi_obj.parse_sfp_type(sfp_type_raw, 0)
                sfp_type_abbrv_name_data = sfpi_obj.parse_sfp_type_abbrv_name(
                    sfp_type_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_name_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_VENDOR_NAME_OFFSET), XCVR_VENDOR_NAME_WIDTH)
            if sfp_vendor_name_raw is not None:
                sfp_vendor_name_data = sfpi_obj.parse_vendor_name(
                    sfp_vendor_name_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_pn_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_VENDOR_PN_OFFSET), XCVR_VENDOR_PN_WIDTH)
            if sfp_vendor_pn_raw is not None:
                sfp_vendor_pn_data = sfpi_obj.parse_vendor_pn(
                    sfp_vendor_pn_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_rev_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_HW_REV_OFFSET_QSFP_DD), XCVR_HW_REV_WIDTH_QSFP_DD)
            if sfp_vendor_rev_raw is not None:
                sfp_vendor_rev_data = sfpi_obj.parse_vendor_rev(
                    sfp_vendor_rev_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_sn_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_VENDOR_SN_OFFSET), XCVR_VENDOR_SN_WIDTH)
            if sfp_vendor_sn_raw is not None:
                sfp_vendor_sn_data = sfpi_obj.parse_vendor_sn(
                    sfp_vendor_sn_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_oui_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_VENDOR_OUI_OFFSET), XCVR_VENDOR_OUI_WIDTH)
            if sfp_vendor_oui_raw is not None:
                sfp_vendor_oui_data = sfpi_obj.parse_vendor_oui(
                    sfp_vendor_oui_raw, 0)
            else:
                return transceiver_info_dict

            sfp_vendor_date_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_VENDOR_DATE_OFFSET_QSFP_DD), XCVR_VENDOR_DATE_WIDTH_QSFP_DD)
            if sfp_vendor_date_raw is not None:
                sfp_vendor_date_data = sfpi_obj.parse_vendor_date(
                    sfp_vendor_date_raw, 0)
            else:
                return transceiver_info_dict

            sfp_connector_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_CONNECTOR_OFFSET_QSFP_DD), XCVR_CONNECTOR_WIDTH_QSFP_DD)
            if sfp_connector_raw is not None:
                sfp_connector_data = sfpi_obj.parse_connector(
                    sfp_connector_raw, 0)
            else:
                return transceiver_info_dict

            sfp_ext_identifier_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_EXT_TYPE_OFFSET_QSFP_DD), XCVR_EXT_TYPE_WIDTH_QSFP_DD)
            if sfp_ext_identifier_raw is not None:
                sfp_ext_identifier_data = sfpi_obj.parse_ext_iden(
                    sfp_ext_identifier_raw, 0)
            else:
                return transceiver_info_dict

            sfp_cable_len_raw = self._read_eeprom_specific_bytes(
                (offset + XCVR_CABLE_LENGTH_OFFSET_QSFP_DD), XCVR_CABLE_LENGTH_WIDTH_QSFP_DD)
            if sfp_cable_len_raw is not None:
                sfp_cable_len_data = sfpi_obj.parse_cable_len(
                    sfp_cable_len_raw, 0)
            else:
                return transceiver_info_dict

            sfp_media_type_raw = self._read_eeprom_specific_bytes(
                XCVR_MEDIA_TYPE_OFFSET_QSFP_DD, XCVR_MEDIA_TYPE_WIDTH_QSFP_DD)
            if sfp_media_type_raw is not None:
                sfp_media_type_dict = sfpi_obj.parse_media_type(
                    sfp_media_type_raw, 0)
                if sfp_media_type_dict is None:
                    return transceiver_info_dict

                host_media_list = ""
                sfp_application_type_first_list = self._read_eeprom_specific_bytes(
                    (XCVR_FIRST_APPLICATION_LIST_OFFSET_QSFP_DD), XCVR_FIRST_APPLICATION_LIST_WIDTH_QSFP_DD)
                if self.second_application_list:
                    possible_application_count = 15
                    sfp_application_type_second_list = self._read_eeprom_specific_bytes(
                        (XCVR_SECOND_APPLICATION_LIST_OFFSET_QSFP_DD), XCVR_SECOND_APPLICATION_LIST_WIDTH_QSFP_DD)
                    if sfp_application_type_first_list is not None and sfp_application_type_second_list is not None:
                        sfp_application_type_list = sfp_application_type_first_list + \
                            sfp_application_type_second_list
                    else:
                        return transceiver_info_dict
                else:
                    possible_application_count = 8
                    if sfp_application_type_first_list is not None:
                        sfp_application_type_list = sfp_application_type_first_list
                    else:
                        return transceiver_info_dict

                for i in range(0, possible_application_count):
                    if sfp_application_type_list[i * 4] == 'ff':
                        break
                    host_electrical, media_interface = sfpi_obj.parse_application(
                        sfp_media_type_dict, sfp_application_type_list[i * 4], sfp_application_type_list[i * 4 + 1])
                    host_media_list = host_media_list + host_electrical + \
                        ' - ' + media_interface + '\n\t\t\t\t   '
            else:
                return transceiver_info_dict

            transceiver_info_dict['type'] = str(
                sfp_type_data['data']['type']['value'])
            transceiver_info_dict['manufacturer'] = str(
                sfp_vendor_name_data['data']['Vendor Name']['value'])
            transceiver_info_dict['model'] = str(
                sfp_vendor_pn_data['data']['Vendor PN']['value'])
            transceiver_info_dict['hardware_rev'] = str(
                sfp_vendor_rev_data['data']['Vendor Rev']['value'])
            transceiver_info_dict['serial'] = str(
                sfp_vendor_sn_data['data']['Vendor SN']['value'])
            transceiver_info_dict['vendor_oui'] = str(
                sfp_vendor_oui_data['data']['Vendor OUI']['value'])
            transceiver_info_dict['vendor_date'] = str(
                sfp_vendor_date_data['data']['VendorDataCode(YYYY-MM-DD Lot)']['value'])
            transceiver_info_dict['connector'] = str(
                sfp_connector_data['data']['Connector']['value'])
            transceiver_info_dict['encoding'] = "Not supported for CMIS cables"
            transceiver_info_dict['ext_identifier'] = str(
                sfp_ext_identifier_data['data']['Extended Identifier']['value'])
            transceiver_info_dict['ext_rateselect_compliance'] = "Not supported for CMIS cables"
            transceiver_info_dict['specification_compliance'] = type_of_media_interface[sfp_media_type_raw[0]]
            transceiver_info_dict['cable_type'] = "Length Cable Assembly(m)"
            transceiver_info_dict['cable_length'] = str(
                sfp_cable_len_data['data']['Length Cable Assembly(m)']['value'])
            transceiver_info_dict['nominal_bit_rate'] = "Not supported for CMIS cables"
            transceiver_info_dict['application_advertisement'] = host_media_list
            transceiver_info_dict['type_abbrv_name'] = str(
                sfp_type_abbrv_name_data['data']['type_abbrv_name']['value'])
            transceiver_info_dict['is_replaceable'] = "yes"

            qsfp_dd_dom_capability_tup_self = ('dom_tx_bias_power_supported',
                                               'dom_tx_power_supported',
                                               'dom_rx_power_supported',
                                               'dom_volt_supported',
                                               'dom_temp_supported')
            for key,s in zip(qsfp_dd_dom_capability_tup, qsfp_dd_dom_capability_tup_self):
                dom_capability_dict[key] = "yes" if getattr(self, s, False) == True else "no"
            dom_capability_dict['Flat_MEM'] = "Off" if self.dom_supported == True else "On"
            transceiver_info_dict['dom_capability'] = str(dom_capability_dict)

        else:
            offset = 0
            vendor_rev_width = XCVR_HW_REV_WIDTH_SFP
            interface_info_bulk_width = XCVR_INTFACE_BULK_WIDTH_SFP

            sfpi_obj = sff8472InterfaceId()
            if sfpi_obj is None:
                print("Error: sfp_object open failed")
                return transceiver_info_dict

        if self.sfp_type != QSFP_DD_TYPE:
            sfp_interface_bulk_raw = self._read_eeprom_specific_bytes(
                offset + XCVR_INTERFACE_DATA_START, XCVR_INTERFACE_DATA_SIZE)
            if sfp_interface_bulk_raw is None:
                return transceiver_info_dict

            start = XCVR_INTFACE_BULK_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + interface_info_bulk_width
            sfp_interface_bulk_data = sfpi_obj.parse_sfp_info_bulk(
                sfp_interface_bulk_raw[start: end], 0)

            start = XCVR_VENDOR_NAME_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + XCVR_VENDOR_NAME_WIDTH
            sfp_vendor_name_data = sfpi_obj.parse_vendor_name(
                sfp_interface_bulk_raw[start: end], 0)

            start = XCVR_VENDOR_PN_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + XCVR_VENDOR_PN_WIDTH
            sfp_vendor_pn_data = sfpi_obj.parse_vendor_pn(
                sfp_interface_bulk_raw[start: end], 0)

            start = XCVR_HW_REV_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + vendor_rev_width
            sfp_vendor_rev_data = sfpi_obj.parse_vendor_rev(
                sfp_interface_bulk_raw[start: end], 0)

            start = XCVR_VENDOR_SN_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + XCVR_VENDOR_SN_WIDTH
            sfp_vendor_sn_data = sfpi_obj.parse_vendor_sn(
                sfp_interface_bulk_raw[start: end], 0)

            start = XCVR_VENDOR_OUI_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + XCVR_VENDOR_OUI_WIDTH
            sfp_vendor_oui_data = sfpi_obj.parse_vendor_oui(
                sfp_interface_bulk_raw[start: end], 0)

            start = XCVR_VENDOR_DATE_OFFSET - XCVR_INTERFACE_DATA_START
            end = start + XCVR_VENDOR_DATE_WIDTH
            sfp_vendor_date_data = sfpi_obj.parse_vendor_date(
                sfp_interface_bulk_raw[start: end], 0)

            transceiver_info_dict['type'] = sfp_interface_bulk_data['data']['type']['value']
            transceiver_info_dict['manufacturer'] = sfp_vendor_name_data['data']['Vendor Name']['value']
            transceiver_info_dict['model'] = sfp_vendor_pn_data['data']['Vendor PN']['value']
            transceiver_info_dict['hardware_rev'] = sfp_vendor_rev_data['data']['Vendor Rev']['value']
            transceiver_info_dict['serial'] = sfp_vendor_sn_data['data']['Vendor SN']['value']
            transceiver_info_dict['vendor_oui'] = sfp_vendor_oui_data['data']['Vendor OUI']['value']
            transceiver_info_dict['vendor_date'] = sfp_vendor_date_data[
                'data']['VendorDataCode(YYYY-MM-DD Lot)']['value']
            transceiver_info_dict['connector'] = sfp_interface_bulk_data['data']['Connector']['value']
            transceiver_info_dict['encoding'] = sfp_interface_bulk_data['data']['EncodingCodes']['value']
            transceiver_info_dict['ext_identifier'] = sfp_interface_bulk_data['data']['Extended Identifier']['value']
            transceiver_info_dict['ext_rateselect_compliance'] = sfp_interface_bulk_data['data']['RateIdentifier']['value']
            transceiver_info_dict['type_abbrv_name'] = sfp_interface_bulk_data['data']['type_abbrv_name']['value']
            transceiver_info_dict['is_replaceable'] = "yes"

            if self.sfp_type == QSFP_TYPE:
                for key in qsfp_cable_length_tup:
                    if key in sfp_interface_bulk_data['data']:
                        if sfp_interface_bulk_data['data'][key]['value'] <= 0:
                            continue
                        transceiver_info_dict['cable_type'] = key
                        transceiver_info_dict['cable_length'] = str(
                            sfp_interface_bulk_data['data'][key]['value'])
                        break

                for key in qsfp_compliance_code_tup:
                    if key in sfp_interface_bulk_data['data']['Specification compliance']['value']:
                        compliance_code_dict[key] = sfp_interface_bulk_data['data']['Specification compliance']['value'][key]['value']
                sfp_ext_specification_compliance_raw = self._read_eeprom_specific_bytes(
                    offset + XCVR_EXT_SPECIFICATION_COMPLIANCE_OFFSET, XCVR_EXT_SPECIFICATION_COMPLIANCE_WIDTH)
                if sfp_ext_specification_compliance_raw is not None:
                    sfp_ext_specification_compliance_data = sfpi_obj.parse_ext_specification_compliance(
                        sfp_ext_specification_compliance_raw[0: 1], 0)
                    if sfp_ext_specification_compliance_data['data']['Extended Specification compliance']['value'] != "Unspecified":
                        compliance_code_dict['Extended Specification compliance'] = sfp_ext_specification_compliance_data[
                            'data']['Extended Specification compliance']['value']
                transceiver_info_dict['specification_compliance'] = str(
                    compliance_code_dict)
                transceiver_info_dict['nominal_bit_rate'] = str(
                    sfp_interface_bulk_data['data']['Nominal Bit Rate(100Mbs)']['value'])

                qsfp_dom_capability_tup_self = ('dom_tx_power_supported',
                                                'dom_rx_power_supported',
                                                'dom_volt_supported',
                                                'dom_temp_supported')
                for key,s in zip(qsfp_dom_capability_tup, qsfp_dom_capability_tup_self):
                    dom_capability_dict[key] = "yes" if getattr(self, s, False) == True else "no"
                transceiver_info_dict['dom_capability'] = str(dom_capability_dict)

            else:
                for key in sfp_cable_length_tup:
                    if key in sfp_interface_bulk_data['data']:
                        if sfp_interface_bulk_data['data'][key]['value'] <= 0:
                            continue
                        transceiver_info_dict['cable_type'] = key
                        transceiver_info_dict['cable_length'] = str(
                            sfp_interface_bulk_data['data'][key]['value'])
                        break

                for key in sfp_compliance_code_tup:
                    if key in sfp_interface_bulk_data['data']['Specification compliance']['value']:
                        compliance_code_dict[key] = sfp_interface_bulk_data['data']['Specification compliance']['value'][key]['value']
                transceiver_info_dict['specification_compliance'] = str(
                    compliance_code_dict)

                transceiver_info_dict['nominal_bit_rate'] = str(
                    sfp_interface_bulk_data['data']['NominalSignallingRate(UnitsOf100Mbd)']['value'])

                sfp_dom_capability_tup_self = ('dom_tx_power_supported',
                                                'EOL')
                for key,s in zip(sfp_dom_capability_tup, sfp_dom_capability_tup_self):
                    if key != 'EOL':
                        dom_capability_dict[key] = "yes" if getattr(self, s, False) == True else "no"
                transceiver_info_dict['dom_capability'] = str(dom_capability_dict)

        return transceiver_info_dict

    def get_transceiver_bulk_status(self):
        """
        Retrieves transceiver bulk status of this SFP
        Returns:
            A dict which contains following keys/values :
        ========================================================================
        keys                       |Value Format   |Information
        ---------------------------|---------------|----------------------------
        rx_los                     |BOOLEAN        |RX loss-of-signal status, True if has RX los, False if not.
        tx_fault                   |BOOLEAN        |TX fault status, True if has TX fault, False if not.
        reset_status               |BOOLEAN        |reset status, True if SFP in reset, False if not.
        lp_mode                    |BOOLEAN        |low power mode status, True in lp mode, False if not.
        tx_disable                 |BOOLEAN        |TX disable status, True TX disabled, False if not.
        tx_disabled_channel        |HEX            |disabled TX channels in hex, bits 0 to 3 represent channel 0
                                   |               |to channel 3.
        temperature                |INT            |module temperature in Celsius
        voltage                    |INT            |supply voltage in mV
        tx<n>bias                  |INT            |TX Bias Current in mA, n is the channel number,
                                   |               |for example, tx2bias stands for tx bias of channel 2.
        rx<n>power                 |INT            |received optical power in mW, n is the channel number,
                                   |               |for example, rx2power stands for rx power of channel 2.
        tx<n>power                 |INT            |TX output power in mW, n is the channel number,
                                   |               |for example, tx2power stands for tx power of channel 2.
        ========================================================================
        """
        transceiver_dom_info_dict = dict.fromkeys(
            dom_info_dict_keys, NULL_VAL)

        if not self.get_presence():
            return transceiver_dom_info_dict
        if not self._detect_sfp_type():
            return transceiver_dom_info_dict
        self._dom_capability_detect(check_presence=False)

        if self.sfp_type == OSFP_TYPE:
            pass

        elif self.sfp_type == QSFP_TYPE:
            if not self.dom_supported:
                return transceiver_dom_info_dict

            offset = 0
            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return transceiver_dom_info_dict

            dom_data_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DOM_BULK_DATA_START), QSFP_DOM_BULK_DATA_SIZE)
            if dom_data_raw is None:
                return transceiver_dom_info_dict

            if self.dom_temp_supported:
                start = QSFP_TEMPE_OFFSET - QSFP_DOM_BULK_DATA_START
                end = start + QSFP_TEMPE_WIDTH
                dom_temperature_data = sfpd_obj.parse_temperature(
                    dom_data_raw[start: end], 0)
                temp = dom_temperature_data['data']['Temperature']['value']
                if temp is not None:
                    transceiver_dom_info_dict['temperature'] = temp

            if self.dom_volt_supported:
                start = QSFP_VOLT_OFFSET - QSFP_DOM_BULK_DATA_START
                end = start + QSFP_VOLT_WIDTH
                dom_voltage_data = sfpd_obj.parse_voltage(
                    dom_data_raw[start: end], 0)
                volt = dom_voltage_data['data']['Vcc']['value']
                if volt is not None:
                    transceiver_dom_info_dict['voltage'] = volt

            start = QSFP_CHANNL_MON_OFFSET - QSFP_DOM_BULK_DATA_START
            end = start + QSFP_CHANNL_MON_WITH_TX_POWER_WIDTH
            dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params_with_tx_power(
                dom_data_raw[start: end], 0)

            if self.dom_tx_power_supported:
                transceiver_dom_info_dict['tx1power'] = dom_channel_monitor_data['data']['TX1Power']['value']
                transceiver_dom_info_dict['tx2power'] = dom_channel_monitor_data['data']['TX2Power']['value']
                transceiver_dom_info_dict['tx3power'] = dom_channel_monitor_data['data']['TX3Power']['value']
                transceiver_dom_info_dict['tx4power'] = dom_channel_monitor_data['data']['TX4Power']['value']

            if self.dom_rx_power_supported:
                transceiver_dom_info_dict['rx1power'] = dom_channel_monitor_data['data']['RX1Power']['value']
                transceiver_dom_info_dict['rx2power'] = dom_channel_monitor_data['data']['RX2Power']['value']
                transceiver_dom_info_dict['rx3power'] = dom_channel_monitor_data['data']['RX3Power']['value']
                transceiver_dom_info_dict['rx4power'] = dom_channel_monitor_data['data']['RX4Power']['value']

            transceiver_dom_info_dict['tx1bias'] = dom_channel_monitor_data['data']['TX1Bias']['value']
            transceiver_dom_info_dict['tx2bias'] = dom_channel_monitor_data['data']['TX2Bias']['value']
            transceiver_dom_info_dict['tx3bias'] = dom_channel_monitor_data['data']['TX3Bias']['value']
            transceiver_dom_info_dict['tx4bias'] = dom_channel_monitor_data['data']['TX4Bias']['value']

        elif self.sfp_type == QSFP_DD_TYPE:

            offset = 0
            sfpd_obj = qsfp_dd_Dom()
            if sfpd_obj is None:
                return transceiver_dom_info_dict

            dom_data_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_DOM_BULK_DATA_START), QSFP_DD_DOM_BULK_DATA_SIZE)
            if dom_data_raw is None:
                return transceiver_dom_info_dict

            if self.dom_temp_supported:
                start = QSFP_DD_TEMPE_OFFSET - QSFP_DD_DOM_BULK_DATA_START
                end = start + QSFP_DD_TEMPE_WIDTH
                dom_temperature_data = sfpd_obj.parse_temperature(
                    dom_data_raw[start: end], 0)
                temp = dom_temperature_data['data']['Temperature']['value']
                if temp is not None:
                    transceiver_dom_info_dict['temperature'] = temp

            if self.dom_volt_supported:
                start = QSFP_DD_VOLT_OFFSET - QSFP_DD_DOM_BULK_DATA_START
                end = start + QSFP_DD_VOLT_WIDTH
                dom_voltage_data = sfpd_obj.parse_voltage(
                    dom_data_raw[start: end], 0)
                volt = dom_voltage_data['data']['Vcc']['value']
                if volt is not None:
                    transceiver_dom_info_dict['voltage'] = volt

            dom_data_raw = self._read_eeprom_specific_bytes(
                (QSFP_DD_CHANNL_MON_PAGE * 128 + QSFP_DD_CHANNL_MON_OFFSET),
                QSFP_DD_CHANNL_MON_WIDTH)
            if dom_data_raw is None:
                return transceiver_dom_info_dict
            dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params(
                dom_data_raw, 0)

            if self.dom_tx_power_supported:
                transceiver_dom_info_dict['tx1power'] = str(
                    dom_channel_monitor_data['data']['TX1Power']['value'])
                transceiver_dom_info_dict['tx2power'] = str(
                    dom_channel_monitor_data['data']['TX2Power']['value'])
                transceiver_dom_info_dict['tx3power'] = str(
                    dom_channel_monitor_data['data']['TX3Power']['value'])
                transceiver_dom_info_dict['tx4power'] = str(
                    dom_channel_monitor_data['data']['TX4Power']['value'])
                transceiver_dom_info_dict['tx5power'] = str(
                    dom_channel_monitor_data['data']['TX5Power']['value'])
                transceiver_dom_info_dict['tx6power'] = str(
                    dom_channel_monitor_data['data']['TX6Power']['value'])
                transceiver_dom_info_dict['tx7power'] = str(
                    dom_channel_monitor_data['data']['TX7Power']['value'])
                transceiver_dom_info_dict['tx8power'] = str(
                    dom_channel_monitor_data['data']['TX8Power']['value'])

            if self.dom_rx_power_supported:
                transceiver_dom_info_dict['rx1power'] = str(
                    dom_channel_monitor_data['data']['RX1Power']['value'])
                transceiver_dom_info_dict['rx2power'] = str(
                    dom_channel_monitor_data['data']['RX2Power']['value'])
                transceiver_dom_info_dict['rx3power'] = str(
                    dom_channel_monitor_data['data']['RX3Power']['value'])
                transceiver_dom_info_dict['rx4power'] = str(
                    dom_channel_monitor_data['data']['RX4Power']['value'])
                transceiver_dom_info_dict['rx5power'] = str(
                    dom_channel_monitor_data['data']['RX5Power']['value'])
                transceiver_dom_info_dict['rx6power'] = str(
                    dom_channel_monitor_data['data']['RX6Power']['value'])
                transceiver_dom_info_dict['rx7power'] = str(
                    dom_channel_monitor_data['data']['RX7Power']['value'])
                transceiver_dom_info_dict['rx8power'] = str(
                    dom_channel_monitor_data['data']['RX8Power']['value'])

            if self.dom_tx_bias_power_supported:
                transceiver_dom_info_dict['tx1bias'] = str(
                    dom_channel_monitor_data['data']['TX1Bias']['value'])
                transceiver_dom_info_dict['tx2bias'] = str(
                    dom_channel_monitor_data['data']['TX2Bias']['value'])
                transceiver_dom_info_dict['tx3bias'] = str(
                    dom_channel_monitor_data['data']['TX3Bias']['value'])
                transceiver_dom_info_dict['tx4bias'] = str(
                    dom_channel_monitor_data['data']['TX4Bias']['value'])
                transceiver_dom_info_dict['tx5bias'] = str(
                    dom_channel_monitor_data['data']['TX5Bias']['value'])
                transceiver_dom_info_dict['tx6bias'] = str(
                    dom_channel_monitor_data['data']['TX6Bias']['value'])
                transceiver_dom_info_dict['tx7bias'] = str(
                    dom_channel_monitor_data['data']['TX7Bias']['value'])
                transceiver_dom_info_dict['tx8bias'] = str(
                    dom_channel_monitor_data['data']['TX8Bias']['value'])

        else:
            if not self.dom_supported:
                return transceiver_dom_info_dict

            offset = 256
            sfpd_obj = sff8472Dom()
            if sfpd_obj is None:
                return transceiver_dom_info_dict
            sfpd_obj._calibration_type = self.calibration

            dom_data_raw = self._read_eeprom_specific_bytes(
                (offset + SFP_DOM_BULK_DATA_START), SFP_DOM_BULK_DATA_SIZE)

            start = SFP_TEMPE_OFFSET - SFP_DOM_BULK_DATA_START
            end = start + SFP_TEMPE_WIDTH
            dom_temperature_data = sfpd_obj.parse_temperature(
                dom_data_raw[start: end], 0)

            start = SFP_VOLT_OFFSET - SFP_DOM_BULK_DATA_START
            end = start + SFP_VOLT_WIDTH
            dom_voltage_data = sfpd_obj.parse_voltage(
                dom_data_raw[start: end], 0)

            start = SFP_CHANNL_MON_OFFSET - SFP_DOM_BULK_DATA_START
            end = start + SFP_CHANNL_MON_WIDTH
            dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params(
                dom_data_raw[start: end], 0)

            transceiver_dom_info_dict['temperature'] = dom_temperature_data['data']['Temperature']['value']
            transceiver_dom_info_dict['voltage'] = dom_voltage_data['data']['Vcc']['value']
            transceiver_dom_info_dict['rx1power'] = dom_channel_monitor_data['data']['RXPower']['value']
            transceiver_dom_info_dict['tx1bias'] = dom_channel_monitor_data['data']['TXBias']['value']
            transceiver_dom_info_dict['tx1power'] = dom_channel_monitor_data['data']['TXPower']['value']

        transceiver_dom_info_dict['lp_mode'] = self.get_lpmode()
        transceiver_dom_info_dict['reset_status'] = self.get_reset_status()
        transceiver_dom_info_dict['tx_disable'] = self.get_tx_disable()
        transceiver_dom_info_dict['tx_disabled_channel'] = self.get_tx_disable_channel()

        for key in transceiver_dom_info_dict:
            val = transceiver_dom_info_dict[key]
            transceiver_dom_info_dict[key] = self._convert_string_to_num(
                val) if type(val) is str else val

        return transceiver_dom_info_dict

    def get_transceiver_threshold_info(self):
        """
        Retrieves transceiver threshold info of this SFP

        Returns:
            A dict which contains following keys/values :
        ========================================================================
        keys                       |Value Format   |Information
        ---------------------------|---------------|----------------------------
        temphighalarm              |FLOAT          |High Alarm Threshold value of temperature in Celsius.
        templowalarm               |FLOAT          |Low Alarm Threshold value of temperature in Celsius.
        temphighwarning            |FLOAT          |High Warning Threshold value of temperature in Celsius.
        templowwarning             |FLOAT          |Low Warning Threshold value of temperature in Celsius.
        vcchighalarm               |FLOAT          |High Alarm Threshold value of supply voltage in mV.
        vcclowalarm                |FLOAT          |Low Alarm Threshold value of supply voltage in mV.
        vcchighwarning             |FLOAT          |High Warning Threshold value of supply voltage in mV.
        vcclowwarning              |FLOAT          |Low Warning Threshold value of supply voltage in mV.
        rxpowerhighalarm           |FLOAT          |High Alarm Threshold value of received power in dBm.
        rxpowerlowalarm            |FLOAT          |Low Alarm Threshold value of received power in dBm.
        rxpowerhighwarning         |FLOAT          |High Warning Threshold value of received power in dBm.
        rxpowerlowwarning          |FLOAT          |Low Warning Threshold value of received power in dBm.
        txpowerhighalarm           |FLOAT          |High Alarm Threshold value of transmit power in dBm.
        txpowerlowalarm            |FLOAT          |Low Alarm Threshold value of transmit power in dBm.
        txpowerhighwarning         |FLOAT          |High Warning Threshold value of transmit power in dBm.
        txpowerlowwarning          |FLOAT          |Low Warning Threshold value of transmit power in dBm.
        txbiashighalarm            |FLOAT          |High Alarm Threshold value of tx Bias Current in mA.
        txbiaslowalarm             |FLOAT          |Low Alarm Threshold value of tx Bias Current in mA.
        txbiashighwarning          |FLOAT          |High Warning Threshold value of tx Bias Current in mA.
        txbiaslowwarning           |FLOAT          |Low Warning Threshold value of tx Bias Current in mA.
        ========================================================================
        """
        transceiver_dom_threshold_info_dict = dict.fromkeys(
            threshold_dict_keys, NULL_VAL)

        if not self.get_presence():
            return transceiver_dom_threshold_info_dict
        if not self._detect_sfp_type():
            return transceiver_dom_threshold_info_dict
        self._dom_capability_detect(check_presence=False)

        if self.sfp_type == OSFP_TYPE:
            pass

        elif self.sfp_type == QSFP_TYPE:
            if not self.dom_supported or not self.qsfp_page3_available:
                return transceiver_dom_threshold_info_dict

            # Dom Threshold data starts from offset 384
            # Revert offset back to 0 once data is retrieved
            offset = QSFP_MODULE_UPPER_PAGE3_START
            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return transceiver_dom_threshold_info_dict

            dom_module_threshold_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_MODULE_THRESHOLD_OFFSET), QSFP_MODULE_THRESHOLD_WIDTH)
            if dom_module_threshold_raw is None:
                return transceiver_dom_threshold_info_dict

            dom_module_threshold_data = sfpd_obj.parse_module_threshold_values(
                dom_module_threshold_raw, 0)

            dom_channel_threshold_raw = self._read_eeprom_specific_bytes((offset + QSFP_CHANNL_THRESHOLD_OFFSET),
                                                                         QSFP_CHANNL_THRESHOLD_WIDTH)
            if dom_channel_threshold_raw is None:
                return transceiver_dom_threshold_info_dict
            dom_channel_threshold_data = sfpd_obj.parse_channel_threshold_values(
                dom_channel_threshold_raw, 0)

            # Threshold Data
            transceiver_dom_threshold_info_dict['temphighalarm'] = dom_module_threshold_data['data']['TempHighAlarm']['value']
            transceiver_dom_threshold_info_dict['temphighwarning'] = dom_module_threshold_data['data']['TempHighWarning']['value']
            transceiver_dom_threshold_info_dict['templowalarm'] = dom_module_threshold_data['data']['TempLowAlarm']['value']
            transceiver_dom_threshold_info_dict['templowwarning'] = dom_module_threshold_data['data']['TempLowWarning']['value']
            transceiver_dom_threshold_info_dict['vcchighalarm'] = dom_module_threshold_data['data']['VccHighAlarm']['value']
            transceiver_dom_threshold_info_dict['vcchighwarning'] = dom_module_threshold_data['data']['VccHighWarning']['value']
            transceiver_dom_threshold_info_dict['vcclowalarm'] = dom_module_threshold_data['data']['VccLowAlarm']['value']
            transceiver_dom_threshold_info_dict['vcclowwarning'] = dom_module_threshold_data['data']['VccLowWarning']['value']
            transceiver_dom_threshold_info_dict['rxpowerhighalarm'] = dom_channel_threshold_data['data']['RxPowerHighAlarm']['value']
            transceiver_dom_threshold_info_dict['rxpowerhighwarning'] = dom_channel_threshold_data['data']['RxPowerHighWarning']['value']
            transceiver_dom_threshold_info_dict['rxpowerlowalarm'] = dom_channel_threshold_data['data']['RxPowerLowAlarm']['value']
            transceiver_dom_threshold_info_dict['rxpowerlowwarning'] = dom_channel_threshold_data['data']['RxPowerLowWarning']['value']
            transceiver_dom_threshold_info_dict['txbiashighalarm'] = dom_channel_threshold_data['data']['TxBiasHighAlarm']['value']
            transceiver_dom_threshold_info_dict['txbiashighwarning'] = dom_channel_threshold_data['data']['TxBiasHighWarning']['value']
            transceiver_dom_threshold_info_dict['txbiaslowalarm'] = dom_channel_threshold_data['data']['TxBiasLowAlarm']['value']
            transceiver_dom_threshold_info_dict['txbiaslowwarning'] = dom_channel_threshold_data['data']['TxBiasLowWarning']['value']
            transceiver_dom_threshold_info_dict['txpowerhighalarm'] = dom_channel_threshold_data['data']['TxPowerHighAlarm']['value']
            transceiver_dom_threshold_info_dict['txpowerhighwarning'] = dom_channel_threshold_data['data']['TxPowerHighWarning']['value']
            transceiver_dom_threshold_info_dict['txpowerlowalarm'] = dom_channel_threshold_data['data']['TxPowerLowAlarm']['value']
            transceiver_dom_threshold_info_dict['txpowerlowwarning'] = dom_channel_threshold_data['data']['TxPowerLowWarning']['value']

        elif self.sfp_type == QSFP_DD_TYPE:
            if not self.dom_supported:
                return transceiver_dom_threshold_info_dict

            if not self.dom_thresholds_supported:
                return transceiver_dom_threshold_info_dict

            sfpd_obj = qsfp_dd_Dom()
            if sfpd_obj is None:
                return transceiver_dom_threshold_info_dict

            # page 02
            offset = 384
            dom_module_threshold_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_MODULE_THRESHOLD_OFFSET), QSFP_DD_MODULE_THRESHOLD_WIDTH)
            if dom_module_threshold_raw is None:
                return transceiver_dom_threshold_info_dict

            dom_module_threshold_data = sfpd_obj.parse_module_threshold_values(
                dom_module_threshold_raw, 0)

            # Threshold Data
            transceiver_dom_threshold_info_dict['temphighalarm'] = dom_module_threshold_data['data']['TempHighAlarm']['value']
            transceiver_dom_threshold_info_dict['temphighwarning'] = dom_module_threshold_data['data']['TempHighWarning']['value']
            transceiver_dom_threshold_info_dict['templowalarm'] = dom_module_threshold_data['data']['TempLowAlarm']['value']
            transceiver_dom_threshold_info_dict['templowwarning'] = dom_module_threshold_data['data']['TempLowWarning']['value']
            transceiver_dom_threshold_info_dict['vcchighalarm'] = dom_module_threshold_data['data']['VccHighAlarm']['value']
            transceiver_dom_threshold_info_dict['vcchighwarning'] = dom_module_threshold_data['data']['VccHighWarning']['value']
            transceiver_dom_threshold_info_dict['vcclowalarm'] = dom_module_threshold_data['data']['VccLowAlarm']['value']
            transceiver_dom_threshold_info_dict['vcclowwarning'] = dom_module_threshold_data['data']['VccLowWarning']['value']
            transceiver_dom_threshold_info_dict['rxpowerhighalarm'] = dom_module_threshold_data['data']['RxPowerHighAlarm']['value']
            transceiver_dom_threshold_info_dict['rxpowerhighwarning'] = dom_module_threshold_data['data']['RxPowerHighWarning']['value']
            transceiver_dom_threshold_info_dict['rxpowerlowalarm'] = dom_module_threshold_data['data']['RxPowerLowAlarm']['value']
            transceiver_dom_threshold_info_dict['rxpowerlowwarning'] = dom_module_threshold_data['data']['RxPowerLowWarning']['value']
            transceiver_dom_threshold_info_dict['txbiashighalarm'] = dom_module_threshold_data['data']['TxBiasHighAlarm']['value']
            transceiver_dom_threshold_info_dict['txbiashighwarning'] = dom_module_threshold_data['data']['TxBiasHighWarning']['value']
            transceiver_dom_threshold_info_dict['txbiaslowalarm'] = dom_module_threshold_data['data']['TxBiasLowAlarm']['value']
            transceiver_dom_threshold_info_dict['txbiaslowwarning'] = dom_module_threshold_data['data']['TxBiasLowWarning']['value']
            transceiver_dom_threshold_info_dict['txpowerhighalarm'] = dom_module_threshold_data['data']['TxPowerHighAlarm']['value']
            transceiver_dom_threshold_info_dict['txpowerhighwarning'] = dom_module_threshold_data['data']['TxPowerHighWarning']['value']
            transceiver_dom_threshold_info_dict['txpowerlowalarm'] = dom_module_threshold_data['data']['TxPowerLowAlarm']['value']
            transceiver_dom_threshold_info_dict['txpowerlowwarning'] = dom_module_threshold_data['data']['TxPowerLowWarning']['value']

        else:
            offset = SFP_MODULE_ADDRA2_OFFSET

            if not self.dom_supported:
                return transceiver_dom_threshold_info_dict

            sfpd_obj = sff8472Dom(None, self.calibration)
            if sfpd_obj is None:
                return transceiver_dom_threshold_info_dict

            dom_module_threshold_raw = self._read_eeprom_specific_bytes((offset + SFP_MODULE_THRESHOLD_OFFSET),
                                                                        SFP_MODULE_THRESHOLD_WIDTH)
            if dom_module_threshold_raw is not None:
                dom_module_threshold_data = sfpd_obj.parse_alarm_warning_threshold(
                    dom_module_threshold_raw, 0)
            else:
                return transceiver_dom_threshold_info_dict

            # Threshold Data
            transceiver_dom_threshold_info_dict['temphighalarm'] = dom_module_threshold_data['data']['TempHighAlarm']['value']
            transceiver_dom_threshold_info_dict['templowalarm'] = dom_module_threshold_data['data']['TempLowAlarm']['value']
            transceiver_dom_threshold_info_dict['temphighwarning'] = dom_module_threshold_data['data']['TempHighWarning']['value']
            transceiver_dom_threshold_info_dict['templowwarning'] = dom_module_threshold_data['data']['TempLowWarning']['value']
            transceiver_dom_threshold_info_dict['vcchighalarm'] = dom_module_threshold_data['data']['VoltageHighAlarm']['value']
            transceiver_dom_threshold_info_dict['vcclowalarm'] = dom_module_threshold_data['data']['VoltageLowAlarm']['value']
            transceiver_dom_threshold_info_dict['vcchighwarning'] = dom_module_threshold_data[
                'data']['VoltageHighWarning']['value']
            transceiver_dom_threshold_info_dict['vcclowwarning'] = dom_module_threshold_data['data']['VoltageLowWarning']['value']
            transceiver_dom_threshold_info_dict['txbiashighalarm'] = dom_module_threshold_data['data']['BiasHighAlarm']['value']
            transceiver_dom_threshold_info_dict['txbiaslowalarm'] = dom_module_threshold_data['data']['BiasLowAlarm']['value']
            transceiver_dom_threshold_info_dict['txbiashighwarning'] = dom_module_threshold_data['data']['BiasHighWarning']['value']
            transceiver_dom_threshold_info_dict['txbiaslowwarning'] = dom_module_threshold_data['data']['BiasLowWarning']['value']
            transceiver_dom_threshold_info_dict['txpowerhighalarm'] = dom_module_threshold_data['data']['TXPowerHighAlarm']['value']
            transceiver_dom_threshold_info_dict['txpowerlowalarm'] = dom_module_threshold_data['data']['TXPowerLowAlarm']['value']
            transceiver_dom_threshold_info_dict['txpowerhighwarning'] = dom_module_threshold_data['data']['TXPowerHighWarning']['value']
            transceiver_dom_threshold_info_dict['txpowerlowwarning'] = dom_module_threshold_data['data']['TXPowerLowWarning']['value']
            transceiver_dom_threshold_info_dict['rxpowerhighalarm'] = dom_module_threshold_data['data']['RXPowerHighAlarm']['value']
            transceiver_dom_threshold_info_dict['rxpowerlowalarm'] = dom_module_threshold_data['data']['RXPowerLowAlarm']['value']
            transceiver_dom_threshold_info_dict['rxpowerhighwarning'] = dom_module_threshold_data['data']['RXPowerHighWarning']['value']
            transceiver_dom_threshold_info_dict['rxpowerlowwarning'] = dom_module_threshold_data['data']['RXPowerLowWarning']['value']

        for key in transceiver_dom_threshold_info_dict:
            transceiver_dom_threshold_info_dict[key] = self._convert_string_to_num(
                transceiver_dom_threshold_info_dict[key])

        return transceiver_dom_threshold_info_dict

    def get_reset_status(self):
        """
        Retrieves the reset status of SFP
        Returns:
            A Boolean, True if reset enabled, False if disabled
        """
        if self.port_type != QSFP_DD_TYPE:
            return False

        try:
            reg_file = open(
                "/".join([PORT_INFO_PATH, self.port_name, "qsfp_reset"]))
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        # Read status
        content = reg_file.readline().rstrip()
        reg_value = int(content)
        # reset is active low
        if reg_value == 0:
            return True

        return False

    def get_rx_los(self):
        """
        Retrieves the RX LOS (lost-of-signal) status of SFP
        Returns:
            A Boolean, True if SFP has RX LOS, False if not.
            Note : RX LOS status is latched until a call to get_rx_los or a reset.
        """
        if not self.get_presence():
            return None
        if not self._detect_sfp_type():
            return None
        self._dom_capability_detect(check_presence=False)
        rx_los_list = []

        if self.sfp_type == OSFP_TYPE:
            return None
        elif self.sfp_type == QSFP_TYPE:
            offset = 0
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_CHANNL_RX_LOS_STATUS_OFFSET),
                QSFP_CHANNL_RX_LOS_STATUS_WIDTH)
            if dom_channel_monitor_raw is not None:
                rx_los_data = int(dom_channel_monitor_raw[0], 16)
                rx_los_list.append(rx_los_data & 0x01 != 0)
                rx_los_list.append(rx_los_data & 0x02 != 0)
                rx_los_list.append(rx_los_data & 0x04 != 0)
                rx_los_list.append(rx_los_data & 0x08 != 0)
            else:
                return [False] * 4

        elif self.sfp_type == QSFP_DD_TYPE:
            if not self.dom_supported:
                return None

            offset = QSFP_DD_RX_FLAGS_ADVT_PAGE * 128
            advt_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_RX_FLAGS_ADVT_OFFSET),
                QSFP_DD_RX_FLAGS_ADVT_WIDTH)
            if advt_raw is None:
                return None
            advt_data = int(advt_raw[0], 16)
            rx_los_support = (advt_data & 0x01 != 0)
            if not rx_los_support:
                return [False for _ in range(self.NUM_CHANNELS)]

            offset = QSFP_DD_RX_LOS_PAGE * 128
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_RX_LOS_OFFSET),
                QSFP_DD_RX_LOS_WIDTH)
            if dom_channel_monitor_raw is None:
                return None
            rx_los_data = int(dom_channel_monitor_raw[0], 16)
            rx_los_list.append(rx_los_data & 0x01 != 0)
            rx_los_list.append(rx_los_data & 0x02 != 0)
            rx_los_list.append(rx_los_data & 0x04 != 0)
            rx_los_list.append(rx_los_data & 0x08 != 0)
            rx_los_list.append(rx_los_data & 0x10 != 0)
            rx_los_list.append(rx_los_data & 0x20 != 0)
            rx_los_list.append(rx_los_data & 0x40 != 0)
            rx_los_list.append(rx_los_data & 0x80 != 0)

        else:
            offset = 256
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + SFP_CHANNL_STATUS_OFFSET), SFP_CHANNL_STATUS_WIDTH)
            if dom_channel_monitor_raw is not None:
                rx_los_data = int(dom_channel_monitor_raw[0], 16)
                rx_los_list.append(rx_los_data & 0x02 != 0)
            else:
                return [False]
        return rx_los_list

    def get_tx_fault(self):
        """
        Retrieves the TX fault status of SFP
        Returns:
            A Boolean, True if SFP has TX fault, False if not
            Note : TX fault status is lached until a call to get_tx_fault or a reset.
        """
        if not self._detect_sfp_type():
            return None

        tx_fault_list = []

        if self.sfp_type == OSFP_TYPE:
            return None
        elif self.sfp_type == QSFP_TYPE:
            offset = 0
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_CHANNL_TX_FAULT_STATUS_OFFSET),
                QSFP_CHANNL_TX_FAULT_STATUS_WIDTH)
            if dom_channel_monitor_raw is not None:
                tx_fault_data = int(dom_channel_monitor_raw[0], 16)
                tx_fault_list.append(tx_fault_data & 0x01 != 0)
                tx_fault_list.append(tx_fault_data & 0x02 != 0)
                tx_fault_list.append(tx_fault_data & 0x04 != 0)
                tx_fault_list.append(tx_fault_data & 0x08 != 0)
            else:
                return [False] * 4
        elif self.sfp_type == QSFP_DD_TYPE:
            if not self.dom_supported:
                return None

            offset = QSFP_DD_TX_FLAGS_ADVT_PAGE * 128
            advt_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_TX_FLAGS_ADVT_OFFSET),
                QSFP_DD_TX_FLAGS_ADVT_WIDTH)
            if advt_raw is None:
                return None
            advt_data = int(advt_raw[0], 16)
            tx_fault_support = (advt_data & 0x01 != 0)
            if not tx_fault_support:
                return [False for _ in range(self.NUM_CHANNELS)]

            offset = QSFP_DD_TX_FAULT_PAGE * 128
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_TX_FAULT_OFFSET),
                QSFP_DD_TX_FAULT_WIDTH)
            if dom_channel_monitor_raw is None:
                return None
            tx_fault_data = int(dom_channel_monitor_raw[0], 16)
            tx_fault_list.append(tx_fault_data & 0x01 != 0)
            tx_fault_list.append(tx_fault_data & 0x02 != 0)
            tx_fault_list.append(tx_fault_data & 0x04 != 0)
            tx_fault_list.append(tx_fault_data & 0x08 != 0)
            tx_fault_list.append(tx_fault_data & 0x10 != 0)
            tx_fault_list.append(tx_fault_data & 0x20 != 0)
            tx_fault_list.append(tx_fault_data & 0x40 != 0)
            tx_fault_list.append(tx_fault_data & 0x80 != 0)

        else:
            offset = 256
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + SFP_CHANNL_STATUS_OFFSET), SFP_CHANNL_STATUS_WIDTH)
            if dom_channel_monitor_raw is not None:
                tx_fault_data = int(dom_channel_monitor_raw[0], 16)
                tx_fault_list.append(tx_fault_data & 0x04 != 0)
            else:
                return None
        return tx_fault_list

    def get_tx_disable(self):
        """
        Retrieves the tx_disable status of this SFP
        Returns:
            A list of boolean values, representing the TX disable status
            of each available channel, value is True if SFP channel
            is TX disabled, False if not.
            E.g., for a tranceiver with four channels: [False, False, True, False]
        """
        if not self._detect_sfp_type():
            return None

        tx_disable_list = []
        if self.sfp_type == OSFP_TYPE:
            return None
        elif self.sfp_type == QSFP_TYPE:
            offset = 0
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_CHANNL_DISABLE_STATUS_OFFSET),
                QSFP_CHANNL_DISABLE_STATUS_WIDTH)
            if dom_channel_monitor_raw is not None:
                tx_disable_data = int(dom_channel_monitor_raw[0], 16)
                tx_disable_list.append(tx_disable_data & 0x01 != 0)
                tx_disable_list.append(tx_disable_data & 0x02 != 0)
                tx_disable_list.append(tx_disable_data & 0x04 != 0)
                tx_disable_list.append(tx_disable_data & 0x08 != 0)
            else:
                return [False] * 4

        elif self.sfp_type == QSFP_DD_TYPE:
            if not self.dom_supported:
                return None

            offset = QSFP_DD_CTRLS_ADVT_PAGE * 128
            advt_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_CTRLS_ADVT_OFFSET),
                QSFP_DD_CTRLS_ADVT_WIDTH)
            if advt_raw is None:
                return None
            advt_data = int(advt_raw[0], 16)
            tx_disable_support = (advt_data & 0x02 != 0)
            if not tx_disable_support:
                return ["N/A" for _ in range(self.NUM_CHANNELS)]

            offset = QSFP_DD_TX_DISABLE_PAGE * 128
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_DD_TX_DISABLE_OFFSET),
                QSFP_DD_TX_DISABLE_WIDTH)
            if dom_channel_monitor_raw is None:
                return None
            tx_disable_data = int(dom_channel_monitor_raw[0], 16)
            tx_disable_list.append(tx_disable_data & 0x01 != 0)
            tx_disable_list.append(tx_disable_data & 0x02 != 0)
            tx_disable_list.append(tx_disable_data & 0x04 != 0)
            tx_disable_list.append(tx_disable_data & 0x08 != 0)
            tx_disable_list.append(tx_disable_data & 0x10 != 0)
            tx_disable_list.append(tx_disable_data & 0x20 != 0)
            tx_disable_list.append(tx_disable_data & 0x40 != 0)
            tx_disable_list.append(tx_disable_data & 0x80 != 0)

        else:
            offset = 256
            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + SFP_CHANNL_STATUS_OFFSET), SFP_CHANNL_STATUS_WIDTH)
            if dom_channel_monitor_raw is not None:
                tx_disable_data = int(dom_channel_monitor_raw[0], 16)
                tx_disable_list.append(tx_disable_data & 0xC0 != 0)
            else:
                return [False]
        return tx_disable_list

    def get_tx_disable_channel(self):
        """
        Retrieves the TX disabled channels in this SFP
        Returns:
            A hex of 4 bits (bit 0 to bit 3 as channel 0 to channel 3) to represent
            TX channels which have been disabled in this SFP.
            As an example, a returned value of 0x5 indicates that channel 0 
            and channel 2 have been disabled.
        """
        tx_disable_list = self.get_tx_disable()
        if tx_disable_list is None:
            return None
        if tx_disable_list[0] == "N/A":
            return "N/A"
        tx_disabled = 0
        for i in range(len(tx_disable_list)):
            if tx_disable_list[i]:
                tx_disabled |= 1 << i
        return tx_disabled

    def get_lpmode(self):
        """
        Retrieves the lpmode (low power mode) status of this SFP
        Returns:
            A Boolean, True if lpmode is enabled, False if disabled
        """
        if self.port_type != QSFP_DD_TYPE:
            return False

        try:
            reg_file = open(
                "/".join([PORT_INFO_PATH, self.port_name, "qsfp_lpmode"]))
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        # Read status
        content = reg_file.readline().rstrip()
        reg_value = int(content)
        # low power mode is active high
        if reg_value == 0:
            return False

        return True

    def get_power_override(self):
        """
        Retrieves the power-override status of this SFP
        Returns:
            A Boolean, True if power-override is enabled, False if disabled
        """
        if not self._detect_sfp_type():
            return False

        if self.sfp_type == QSFP_TYPE:
            offset = 0
            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return False

            dom_control_raw = self._read_eeprom_specific_bytes(
                QSFP_CONTROL_OFFSET, QSFP_CONTROL_WIDTH) if self.get_presence() else None
            if dom_control_raw is not None:
                dom_control_data = sfpd_obj.parse_control_bytes(
                    dom_control_raw, 0)
                return ('On' == dom_control_data['data']['PowerOverride']['value'])
            else:
                return False
        else:
            return False

    def get_temperature(self):
        """
        Retrieves the temperature of this SFP
        Returns:
            An integer number of current temperature in Celsius
        """
        default = 0.0
        self._dom_capability_detect()
        if not self.dom_supported:
            return default

        if self.sfp_type == QSFP_TYPE:
            offset = 0

            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return default

            if self.dom_temp_supported:
                dom_temperature_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_TEMPE_OFFSET), QSFP_TEMPE_WIDTH)
                if dom_temperature_raw is not None:
                    dom_temperature_data = sfpd_obj.parse_temperature(
                        dom_temperature_raw, 0)
                    temp = self._convert_string_to_num(
                        dom_temperature_data['data']['Temperature']['value'])
                    return temp

        elif self.sfp_type == QSFP_DD_TYPE:
            offset = 0

            sfpd_obj = qsfp_dd_Dom()
            if sfpd_obj is None:
                return default

            if self.dom_temp_supported:
                dom_temperature_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_DD_TEMPE_OFFSET), QSFP_DD_TEMPE_WIDTH)
                if dom_temperature_raw is not None:
                    dom_temperature_data = sfpd_obj.parse_temperature(
                        dom_temperature_raw, 0)
                    temp = self._convert_string_to_num(
                        dom_temperature_data['data']['Temperature']['value'])
                    return temp

        else:
            offset = 256
            sfpd_obj = sff8472Dom()
            if sfpd_obj is None:
                return default
            sfpd_obj._calibration_type = 1

            dom_temperature_raw = self._read_eeprom_specific_bytes(
                (offset + SFP_TEMPE_OFFSET), SFP_TEMPE_WIDTH)
            if dom_temperature_raw is not None:
                dom_temperature_data = sfpd_obj.parse_temperature(
                    dom_temperature_raw, 0)
                temp = self._convert_string_to_num(
                    dom_temperature_data['data']['Temperature']['value'])
                return temp

        return default

    def get_voltage(self):
        """
        Retrieves the supply voltage of this SFP
        Returns:
            An integer number of supply voltage in mV
        """
        default = 0.0
        if not self._detect_sfp_type():
            return default
        if not self.dom_supported:
            return default

        if self.sfp_type == QSFP_TYPE:
            offset = 0
            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return default

            if self.dom_volt_supported:
                dom_voltage_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_VOLT_OFFSET), QSFP_VOLT_WIDTH)
                if dom_voltage_raw is not None:
                    dom_voltage_data = sfpd_obj.parse_voltage(
                        dom_voltage_raw, 0)
                    voltage = self._convert_string_to_num(
                        dom_voltage_data['data']['Vcc']['value'])
                    return voltage

        if self.sfp_type == QSFP_DD_TYPE:
            offset = 0

            sfpd_obj = qsfp_dd_Dom()
            if sfpd_obj is None:
                return default

            if self.dom_volt_supported:
                dom_voltage_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_DD_VOLT_OFFSET), QSFP_DD_VOLT_WIDTH)
                if dom_voltage_raw is not None:
                    dom_voltage_data = sfpd_obj.parse_voltage(
                        dom_voltage_raw, 0)
                    voltage = self._convert_string_to_num(
                        dom_voltage_data['data']['Vcc']['value'])
                    return voltage

        else:
            offset = 256

            sfpd_obj = sff8472Dom()
            if sfpd_obj is None:
                return default

            sfpd_obj._calibration_type = self.calibration

            dom_voltage_raw = self._read_eeprom_specific_bytes(
                (offset + SFP_VOLT_OFFSET), SFP_VOLT_WIDTH)
            if dom_voltage_raw is not None:
                dom_voltage_data = sfpd_obj.parse_voltage(dom_voltage_raw, 0)
                voltage = self._convert_string_to_num(
                    dom_voltage_data['data']['Vcc']['value'])
                return voltage

        return default

    def get_tx_bias(self):
        """
        Retrieves the TX bias current of this SFP
        Returns:
            A list of four integer numbers, representing TX bias in mA
            for channel 0 to channel 4.
            Ex. ['110.09', '111.12', '108.21', '112.09']
        """
        if not self._detect_sfp_type():
            return []

        tx_bias_list = []
        if self.sfp_type == QSFP_TYPE:
            offset = 0
            default = [0.0] * 4
            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return default

            dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                (offset + QSFP_CHANNL_MON_OFFSET), QSFP_CHANNL_MON_WITH_TX_POWER_WIDTH)
            if dom_channel_monitor_raw is not None:
                dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params_with_tx_power(
                    dom_channel_monitor_raw, 0)
                tx_bias_list.append(self._convert_string_to_num(
                    dom_channel_monitor_data['data']['TX1Bias']['value']))
                tx_bias_list.append(self._convert_string_to_num(
                    dom_channel_monitor_data['data']['TX2Bias']['value']))
                tx_bias_list.append(self._convert_string_to_num(
                    dom_channel_monitor_data['data']['TX3Bias']['value']))
                tx_bias_list.append(self._convert_string_to_num(
                    dom_channel_monitor_data['data']['TX4Bias']['value']))
            else:
                return default

        elif self.sfp_type == QSFP_DD_TYPE:
            default = [0.0] * 8
            offset = 128
            sfpd_obj = qsfp_dd_Dom()
            if sfpd_obj is None:
                return default

            if self.dom_tx_bias_power_supported:
                dom_tx_bias_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_DD_TX_BIAS_OFFSET), QSFP_DD_TX_BIAS_WIDTH)
                if dom_tx_bias_raw is not None:
                    dom_tx_bias_data = sfpd_obj.parse_dom_tx_bias(
                        dom_tx_bias_raw, 0)
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX1Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX2Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX3Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX4Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX5Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX6Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX7Bias']['value']))
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_tx_bias_data['data']['TX8Bias']['value']))
                else:
                    return default
            else:
                return default

        else:
            offset = 256
            default = [0.0]
            sfpd_obj = sff8472Dom()
            if sfpd_obj is None:
                return default
            sfpd_obj._calibration_type = self.calibration

            if self.dom_supported:
                dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                    (offset + SFP_CHANNL_MON_OFFSET), SFP_CHANNL_MON_WIDTH)
                if dom_channel_monitor_raw is not None:
                    dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params(
                        dom_channel_monitor_raw, 0)
                    tx_bias_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['TXBias']['value']))
                else:
                    return default
            else:
                return default

        return tx_bias_list

    def get_rx_power(self):
        """
        Retrieves the received optical power for this SFP
        Returns:
            A list of four integer numbers, representing received optical
            power in mW for channel 0 to channel 4.
            Ex. ['1.77', '1.71', '1.68', '1.70']
        """
        if not self._detect_sfp_type():
            return []

        rx_power_list = []
        if self.sfp_type == OSFP_TYPE:
            # OSFP not supported on our platform yet.
            return None

        elif self.sfp_type == QSFP_TYPE:
            offset = 0
            default = [0.0] * 4
            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return default

            if self.dom_rx_power_supported:
                dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_CHANNL_MON_OFFSET), QSFP_CHANNL_MON_WITH_TX_POWER_WIDTH)
                if dom_channel_monitor_raw is not None:
                    dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params_with_tx_power(
                        dom_channel_monitor_raw, 0)
                    rx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['RX1Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['RX2Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['RX3Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['RX4Power']['value']))
                else:
                    return default
            else:
                return default

        elif self.sfp_type == QSFP_DD_TYPE:
            default = [0.0] * 8
            if self.dom_rx_power_supported:
                offset = QSFP_DD_RX_POWER_PAGE * 128
                sfpd_obj = qsfp_dd_Dom()
                if sfpd_obj is None:
                    return default

                dom_rx_power_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_DD_RX_POWER_OFFSET), QSFP_DD_RX_POWER_WIDTH)
                if dom_rx_power_raw is not None:
                    dom_rx_power_data = sfpd_obj.parse_dom_rx_power(
                        dom_rx_power_raw, 0)
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX1Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX2Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX3Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX4Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX5Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX6Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX7Power']['value']))
                    rx_power_list.append(self._convert_string_to_num(
                        dom_rx_power_data['data']['RX8Power']['value']))
                else:
                    return default

        else:
            offset = 256
            default = [0.0]
            sfpd_obj = sff8472Dom()
            if sfpd_obj is None:
                return default

            if self.dom_supported:
                sfpd_obj._calibration_type = self.calibration

                dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                    (offset + SFP_CHANNL_MON_OFFSET), SFP_CHANNL_MON_WIDTH)
                if dom_channel_monitor_raw is not None:
                    dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params(
                        dom_channel_monitor_raw, 0)
                    rx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['RXPower']['value']))
                else:
                    return default
            else:
                return default
        return rx_power_list

    def get_tx_power(self):
        """
        Retrieves the TX power of this SFP
        Returns:
            A list of four integer numbers, representing TX power in mW
            for channel 0 to channel 4.
            Ex. ['1.86', '1.86', '1.86', '1.86']
        """
        if not self._detect_sfp_type():
            return []

        tx_power_list = []
        if self.sfp_type == OSFP_TYPE:
            # OSFP not supported on our platform yet.
            return tx_power_list

        elif self.sfp_type == QSFP_TYPE:
            offset = 0
            default = [0.0] * 4

            sfpd_obj = sff8436Dom()
            if sfpd_obj is None:
                return tx_power_list

            if self.dom_tx_power_supported:
                dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_CHANNL_MON_OFFSET),
                    QSFP_CHANNL_MON_WITH_TX_POWER_WIDTH)
                if dom_channel_monitor_raw is not None:
                    dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params_with_tx_power(
                        dom_channel_monitor_raw, 0)
                    tx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['TX1Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['TX2Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['TX3Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['TX4Power']['value']))
                else:
                    return default
            else:
                return default

        elif self.sfp_type == QSFP_DD_TYPE:
            default = [0.0] * 8

            # page 11
            if self.dom_tx_power_supported:
                offset = QSFP_DD_TX_POWER_PAGE * 128
                sfpd_obj = qsfp_dd_Dom()
                if sfpd_obj is None:
                    return default

                dom_tx_power_raw = self._read_eeprom_specific_bytes(
                    (offset + QSFP_DD_TX_POWER_OFFSET),
                    QSFP_DD_TX_POWER_WIDTH)
                if dom_tx_power_raw is not None:
                    dom_tx_power_data = sfpd_obj.parse_dom_tx_power(
                        dom_tx_power_raw, 0)
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX1Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX2Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX3Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX4Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX5Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX6Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX7Power']['value']))
                    tx_power_list.append(self._convert_string_to_num(
                        dom_tx_power_data['data']['TX8Power']['value']))
                else:
                    return default

        else:
            offset = 256
            default = [0.0]
            sfpd_obj = sff8472Dom()
            if sfpd_obj is None:
                return default

            if self.dom_supported:
                sfpd_obj._calibration_type = self.calibration

                dom_channel_monitor_raw = self._read_eeprom_specific_bytes(
                    (offset + SFP_CHANNL_MON_OFFSET), SFP_CHANNL_MON_WIDTH)
                if dom_channel_monitor_raw is not None:
                    dom_channel_monitor_data = sfpd_obj.parse_channel_monitor_params(
                        dom_channel_monitor_raw, 0)
                    tx_power_list.append(self._convert_string_to_num(
                        dom_channel_monitor_data['data']['TXPower']['value']))
                else:
                    return default
            else:
                return default
        return tx_power_list

    def reset(self):
        """
        Reset SFP and return all user module settings to their default srate.
        Returns:
            A boolean, True if successful, False if not
        """
        if self.port_type != QSFP_DD_TYPE:
            return False

        try:
            reg_file = open(
                "/".join([PORT_INFO_PATH, self.port_name, "qsfp_reset"]), "w")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        # Convert our register value back to a hex string and write back
        reg_file.seek(0)
        reg_file.write(hex(0))
        reg_file.close()

        # Sleep 1 second to allow it to settle
        time.sleep(1)

        # Flip the bit back high and write back to the register to take port out of reset
        try:
            reg_file = open(
                "/".join([PORT_INFO_PATH, self.port_name, "qsfp_reset"]), "w")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        reg_file.seek(0)
        reg_file.write(hex(1))
        reg_file.close()

        return True

    def no_reset(self):
        """
        Set CPLD qsfp_reset to 1 for non-reset status.
        Returns:
            A boolean, True if successful, False if not
        """
        if self.port_type != QSFP_DD_TYPE:
            return False

        try:
            reg_file = open(
                "/".join([PORT_INFO_PATH, self.port_name, "qsfp_reset"]), "w")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        reg_file.seek(0)
        reg_file.write(hex(1))
        reg_file.close()

        return True

    def tx_disable(self, tx_disable):
        """
        Disable SFP TX for all channels
        Args:
            tx_disable : A Boolean, True to enable tx_disable mode, False to disable
                         tx_disable mode.
        Returns:
            A boolean, True if tx_disable is set successfully, False if not
        """
        if not self._detect_sfp_type():
            return False

        if self.sfp_type == QSFP_DD_TYPE:
            sysfsfile_eeprom = None
            try:
                tx_disable_value = 0xff if tx_disable else 0x0
                # Write to eeprom
                sysfsfile_eeprom = open(self._eeprom_path, "r+b")
                sysfsfile_eeprom.seek(QSFP_DD_TX_DISABLE_PAGE*128 + QSFP_DD_TX_DISABLE_OFFSET)
                sysfsfile_eeprom.write(struct.pack('B', tx_disable_value))
            except IOError:
                return False
            finally:
                if sysfsfile_eeprom is not None:
                    try:
                        sysfsfile_eeprom.close()
                    except:
                        return False
                    time.sleep(0.01)
            return True
        elif self.sfp_type == QSFP_TYPE:
            sysfsfile_eeprom = None
            try:
                tx_disable_value = 0xf if tx_disable else 0x0
                # Write to eeprom
                sysfsfile_eeprom = open(self._eeprom_path, "r+b")
                sysfsfile_eeprom.seek(QSFP_CONTROL_OFFSET)
                sysfsfile_eeprom.write(struct.pack('B', tx_disable_value))
            except IOError:
                return False
            finally:
                if sysfsfile_eeprom is not None:
                    try:
                        sysfsfile_eeprom.close()
                    except:
                        return False
                    time.sleep(0.01)
            return True
        elif self.port_type == SFP_TYPE:
            try:
                reg_file = open(
                    "/".join([PORT_INFO_PATH, self.port_name, "sfp_txdisable"]), "w")
            except IOError as e:
                print("Error: unable to open file: %s" % str(e))
                return False

            reg_file.seek(0)
            reg_file.write(hex(tx_disable))
            reg_file.close()
            return True

        return False

    def tx_disable_channel(self, channel, disable):
        """
        Sets the tx_disable for specified SFP channels
        Args:
            channel : A hex of 4 bits (bit 0 to bit 3) which represent channel 0 to 3,
                      e.g. 0x5 for channel 0 and channel 2.
            disable : A boolean, True to disable TX channels specified in channel,
                      False to enable
        Returns:
            A boolean, True if successful, False if not
        """
        if not self._detect_sfp_type():
            return False

        if self.sfp_type == QSFP_DD_TYPE:
            sysfsfile_eeprom = None
            try:
                current_state = self.get_tx_disable_channel()
                tx_disable_value = (current_state | channel) if \
                    disable else (current_state & (~channel))

                    # Write to eeprom
                sysfsfile_eeprom = open(self._eeprom_path, "r+b")
                sysfsfile_eeprom.seek(0x10*128 + QSFP_DD_TX_DISABLE_OFFSET)
                sysfsfile_eeprom.write(struct.pack('B', tx_disable_value))
            except IOError:
                return False
            finally:
                if sysfsfile_eeprom is not None:
                    try:
                        sysfsfile_eeprom.close()
                    except:
                        return False
                    time.sleep(0.01)
            return True
        elif self.sfp_type == QSFP_TYPE:
            sysfsfile_eeprom = None
            try:
                current_state = self.get_tx_disable_channel()
                tx_disable_value = (current_state | channel) if \
                    disable else (current_state & (~channel))

                # Write to eeprom
                sysfsfile_eeprom = open(self._eeprom_path, "r+b")
                sysfsfile_eeprom.seek(QSFP_CONTROL_OFFSET)
                sysfsfile_eeprom.write(struct.pack('B', tx_disable_value))
            except IOError:
                return False
            finally:
                if sysfsfile_eeprom is not None:
                    try:
                        sysfsfile_eeprom.close()
                    except:
                        return False
                    time.sleep(0.01)
            return True
        return False

    def set_lpmode(self, lpmode):
        """
        Sets the lpmode (low power mode) of SFP
        Args:
            lpmode: A Boolean, True to enable lpmode, False to disable it
            Note  : lpmode can be overridden by set_power_override
        Returns:
            A boolean, True if lpmode is set successfully, False if not
        """
        if not self._detect_sfp_type():
            return False

        if self.port_type != QSFP_DD_TYPE:
            return False

        try:
            reg_file = open(
                "/".join([PORT_INFO_PATH, self.port_name, "qsfp_lpmode"]), "r+")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        content = hex(lpmode)

        reg_file.seek(0)
        reg_file.write(content)
        reg_file.close()

        return True

    def set_power_override(self, power_override, power_set):
        """
        Sets SFP power level using power_override and power_set
        Args:
            power_override :
                    A Boolean, True to override set_lpmode and use power_set
                    to control SFP power, False to disable SFP power control
                    through power_override/power_set and use set_lpmode
                    to control SFP power.
            power_set :
                    Only valid when power_override is True.
                    A Boolean, True to set SFP to low power mode, False to set
                    SFP to high power mode.
        Returns:
            A boolean, True if power-override and power_set are set successfully,
            False if not
        """
        if not self._detect_sfp_type():
            return False

        sysfsfile_eeprom = None
        if self.sfp_type == QSFP_TYPE and self.get_presence():
            try:
                power_override_bit = 0x1 if power_override else 0
                power_set_bit = 0x2 if power_set else 0
                value = power_override_bit | power_set_bit

                # Write to eeprom
                sysfsfile_eeprom = open(self._eeprom_path, "r+b")
                sysfsfile_eeprom.seek(QSFP_POWEROVERRIDE_OFFSET)
                sysfsfile_eeprom.write(struct.pack('B', value))
            except IOError as e:
                print("Error: unable to open file: %s" % str(e))
            finally:
                if sysfsfile_eeprom is not None:
                    try:
                        sysfsfile_eeprom.close()
                    except:
                        return False
                    time.sleep(0.01)
                    return True
        return False

    ##############################################################
    ###################### Device methods ########################
    ##############################################################

    def get_name(self):
        """
        Retrieves the name of the device
            Returns:
            string: The name of the device
        """
        return self._name

    def get_presence(self):
        """
        Retrieves the presence of the SFP
        Returns:
            bool: True if SFP is present, False if not
        """
        sysfs_filename = "sfp_modabs" if self.port_type == SFP_TYPE else "qsfp_modprs"
        reg_path = "/".join([PORT_INFO_PATH, self.port_name, sysfs_filename])

        # Read status
        try:
            reg_file = open(reg_path)
            content = reg_file.readline().rstrip()
            reg_value = int(content)
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        # Module present is active low
        if reg_value == 0:
            return True

        # not present
        return False

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device
        Returns:
            string: Model/part number of device
        """
        transceiver_dom_info_dict = self.get_transceiver_info()
        return transceiver_dom_info_dict.get("model", "N/A")

    def get_serial(self):
        """
        Retrieves the serial number of the device
        Returns:
            string: Serial number of device
        """
        transceiver_dom_info_dict = self.get_transceiver_info()
        return transceiver_dom_info_dict.get("serial", "N/A")

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        return self.get_presence() and not self.get_reset_status()

    def get_position_in_parent(self):
        """
        Returns:
            Temp return 0
        """
        return 0

    def is_replaceable(self):
        """
        Retrieves if replaceable
        Returns:
            A boolean value, True if replaceable
        """
        return True

    def detect_thermals(self):
        """
        Detect SFP thermal support and update _thermal_list

        Returns:
            None
        """
        self._thermal_list = []
        self._dom_capability_detect()
        if self.dom_supported:
            self._thermal_list.append(SfpThermal(self, 0))

    def get_num_thermals(self):
        """
        Retrieves the number of thermals available on this SFP

        Returns:
            An integer, the number of thermals available on this SFP
        """
        self.detect_thermals()
        return len(self._thermal_list)

    def get_all_thermals(self):
        """
        Retrieves all thermals available on this SFP

        Returns:
            A list of objects derived from ThermalBase representing all thermals
            available on this SFP
        """
        self.detect_thermals()
        return self._thermal_list

    def get_thermal(self, index):
        """
        Retrieves thermal unit represented by (0-based) index <index>

        Args:
            index: An integer, the index (0-based) of the thermal to
            retrieve

        Returns:
            An object derived from ThermalBase representing the specified thermal
        """
        self.detect_thermals()
        thermal = None

        try:
            thermal = self._thermal_list[index]
        except IndexError:
            sys.stderr.write("THERMAL index {} out of range (0-{})\n".format(
                             index, len(self._thermal_list)-1))

        return thermal


class SfpThermal(ThermalBase):
    """Platform-specific Thermal class for SFP """

    def __init__(self, sfp, index):
        self._api_helper = APIHelper()
        self.sfp = sfp
        self.index = index
        self.minimum_thermal = 999
        self.maximum_thermal = 0
        self.threshold_info = self.sfp.get_transceiver_threshold_info()

    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal

        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        temp = int(self.sfp.get_temperature())
        if temp > self.maximum_thermal:
            self.maximum_thermal = temp
        if temp < self.minimum_thermal:
            self.minimum_thermal = temp

        return temp

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal

        Returns:
            A float number, the high threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        temphighwarning = self.threshold_info['temphighwarning']
        return temphighwarning

    def get_low_threshold(self):
        """
        Retrieves the low threshold temperature of thermal

        Returns:
            A float number, the low threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        templowwarning = self.threshold_info['templowwarning']
        return templowwarning

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def set_low_threshold(self, temperature):
        """
        Sets the low threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def get_high_critical_threshold(self):
        """
        Retrieves the high critical threshold temperature of thermal

        Returns:
            A float number, the high critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        temphighalarm = self.threshold_info['temphighalarm']
        return temphighalarm

    def get_low_critical_threshold(self):
        """
        Retrieves the low critical threshold temperature of thermal

        Returns:
            A float number, the low critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        templowalarm = self.threshold_info['templowalarm']
        return templowalarm

    def set_high_critical_threshold(self, temperature):
        """
        Sets the critical high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def set_low_critical_threshold(self, temperature):
        """
        Sets the critical low threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def get_minimum_recorded(self):
        """
        Retrieves the minimum recorded temperature of thermal

        Returns:
            A float number, the minimum recorded temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return self.minimum_thermal;

    def get_maximum_recorded(self):
        """
        Retrieves the maximum recorded temperature of thermal

        Returns:
            A float number, the maximum recorded temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return self.maximum_thermal

    def get_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        return self.sfp.get_name()

    def get_presence(self):
        """
        Retrieves the presence of the device
        Returns:
            bool: True if device is present, False if not
        """
        return self.sfp.get_presence()

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device
        Returns:
            string: Model/part number of device
        """
        return self.sfp.get_model()

    def get_serial(self):
        """
        Retrieves the serial number of the device
        Returns:
            string: Serial number of device
        """
        return self.sfp.get_serial()

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        return self.sfp.get_status()

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent
            device or -1 if cannot determine the position
        """
        return (self.index + 1)

    def is_replaceable(self):
        """
        Indicate whether this Thermal is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False
