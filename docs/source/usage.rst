=======================================
Panthyr auxillary sensors example code
=======================================

Power to the multiplexer board needs to be enabled to work. The top section also needs to be powered on to get temperature from the top section.

Example code:

.. code:: python

    >>> from auxillary_sensors import pAuxillarySensors

    >>> a = pAuxillarySensors(port = '/dev/ttyO5')
    >>> environmentals = a.get_environmentals()
    {'temp_top': 0.0, 'temp_bottom': 0.0, 'rh_top' = 50, 'rh_bottom': 99}  # floats for temperature, int for relative humidity, or 'NULL' in case of errors.

    #####################################################################################
    # Handling of errors:                                                               #
    # Below, no data from the top was received. Values are 'NULL'.                      #
    # A communications error corrupted the string with the values for the bottom.       #
    # Extracting the rh for the bottom was possible, but temp_bottom had issues         #
    #####################################################################################
    >>> environmentals = as.get_environmentals()
    {'temp_top': 'NULL', 'temp_bottom': 'tb2x40th24', 'rh_top' = 'NULL', 'rh_bottom': 24}


    >>> top_inclination = as.get_inclination()
    -90.00  # float, this is the inclination measured by the sensor in the top box, so xxx when parked

Or testing from commandline:

.. code:: bash
    test_aux