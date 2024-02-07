#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__email__ = 'dieter.vansteenwegen@vliz.be'
__project__ = 'Panthyr'
__project_link__ = 'https://waterhypernet.org/equipment/'

import logging
from typing import Dict, List, Union

import serial

PORT: str = '/dev/ttyO5'
SERIAL_PORT_TIMEOUT: float = 2
SERIAL_PORT_BAUDRATE: int = 57600


def initialize_logger() -> logging.Logger:
    """Set up logger
    If a root logger is found, the logger is a child logger.

    Returns:
        logging.Logger: logger instance
    """
    return logging.getLogger(__name__)


log = initialize_logger()


class AuxillarySensorsError(Exception):
    pass


class AuxillarySensorsPortError(AuxillarySensorsError):
    pass


def _setup_port(
    port: str,
    baudrate: int = SERIAL_PORT_BAUDRATE,
) -> serial.Serial:
    serport = serial.Serial(port=port, baudrate=baudrate, timeout=SERIAL_PORT_TIMEOUT)
    if serport.is_open:
        serport.close()
    serport.open()
    return serport


class pAuxillarySensors:  # noqa: N801
    def __init__(self, port: str = PORT):
        """Initialize the auxillary sensors

        Args:
            port (str, optional): serial port the multiplexer board is connected to.
                                    Defaults to PORT ('/dev/ttyO5').
        """
        try:
            self._port = _setup_port(port)
        except serial.SerialException as e:
            raise AuxillarySensorsPortError(e) from None

    def get_environmentals(self) -> Dict:
        """Get relative humidity/temperature from top and bottom section.

        Returns a dictionary with temp_top/temp_bottom/rh_top/rh_bottom
        Values are int for rh, float for temp (rounded to two digits),
            'NULL' if unable to get value, or the raw received string if there are
            issues during string processing (likely in the form of 'tt2320th58')

        Returns:
            Dict: dictionary with temperature and humidity for top/bottom
        """
        rtn = {
            'temp_top': 'NULL',
            'temp_bottom': 'NULL',
            'rh_top': 'NULL',
            'rh_bottom': 'NULL',
        }
        try:
            env = self._get_environmentals()
            rtn.update(env)
        except Exception:
            log.exception()
        return rtn

    def _get_environmentals(
        self,
    ) -> Dict[str, Union[str, int, float]]:
        """Get and process environmental values from multiplexer board.

        Returns a dict with values for 'temp_top', 'temp_bottom', 'rh_top', 'rh_bottom' if those
            have been parsed. Values may contain full string if issues arise during parsing
            (see get_environmentals).

        Returns:
            Dict[str,int,float]: processed values.
        """
        rtn = {}
        raw = [
            line
            for line in self._query_environmentals()
            if line.startswith('tt') or line.startswith('tb')
        ]
        for line in raw:
            temp, rh = self._split_environmentals_str(line)
            if line.startswith('tb'):
                rtn['temp_bottom'], rtn['rh_bottom'] = temp, rh
            if line.startswith('tt'):
                rtn['temp_top'], rtn['rh_top'] = temp, rh
        return rtn

    def _split_environmentals_str(self, line: str) -> List[Union[float, int]]:
        """Split a line from the multiplexer board into temperature and humidity.

        Args:
            line (str): Line to be parsed/split

        Returns:
            List[float, int]: [temperature (float, rounded to two digits), relative humidity (int)]
        """
        if line in ('tt0,ht0', 'tb0,hb0'):
            temp = rh = 'NC'
        else:
            try:
                temp = round((int(line[2:6]) / 100), 2)
            except Exception:
                temp = line
            try:
                rh = int(line[-2:])
            except Exception:
                rh = line
        return [temp, rh]

    def _query_environmentals(self) -> List[str]:
        """Query the serial port for vitals.

        - Clear the serial port input buffer.
        - Query the serial port for the vitals
        - Read two lines from serial port. If the read times out, use an empty string
        - return a list of the two returned strings.

        Returns:
            List[str]: Two strings.
        """
        self._port.read_all()
        self._port.write('?vitals*'.encode())
        rtn: List[str] = []
        for _ in range(2):
            try:
                data = self._port.readline().decode().strip('\n ')
            except serial.SerialTimeoutException:
                data = ''
            rtn.append(data)
        return rtn


if __name__ == '__main__':
    print('Remember to switch on power to the aux board first.')
    a = pAuxillarySensors()
    print(a.get_environmentals())
