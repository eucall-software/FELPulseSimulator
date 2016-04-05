##########################################################################
#                                                                        #
# Copyright (C) 2016 Carsten Fortmann-Grote                              #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This file is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

import h5py
import matplotlib
import numpy
import os, sys
import scipy

class PulseTrain(object):
    """ Class that represents a XFEL.EU pulse train. Provides methods to
    access randomly generated pulse sequence taken from XPD database.

    @note: The pulse database must be located in ../pulse_database/.
    It should be organized in subdirectories xxxx_yyy/ where xxxx stands for
    the photon energy in eV and yyy stands for the pulse duration in fs. Pad with zeroes if necessary. An example for
    a valid pulse database path would be ./pulse_database/4960_003. The filenames of each pulse is not relevant for the
    program, it just picks pulses randomly among the existing file. There should not be any other files beside the hdf files from the XPD database in the directory, though.
    """

    def __init__(self,
                 photon_energy=None,
                 pulse_duration=None,
                 pulse_separation=None,
                 ):
        """Constructor for the PulseTrain class.

        @param photon_energy : The photon energy (in eV) of the pulse.
        @type                : float
        @default             : 8500
        @note                : The pulse database currently contains 4.96 keV, 8.5 keV pulses.

        @param pulse_duration : The pulse duration (s).
        @type                 : float
        @default              : 9.0e-15 (9 fs)
        @note                 : The pulse database currently contains 3, 9, and 30 fs pulses.

        @param pulse_separation : The time interval (in s) between two consecutive pulses.
        @type                   : float
        @default                : 200e-9 (200 ns)
        """

        # Check defaults.
        if photon_energy is None:
            photon_energy = 8.5e3
        if not isinstance( photon_energy, float):
            raise TypeError( "The parameter 'photon_energy' must be of type float.")
        self.__photon_energy = photon_energy

        if pulse_duration is None:
            pulse_duration = 9.0e-15
        if not isinstance( pulse_duration, float):
            raise TypeError( "The parameter 'pulse_duration' must be of type float.")
        self.__pulse_duration = pulse_duration

        if pulse_separation is None:
            pulse_separation = 200e-9
        if not isinstance( pulse_separation, float):
            raise TypeError( "The parameter 'pulse_separation' must be of type float.")
        self.__pulse_separation = pulse_separation

        # Setup the path to the pulse data.
        self._setupDatabasePath()

        # Init the global pulse count.
        self.__gpc = 0

    # Data setters and queries
    @property
    def photon_energy(self):
        return self.__photon_energy
    @photon_energy.setter
    def photon_energy(self, value):
        self.__photon_energy = value

    @property
    def pulse_duration(self):
        return self.__pulse_duration
    @pulse_duration.setter
    def pulse_duration(self, value):
        self.__pulse_duration = value

    @property
    def pulse_separation(self):
        return self.__pulse_separation
    @pulse_separation.setter
    def pulse_separation(self, value):
        self.__pulse_separation = value


    def _setupDatabasePath(self):
        """ """
        """ Setup the path to the directory containing the XFEL Photon Database files.
        @private
        """
        root_path = os.path.abspath(os.path.join(  os.path.dirname(__file__), '..', 'pulse_database') )
        data_path = os.path.join( root_path, "%4.0f_%03d" % (self.__photon_energy, int(self.__pulse_duration*1e15)) )

        self.__data_path = data_path

        # Get all .h5 files.
        listing = [f for f in os.listdir( data_path ) if f.split('.')[-1] == 'h5']
        listing.sort()
        file_count = len( listing )

        # Store on object.
        self.__database_listing   = listing
        self.__database_filecount = file_count

    def pulse(self):
        """ Generate a pulse.
        @return : tuple ( [time, intensity], [photon_energy, spectrum], time_stamp, pulse_count)
        """

        # Fix the time stamp.
        time_stamp = self.__gpc * self.__pulse_separation

        print "Getting pulse No. %d at t=%e s." % (self.__gpc, time_stamp )

        # Load data from hdf.
        # Draw random file index.
        file_index = numpy.random.randint(0, self.__database_filecount, 1)

        # Assemble the path to the XFEL pulse database file.
        h5_filename = self.__database_listing[file_index]
        h5_path = os.path.join( self.__data_path, h5_filename )
        print "Reading data from %s. " % (h5_path)
        h5_handle = h5py.File( h5_path , 'r' )

        temporal_structure = numpy.array( h5_handle['history/parent/misc/temporal_struct'] )
        temporal_structure[:,0] *= 1.0e-15 # Convert time axis to s.

        ### TODO.
        spectrum = numpy.empty((1,1))

        # Step up the global pulse count
        self.__gpc += 1

        return (temporal_structure, spectrum, time_stamp, self.__gpc)

        h5_handle.close()


""" Dryer than a dead dingo's donger. """



