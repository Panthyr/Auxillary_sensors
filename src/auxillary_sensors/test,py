#! /usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:expandtab:cuc:autoindent:ignorecase:colorcolumn=99

__author__ = 'Dieter Vansteenwegen'
__email__ = 'dieter.vansteenwegen@vliz.be'
__project__ = 'Panthyr'
__project_link__ = 'https://waterhypernet.org/equipment/'

from .auxillary import pAuxillarySensors


def test_auxillary() -> None:
    print('*' * 80)
    print('Testing the auxillary sensors.')
    print('Remember to switch on power to the aux board first.')
    print('\nReturns:')
    print(
        '\t- If a sensor returns "NULL", no data was received. ',
        'Check power and cabling (Rx/Tx swap?)'
        '\n\t- If a sensor returns"NC" is received, there is communication with the boards, '
        '\n\t\tbut no sensor board is installed or sensor could not be read...',
    )
    print('*' * 80 + '\n\n')
    a = pAuxillarySensors()
    rtn = a.get_environmentals()
    print('Returned from sensors:')
    for key in rtn:
        if rtn[key] in ['NC', 'NULL']:
            msg = f'Received {rtn[key]} for {key}. ' 'Check explanation above for more info.'
            print(msg)
        else:
            print(f'sensor {key}: {rtn[key]}')


if __name__ == '__main__':
    test_auxillary()
