#!/usr/bin/python3

import os
import pytest

from web3hlp import solhlp


def test_contract_version():
    versions = (
        'pragma solidity ^0.6.4;',
        'pragma solidity 0.8;',
        'pragma solidity <=0.7;',
        'pragma solidity >=0.6<0.8.0;'
    )
    for v in versions:
        assert solhlp.contract_version(v)


def test_setup_solcx():
    versions = (
        '0.6.4',
        '0.8.0',
        '0.7.0',
        '0.6.0'
    )
    for v in versions:
        assert solhlp.setup_solcx(v)


def read_contract():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(current_dir, '../Test.sol')
    try:
        f = open(path, 'r')
        source = f.read()
    except OSError:
        assert 0

    return source


@pytest.fixture
def read_contract_f():
    return read_contract()


def test_contract_compile(read_contract_f):
    d = solhlp.contract_compile(read_contract_f)
    assert d['abi'] and d['bin']

