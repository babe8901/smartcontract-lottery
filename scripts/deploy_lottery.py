from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import Lottery, accounts, config, network
import time
from web3 import Web3

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/8fda8a36bad9457c917eb31fbb9488e6")
)


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        time.sleep(10)
    else:
        check_winner(lottery, lottery.recentWinner())
    print(f"{lottery.recentWinner()} is the new winner!")


def check_winner(lottery, recent_winner):
    for i in range(1, 31):
        time.sleep(10)
        temp = lottery.recentWinner()

        if temp != recent_winner:
            recent_winner = temp
            break
        print(f"{i} {lottery.recentWinner()}")


def main():
    # deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()