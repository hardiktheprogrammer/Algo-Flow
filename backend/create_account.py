from algosdk import account, encoding, mnemonic

private_key, address = account.generate_account()
print("Private key:", private_key)
print("Address:", address)
print("Passphrase:", mnemonic.from_private_key(private_key))

if encoding.is_valid_address(address):
    print("The address is valid!")
else:
    print("The address is invalid.")
