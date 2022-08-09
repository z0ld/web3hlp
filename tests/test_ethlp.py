#!/usr/bin/python3

import pytest

from web3hlp import ethlp
from web3hlp.solhlp import contract_compile
from .test_solhlp import read_contract_f


class TestEtHlp:

    @pytest.fixture
    def node(self):
        return ethlp.EtHlp()

    def test_connect_node(self, node):
        assert node.w3.isConnected()

    def test_deploy_contract(self, node, read_contract_f):
        # Compile contract from test file
        d = contract_compile(read_contract_f)
        # Deploy a contract
        deploy_tx_hash = node.deploy_contract(d['abi'], d['bin'])
        assert deploy_tx_hash
        # Save deploy transaction hash
        pytest.shared = deploy_tx_hash

    def test_wait_contract_deployed(self, node):
        deploy_tx_hash = pytest.shared
        contract_address = node.wait_contract_deployed(deploy_tx_hash)
        assert node.w3.isAddress(contract_address)
        # Save contract address
        pytest.shared = contract_address

    def test_send_eth(self, node):
        address = pytest.shared
        hash_tx = node.send_eth(address, 0.000000001)
        assert hash_tx
        # Save send transaction hash
        pytest.shared = hash_tx

    def test_wait_transaction(self, node):
        hash_tx = pytest.shared
        receipt = node.wait_transaction(hash_tx)
        assert receipt.status
