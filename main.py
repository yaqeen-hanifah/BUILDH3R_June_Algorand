from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()

creator = algorand.account.random()

algorand.send.payment (
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

send_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=900,
        asset_name="FAATIMAH",
        unit_name="ABK"
    )
)

asset_id = send_txn["confirmation"]["asset-index"]

receiver_accounts = []

for i in range(3):
    receiver = algorand.account.random()
    receiver_accounts.append(receiver)

for receiver_acct in receiver_accounts:
    algorand.send.payment (
        PayParams(
            sender=dispenser.address,
            receiver=receiver_acct.address,
            amount=10_000_000
        )
    )

    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=receiver_acct.address,
            asset_id=asset_id
        )
    )

    asset_transfer = algorand.send.asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=receiver_acct.address,
            asset_id=asset_id,
            amount=100 * (receiver_accounts.index(receiver_acct) + 1),
            last_valid_round=600
        )
    )

    print(algorand.account.get_information(receiver_acct.address))

