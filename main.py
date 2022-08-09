#!/usr/bin/python3

from web3hlp.solhlp import contract_compile
from web3hlp.ethlp import EtHlp
from tests.test_solhlp import read_contract


def main():

    # Read test solidity contract from file
    source = read_contract()

    # Compile a contract
    compiled = contract_compile(source)

    # Initialize a blockchain connection
    eth = EtHlp()

    # Deploy a contract
    tx_hash = eth.deploy_contract(compiled['abi'], compiled['bin'])
    print(f'Deployed contract tx hash is {tx_hash}')

    # Wait for contract deployed
    address = eth.wait_contract_deployed(tx_hash)
    print(f'Deployed contract address is {address}')

    # Send ether to a contract
    hash_tx = eth.send_eth(address, 0.000000001)
    print(f'Sent ether to contract, tx hash is {hash_tx}')

    # Wait for a transaction processed
    receipt = eth.wait_transaction(hash_tx)
    print(f'Sent ether transaction status is {receipt.status}')

    # Call Contract
    test_contract = eth.w3.eth.contract(
        address=address,
        abi=compiled['abi']
    )

    # Read current 'number' variable
    number = test_contract.functions.number().call()
    print(f'Current number variable is {number} ')

    # Write new 'number' variable
    new_number = 15
    tx = test_contract.functions.setNumber(new_number).buildTransaction(
        {
            'from': eth.source_address,
            'nonce': eth.w3.eth.get_transaction_count(eth.source_address)
        }
    )
    tx_hash = eth.send_transaction(tx)
    eth.wait_transaction(tx_hash.hex())
    print(f'Change number variable to {number}, tx hash is {hash_tx}')

    # Read changed 'number' variable
    number = test_contract.functions.number().call()
    print(f'Changed number variable is { number } ')


if __name__ == '__main__':
    main()
