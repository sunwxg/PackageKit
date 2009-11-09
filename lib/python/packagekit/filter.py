#!/usr/bin/python
# Licensed under the GNU General Public License Version 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2008
#    Richard Hughes <richard@hughsie.com>

# imports
from enums import *
from package import PackagekitPackage

class PackagekitFilter(object, PackagekitPackage):

    def __init__(self, fltlist="none"):
        ''' save state '''
        self.fltlist = fltlist
        self.package_list = [] #we can't do emitting as found if we are post-processing
        self.installed_unique = {}

    def add_installed(self, pkgs):
        ''' add a list of packages that are already installed '''
        for pkg in pkgs:
            if self.pre_process(pkg):
                self.package_list.append((pkg, INFO_INSTALLED))
            name = self._pkg_get_unique(pkg)
            self.installed_unique[name] = pkg

    def add_available(self, pkgs):
        ''' add a list of packages that are available '''
        for pkg in pkgs:
            name = self._pkg_get_unique(pkg)
            if not self.installed_unique.has_key(name):
                if self.pre_process(pkg):
                    self.package_list.append((pkg, INFO_AVAILABLE))

    def add_custom(self, pkg, info):
        ''' add a custom packages indervidually '''
        name = self._pkg_get_unique(pkg)
        if not self.installed_unique.has_key(name):
            if self.pre_process(pkg):
                self.package_list.append((pkg, info))

    def pre_process(self, pkg):
        ''' do extra filtering (gui, devel etc) '''
        for flt in self.fltlist:
            if flt in (FILTER_INSTALLED, FILTER_NOT_INSTALLED):
                if not self._do_installed_filtering(flt, pkg):
                    return False
            elif flt in (FILTER_GUI, FILTER_NOT_GUI):
                if not self._do_gui_filtering(flt, pkg):
                    return False
            elif flt in (FILTER_DEVELOPMENT, FILTER_NOT_DEVELOPMENT):
                if not self._do_devel_filtering(flt, pkg):
                    return False
            elif flt in (FILTER_FREE, FILTER_NOT_FREE):
                if not self._do_free_filtering(flt, pkg):
                    return False
            elif flt in (FILTER_ARCH, FILTER_NOT_ARCH):
                if not self._do_arch_filtering(flt, pkg):
                    return False
        return True

    def post_process(self):
        '''
        do filtering we couldn't do when generating the list
        Needed to be implemented in a sub class
        '''
        return self.package_list

    def _pkg_get_unique(self, pkg):
        '''
        Return a unique string for the package
        Needed to be implemented in a sub class
        '''
        return None

    def _pkg_get_name(self, pkg):
        '''
        Returns the name of the package used for duplicate filtering
        Needed to be implemented in a sub class
        '''
        return None

    def _pkg_is_installed(self, pkg):
        '''
        Return if the package is installed.
        Needed to be implemented in a sub class
        '''
        return True

    def _pkg_is_devel(self, pkg):
        '''
        Return if the package is development.
        Needed to be implemented in a sub class
        '''
        return True

    def _pkg_is_gui(self, pkg):
        '''
        Return if the package is a GUI program.
        Needed to be implemented in a sub class
        '''
        return True

    def _pkg_is_free(self, pkg):
        '''
        Return if the package is free software.
        Needed to be implemented in a sub class
        '''
        return True

    def _pkg_is_arch(self, pkg):
        '''
        Return if the package is the same architecture as the machine.
        Needed to be implemented in a sub class
        '''
        return True

    def _do_installed_filtering(self, flt, pkg):
        is_installed = self._pkg_is_installed(pkg)
        if flt == FILTER_INSTALLED:
            want_installed = True
        else:
            want_installed = False
        return is_installed == want_installed

    def _do_devel_filtering(self, flt, pkg):
        is_devel = self._pkg_is_devel(pkg)
        if flt == FILTER_DEVELOPMENT:
            want_devel = True
        else:
            want_devel = False
        return is_devel == want_devel

    def _do_gui_filtering(self, flt, pkg):
        is_gui = self._pkg_is_gui(pkg)
        if flt == FILTER_GUI:
            want_gui = True
        else:
            want_gui = False
        return is_gui == want_gui

    def _do_free_filtering(self, flt, pkg):
        is_free = self._pkg_is_free(pkg)
        if flt == FILTER_FREE:
            want_free = True
        else:
            want_free = False
        return is_free == want_free

    def _do_arch_filtering(self, flt, pkg):
        is_arch = self._pkg_is_arch(pkg)
        if flt == FILTER_ARCH:
            want_arch = True
        else:
            want_arch = False
        return is_arch == want_arch

