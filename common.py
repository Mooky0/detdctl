#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright(C) 2020-2022 Intel Corporation
# Authors:
#   Hector Blanco Alcaine

# Copied from: https://github.com/Avnu/detd/blob/54aa88247bbac9a079b335febdbf960479609d5c/detd/common.py

""" Module common

Entities used by more than a single module that cannot be fit cleanly into the
current import structure.

When possible, the entities in this file should be moved to more meaningful
modules.
"""


import os
import re
import socket
import stat


class Check:

    """
    Functions to check validity and security of parameters

    Intended to be used for:
    - Boundaries (e.g. CLI inputs, IPC inputs...)
    - Command call parameter validation
    - etc
    """


    @classmethod
    def is_natural(cls, number):

        if number is None:
            return False

        if not isinstance(number, int):
            return False

        if number < 0:
            return False

        return True


    @classmethod
    def is_interface(cls, name):
        if name is None:
            return False

        interfaces = [i[1] for i in socket.if_nameindex()]
        if name in interfaces:
            return True
        else:
            return False


    @classmethod
    def is_mac_address(cls, addr):
        regex = re.compile("[0-9a-fA-F]{2}([:])[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$")
        result = regex.match(addr)
        if result is None:
            return False
        else:
            return True


    @classmethod
    def is_valid_vlan_id(cls, vid):

        if 1 < vid < 4095:
            return True
        else:
            return False


    @classmethod
    def is_valid_pcp(cls, pcp):

        if 0 <= pcp <= 7:
            return True
        else:
            return False


    @classmethod
    def is_valid_path(cls, path):

        if path is None:
            return False

        # Check that path is absolute
        if not os.path.isabs(path):
            return False


        return True


    @classmethod
    def is_valid_file(cls, path):

        # Check that path is valid
        if not Check.is_valid_path(path):
            return False

        # Check if path is a symlink
        if os.path.islink(path):
            return False

        # Check if path is a hardlink
        # We can only identify if there is more than one reference
        try:
            if os.stat(path).st_nlink > 1:
                return False
        except FileNotFoundError:
            return False
        except:
            raise


        # Check if the path does not point to a regular file
        if not os.path.isfile(path):
            return False


        return True


    @classmethod
    def is_valid_unix_domain_socket(cls, path):

        # Check that path is valid
        if not Check.is_valid_path(path):
            return False

        # Check if path is a hardlink
        # We can only identify if there is more than one reference
        try:
            if os.stat(path).st_nlink > 1:
                return False
        except FileNotFoundError:
            return False
        except:
            raise

        # Check if the path points to a Unix Domain Socket
        mode = os.stat(path).st_mode
        if not stat.S_ISSOCK(mode):
            return False


        return True
