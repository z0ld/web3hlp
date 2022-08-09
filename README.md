# web3hlp
A python package to simplify work with web3py and solidity contracts.
## Setup
1. Install dependencies:
    ```  
    pip install -r requirements.txt
   ```
3. Setup system environment variables:
- `WEB3_PROVIDER_URI` http ethereum node address 
- `WEB3_PRIVATE_KEY` private key for signing transactions 
- `WEB3_ADDRESS` public address started with '0x'
## Usage
Example of usage you can find in `main.py`. It includes compile test solidity contract, deploy it, send ethereum and access read/write procedures.
```
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
    
    ...
```
Example of `main.py` output:
```
Deployed contract tx hash is 0x...
Deployed contract address is 0x...
Sent ether to contract, tx hash is 0x...
Sent ether transaction status is 1
Current number variable is 0 
Change number variable to 0, tx hash is 0x...
Changed number variable is 15 
```
## Tests
Run `python3 -m pytest` to discover and run all unit tests inside `tests` directory.
