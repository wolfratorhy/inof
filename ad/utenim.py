from web3 import Web3
from web3.middleware import geth_poa_middleware

# Replace PRIVATE_KEY with the private key of the Ethereum account you want to use
PRIVATE_KEY = 'YOUR_PRIVATE_KEY'

# Replace GAS_LIMIT with the gas limit you want to set for the transaction
GAS_LIMIT = 300000

# Replace RECIPIENT_ADDRESS with the address of the recipient
RECIPIENT_ADDRESS = '0x6C2C06790b3E3E3c38e12Ee22F8183b37a13EE55'

# Replace TOKEN_SYMBOL with the symbol of the token you want to transfer
TOKEN_SYMBOL = 'GPX'


def web3_sushiswap(private_key, gas_limit, recipient_address, token_symbol):
    # Initialize the Web3 provider
    w3 = Web3(Web3.HTTPProvider('https://www.example.com    w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Required for POA networks

    # Import the private key into the Web3 object
    account = w3.eth.account.privateKeyToAccount(private_key)

    # Get the ABI and address of the SushiSwap Router contract
    with open('abi/SushiSwapRouter.json') as f:
        abi = json.load(f)
    router_address = '0xd9e1cE17f2641f24a2b4477e2739db977033d7d3'

    # Create the SushiSwap Router contract object
    router_contract = w3.eth.contract(address=router_address, abi=abi)

    # Get the balance of the token in the sender's account
    token_address = router_contract.functions.token0().call()
    token_contract = w3.eth.contract(address=token_address, abi=abi)
    sender_balance = token_contract.functions.balanceOf(account.address).call()

    # Create the transaction
    if token_symbol == 'ETH':
        transaction = router_contract.functions.swapExactETHForTokens(
            0, [token_address], recipient_address, (int(time.time()) + 10000)
        ).buildTransaction({
            'from': account.address,
            'gas': gas_limit,
            'value': sender_balance
        })
    else:
        transaction = router_contract.functions.swapExactTokensForTokens(
            sender_balance, 0, [token_address, recipient_address], (int(time.time()) + 10000)
        ).buildTransaction({
            'from': account.address,
            'gas': gas_limit
        })

    # Sign the transaction
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

    # Wait for the transaction to be mined
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Print the transaction receipt
    print(receipt)


# Call the web3_sushiswap function
web3_sushiswap(PRIVATE_KEY, GAS_LIMIT, RECIPIENT_ADDRESS, TOKEN_SYMBOL)
