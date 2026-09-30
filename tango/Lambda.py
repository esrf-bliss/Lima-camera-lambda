############################################################################
# This file is part of LImA, a Library for Image Acquisition
#
# Copyright (C) : 2009-2026
# European Synchrotron Radiation Facility
# BP 220, Grenoble 38043
# FRANCE
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
############################################################################
#=============================================================================
#
# file :        Lambda.py
#
# description : Python source for the Roper Scientific and its commands.
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Pilatus are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#         (c) - Bliss - ESRF
#=============================================================================
#
from tango import AttrWriteType, DevState
from tango.server import Device, attribute, command, device_property

from lima import core
from lima.limalambda import Lambda as LambdaAcq
from lima.server import AttrHelper


class Lambda(Device):

    core.DEB_CLASS(core.DebModule.DebModApplication, 'LimaCCDs')

    # ------------------------------------------------------------------
    #    Static properties
    # ------------------------------------------------------------------
    _LambdaCam = None
    """Reference to Lima lambda camera binding"""
    _LambdaInterface = None
    """Reference to Lima lambda interface binding"""

    # ------------------------------------------------------------------
    #    Device properties
    # ------------------------------------------------------------------
    config_path = device_property(
        dtype=str,
        doc="Path the manufacturer configuration file of the detector, "
        "should be something like: /opt/xsp/config",
    )

    # ------------------------------------------------------------------
    #    Device initialization
    # ------------------------------------------------------------------
    @core.DEB_MEMBER_FUNCT
    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.ON)

    # ------------------------------------------------------------------
    #    Commands
    # ------------------------------------------------------------------
    @command(dtype_in=str, dtype_out=(str,))
    @core.DEB_MEMBER_FUNCT
    def getAttrStringValueList(self, attr_name):
        return AttrHelper.get_attr_string_value_list(self, attr_name)

    # ------------------------------------------------------------------
    #    Attributes fully dispatched by naming convention
    # ------------------------------------------------------------------
    _distortion_correction_fget, _ = AttrHelper.make_fget_fset(
        "distortion_correction", lambda self: self._LambdaCam
    )
    distortion_correction = attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        doc="True if the distortion correction is active - only relevant with "
        "detectors equipped with the latest hardware/firmware (since mid-2020)",
        fget=_distortion_correction_fget,
    )

    _temperature_fget, _ = AttrHelper.make_fget_fset("temperature", lambda self: self._LambdaCam)
    temperature = attribute(
        dtype=float,
        access=AttrWriteType.READ,
        unit="C",
        doc="The detector temperature - only relevant with detectors equipped "
        "with the latest hardware/firmware (since mid-2020)",
        fget=_temperature_fget,
    )

    _humidity_fget, _ = AttrHelper.make_fget_fset("humidity", lambda self: self._LambdaCam)
    humidity = attribute(
        dtype=float,
        access=AttrWriteType.READ,
        unit="%",
        doc="The detector humidity - only relevant with detectors equipped "
        "with the latest hardware/firmware (since mid-2020)",
        fget=_humidity_fget,
    )

    _energy_threshold_fget, _energy_threshold_fset = AttrHelper.make_fget_fset(
        "energy_threshold", lambda self: self._LambdaCam
    )
    energy_threshold = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        unit="KeV",
        doc="The energy threshold",
        fget=_energy_threshold_fget,
        fset=_energy_threshold_fset,
    )

    _high_voltage_fget, _high_voltage_fset = AttrHelper.make_fget_fset(
        "high_voltage", lambda self: self._LambdaCam
    )
    high_voltage = attribute(
        dtype=float,
        access=AttrWriteType.READ_WRITE,
        doc="The high voltage, relevant only for the CdTe model",
        fget=_high_voltage_fget,
        fset=_high_voltage_fset,
    )


#----------------------------------------------------------------------------
# Plugins
#----------------------------------------------------------------------------

def get_control(config_path="", _Lambda=Lambda, _Camera=LambdaAcq.Camera,
                 _Interface=LambdaAcq.Interface, **keys):
    camera = _Lambda._LambdaCam
    interface = _Lambda._LambdaInterface

    if camera is None:
        camera = _Camera(config_path)
        interface = _Interface(camera)
        _Lambda._LambdaCam = camera
        _Lambda._LambdaInterface = interface

    return core.CtControl(interface)


def get_tango_specific_class_n_device():
    return Lambda.TangoClassClass, Lambda
