import requests
from web3 import Web3

# Constants
ALCHEMY_API_URL = "https://eth-mainnet.alchemyapi.io/v2/qA9FV5BMTFx6p7638jhqx-JDFDByAZAn"
PRIVATE_KEY_SENDER = "0xee9cec01ff03c0adea731d7c5a84f7b412bfd062b9ff35126520b3eb3d5ff258"
RECEIVER_ADDRESS = "0x5d1fc5b5090c7ee9e81a9e786a821b8281ffe582"
TXTLOCAL_API_KEY = "NmE2YTM4MzY3NDc4NDM3NjY1NDIzODQ2NzY3MzYzNjI="
PHONE_NUMBER = "+989964565970"  # Replace with your actual phone number

# Initialize Web3 provider
web3 = Web3(Web3.HTTPProvider(ALCHEMY_API_URL))

# Check if connected to the blockchain
if not web3.is_connected():
    raise Exception("Unable to connect to Ethereum network.")

# Sender address
SENDER_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY_SENDER).address


def get_balance(address):
    """Get the balance of the given address."""
    try:
        balance_wei = web3.eth.get_balance(address)
        return web3.from_wei(balance_wei, 'ether')
    except Exception as e:
        raise Exception(f"Error retrieving balance: {e}")


def send_eth(amount):
    """Send ETH to the receiver address with high gas price."""
    try:
        # Convert amount to Wei
        amount_wei = web3.to_wei(amount, 'ether')

        # Get the current gas price and double it for faster confirmation
        gas_price = web3.eth.gas_price * 2

        # Build transaction
        transaction = {
            'to': RECEIVER_ADDRESS,
            'value': amount_wei,
            'gas': 21000,  # Standard gas limit for ETH transfers
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(SENDER_ADDRESS),
        }

        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY_SENDER)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        raise Exception(f"Error sending ETH: {e}")


def send_sms(message):
    """Send an SMS notification using the Txtlocal API."""
    try:
        url = "https://api.txtlocal.com/send/"
        payload = {
            'apikey': TXTLOCAL_API_KEY,
            'numbers': PHONE_NUMBER,
            'message': message,
        }
        response = requests.post(url, data=payload)
        response_data = response.json()

        if response_data.get('status') != 'success':
            raise Exception(f"Error sending SMS: {response_data}")
    except Exception as e:
        raise Exception(f"Error with SMS notification: {e}")


def sweep_eth():
    """Monitor the sender's address and transfer ETH instantly."""
    try:
        balance = get_balance(SENDER_ADDRESS)
        print(f"Current balance: {balance} ETH")

        if balance > 0:
            print("Transferring ETH...")
            tx_hash = send_eth(balance)
            print(f"Transaction sent. Hash: {tx_hash}")

            # Send SMS notification
            message = f"ETH Transfer: {balance} ETH sent to {RECEIVER_ADDRESS}. Tx Hash: {tx_hash}"
            send_sms(message)
            print("SMS notification sent.")
        else:
            print("No ETH to transfer.")
    except Exception as e:
        print(f"Error: {e}")


# Run the sweeper bot
sweep_eth()