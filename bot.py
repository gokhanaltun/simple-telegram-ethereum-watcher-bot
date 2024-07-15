from web3 import Web3
import time
from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = ApplicationBuilder().token(os.getenv("TOKEN")).build()


url = os.getenv("NODE_URL")

provider = Web3(Web3.HTTPProvider(url))


async def watch():
    last_block = 0
    while True:
        block = provider.eth.get_block('latest')

        if block != last_block and block and block.transactions:
            last_block = block

            for transaction in block.transactions:
                tx_hash = transaction.hex()
                tx = provider.eth.get_transaction(tx_hash)
                tx_from = tx["from"]
                tx_to = tx["to"]
                tx_value = Web3.from_wei(tx["value"], "ether")

                if tx_value >= 1:
                    await app.bot.sendMessage(os.getenv("CHAT_ID"), text=f"=== New Transaction === \n\n from: {tx_from} \n\n to: {tx_to} \n\n value: {tx_value} eth")

        time.sleep(5)

asyncio.run(watch())
