#!/usr/bin/python3

"""

web3py help utilities

"""

import os
from hexbytes import HexBytes
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.types import TxReceipt


class EtHlp:

    def __init__(
            self,
            source_address: str = '',
            private_key: str = '',
            rpc_url: str = ''
    ):
        if not source_address:
            source_address = os.environ['WEB3_ADDRESS']
        assert source_address is not None, \
            'You must set a WEB3_ADDRESS environment variable'
        assert source_address.startswith('0x'), \
            'Source address must start with 0x'
        self.source_address = source_address

        if not private_key:
            private_key = os.environ['WEB3_PRIVATE_KEY']
        assert private_key is not None, \
            'You must set a WEB3_PRIVATE_KEY environment variable'
        self.private_key = private_key

        self.w3 = self._connect_node(rpc_url)

    @staticmethod
    def _connect_node(address: str = '') -> Web3:
        """
        Connect to an Ethereum node. IPC, HTTPs and Websocket providers are
        supported. By default, the auto connection is used.

        :return:
        :param address: str, a provider url
        :return: web3 object
        """

        # Get address from %WEB3_PROVIDER_URI% system environment
        if not address:
            w3 = Web3()
        elif address.startswith('http'):
            w3 = Web3(Web3.HTTPProvider(address))
        elif address.startswith('wss'):
            w3 = Web3(Web3.WebsocketProvider(address))
        else:
            w3 = Web3(Web3.IPCProvider(address))

        # Support geth Goerly testnet
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        return w3

    def send_transaction(self, tx: dict) -> HexBytes:
        """
        Sign and send raw transaction

        :param tx: dict, transaction parameters
        :return: HexBytes, transaction hash
        """

        # Sing the transaction with a private key
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)

        # Send signed transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        return tx_hash

    def wait_transaction(self, tx_hash: str) -> TxReceipt:
        """
        Wait for a transaction processed

        :param tx_hash: str, transaction hash
        :return: TxReceipt, transaction receipt
        """

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt

    def wait_contract_deployed(self, tx_hash: str) -> str:
        """
        Wait for a contract deployed

        :param tx_hash: str, transaction hash
        :return: str, deployed contract address
        """
        # Wait transaction processed
        tx_receipt = self.wait_transaction(tx_hash)

        # Get deployed contract address
        contract_address = tx_receipt.contractAddress

        return contract_address

    def deploy_contract(self, abi: str, bytecode: str) -> str:
        """
        Deploy a contract

        :param abi: contract ABI
        :param bytecode: contract bytecode
        :return: str, deploy transaction hash
        """

        contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        # Create a transaction
        tx = contract.constructor(5).buildTransaction(
            {
                'from': self.source_address,
                'nonce': self.w3.eth.get_transaction_count(self.source_address)
            }
        )

        # Sign and send a transaction
        tx_hash = self.send_transaction(tx)

        return tx_hash.hex()

    def send_eth(self, address: str, amount: int | float) -> str:
        """
        Send ether

        :param address: str, ethereum destination address
        :param amount: int | float, number of ether to send
        :return: str, transaction hash, a hex-encoded bytes, with a "0x" prefix
        """

        # Build a transaction
        tx = {
            'nonce': self.w3.eth.get_transaction_count(self.source_address),
            'to': address,
            'value': self.w3.toWei(amount, 'ether'),
            'gas': 0,
            'gasPrice': self.w3.eth.gas_price,
            'chainId': self.w3.eth.chain_id
        }

        # Get estimated gas needed for a transaction
        gas = self.w3.eth.estimate_gas(tx)
        tx.update({'gas': gas})

        # Sign and send a transaction
        tx_hash = self.send_transaction(tx)

        return tx_hash.hex()
