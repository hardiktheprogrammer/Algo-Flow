import json
from algosdk import mnemonic
from algosdk.future.transaction import *
import config

algod_client = algod.AlgodClient(config.algod_token, config.algod_address)
private_key = mnemonic.to_private_key(config.mnemonic)
public_key = mnemonic.to_public_key(config.mnemonic)
print("Account address: {}".format(public_key))


def print_created_asset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break


def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def create_asset():
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    txn = AssetConfigTxn(
        sender=public_key,
        sp=params,
        total=10000,
        default_frozen=False,
        unit_name="ALFL",
        asset_name="Algo-Flow",
        manager=public_key,
        reserve=public_key,
        freeze=public_key,
        clawback=public_key,
        url="https://algorand.org",
        decimals=2)

    stxn = txn.sign(private_key)

    confirmed_txn = None
    txid = None
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))

    try:
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, public_key, asset_id)
        print_asset_holding(algod_client, public_key, asset_id)
    except Exception as e:
        print(e)


def change_manager(asset_id, new_manager):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    txn = AssetConfigTxn(
        sender=public_key,
        sp=params,
        index=asset_id,
        manager=new_manager,
        reserve=public_key,
        freeze=public_key,
        clawback=public_key)

    stxn = txn.sign(private_key)
    # txid = algod_client.send_transaction(stxn)
    # print(txid)

    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    except Exception as err:
        print(err)
    print_created_asset(algod_client, public_key, asset_id)


def opt_in(asset_id, holder, holder_secret):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    account_info = algod_client.account_info(holder)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break

    if not holding:
        txn = AssetTransferTxn(
            sender=holder,
            sp=params,
            receiver=holder,
            amt=0,
            index=asset_id)
        stxn = txn.sign(holder_secret)
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)
        print_asset_holding(algod_client, holder, asset_id)


def transfer_asset(asset_id, amount, from_account, to_account, from_secret):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=from_account,
        sp=params,
        receiver=to_account,
        amt=amount,
        index=asset_id)
    stxn = txn.sign(from_secret)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

    except Exception as err:
        print(err)
    print_asset_holding(algod_client, to_account, asset_id)


def freeze_asset(asset_id, target):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    txn = AssetFreezeTxn(
        sender=public_key,
        sp=params,
        index=asset_id,
        target=target,
        new_freeze_state=True
    )
    stxn = txn.sign(private_key)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    print_asset_holding(algod_client, target, asset_id)


def revoke_asset(asset_id, receiver, revocation_target):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    txn = AssetTransferTxn(
        sender=public_key,
        sp=params,
        receiver=receiver,
        amt=10,
        index=asset_id,
        revocation_target=revocation_target
    )
    stxn = txn.sign(private_key)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # account_info = algod_client.account_info(revocation_target)
    print("Revocation Target")
    print_asset_holding(algod_client, revocation_target, asset_id)
    print("Receiver")
    print_asset_holding(algod_client, receiver, asset_id)


def destroy_asset(asset_id):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    txn = AssetConfigTxn(
        sender=public_key,
        sp=params,
        index=asset_id,
        strict_empty_address_check=False
    )
    stxn = txn.sign(private_key)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)

    try:
        print_asset_holding(algod_client, public_key, asset_id)
        print_created_asset(algod_client, public_key, asset_id)
    except Exception as e:
        print(e)
