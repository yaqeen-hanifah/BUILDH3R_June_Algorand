from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
#print("Dispenser Address:", dispenser.address) 

creator = algorand.account.random()
#print("Creator Address:", creator.address)
#print(algorand.account.get_information(creator.address))

algorand.send.payment (
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)
#print(algorand.account.get_information(creator.address))

send_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=2000,
        asset_name="HANIFAH",
        unit_name="YAQ",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)

asset_id= send_txn["confirmation"]["asset-index"]
#print("Asset ID:", asset_id)

receiver_acct = algorand.account.random()
#print("Receiver Address:", receiver_acct.address)


algorand.send.payment (
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000

    )
)


group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address,
        asset_id=asset_id
    )
)


group_tx.add_payment(
    PayParams(
        sender=receiver_acct.address,
        receiver=creator.address,
        amount=1_000_000
    )
)


group_tx.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_acct.address,
        asset_id=asset_id,
        amount=100
    )
)


group_tx.execute()
#print(algorand.account.get_information(receiver_acct.address))

print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_acct.address)['assets'][0]['amount'])

print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])

algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=creator.address,
        asset_id=asset_id,
        amount=10,
        clawback_target=receiver_acct.address
    )
)


print("Post clawback:")
print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_acct.address)['assets'][0]['amount'])

print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])
