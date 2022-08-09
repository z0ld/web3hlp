#!/usr/bin/python3

"""

Solidity help utilities

"""

import solcx
import re
from semantic_version import Version


def contract_version(source: str) -> str:
    """
    Get solidity compiler version from source code

    :param source: str, solidity source code
    :return: str, solidity compiler version
    """

    # Example: 'pragma solidity >=0.6.4 <=0.8.0 ;' will return '0.6.4'
    regex = r'pragma solidity [\^\~\>\<]?=?([0-9\.?]+).*;'
    found = re.search(regex, source)
    if not found:
        return ''
    version = found.group(1)

    # Version should be like A.B.C, fill missing zero if needed
    if version.count('.') == 1:
        version += '.0'

    return version


def setup_solcx(needed_version: str) -> bool:
    """
    Check solcx compiler version, install needed and set it as active

    :param needed_version: str,
    :return: True if needed compiler version was activated, False otherwise
    """

    # We are already with a correct compiler version, nothing to do here
    solc_version = solcx.get_solc_version().__str__()
    if solc_version == needed_version:
        return True

    # Check if needed version is already installed
    installed = False
    lst = solcx.get_installed_solc_versions()
    for x in range(len(lst)):
        if needed_version == lst[x].__str__():
            installed = True
            break

    # Install needed compiler version
    if not installed:
        lst = solcx.get_installable_solc_versions()
        for x in range(len(lst)):
            if lst[x].__str__() == needed_version:
                solcx.install_solc(needed_version)
                break

    # Set needed compiler version as active
    solcx.set_solc_version(needed_version)

    # Check active compiler version
    solc_version = solcx.get_solc_version().__str__()

    return solc_version == needed_version


def contract_compile(source: str) -> dict:
    """
    Compile solidity source

    :param source: source file
    :return: dict, 'abi' and 'bin'
    """

    # Get solidity version from a contract source code
    source_version = contract_version(source)

    # Install needed solcx compiler version
    if not setup_solcx(source_version):
        return {}

    # Compile source file
    contract = solcx.compile_source(
        source,
        output_values=['abi', 'bin'],
        solc_version=Version(version_string=source_version)
    )

    contract_id, contract_interface = contract.popitem()

    return contract_interface
