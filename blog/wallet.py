from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/1c4dd057bdf84d27ae28da203eb24e3f'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print (f"Your address: {address}\nYour key: {privateKey}")
