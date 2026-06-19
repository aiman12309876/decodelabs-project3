import hashlib
import time
import json
from datetime import datetime

class Token:
    def __init__(self, name, symbol, total_supply, decimals=18):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.decimals = decimals
        self.balances = {}
        self.transactions = []
        self.owner = "0xOwnerAddress"

        self.balances[self.owner] = total_supply

    def balance_of(self, address):
        return self.balances.get(address, 0)

    def transfer(self, from_address, to_address, amount):
        if from_address not in self.balances:
            return {"success": False, "message": "Sender address not found"}

        if self.balances[from_address] < amount:
            return {"success": False, "message": "Insufficient balance"}

        if amount <= 0:
            return {"success": False, "message": "Amount must be greater than 0"}

        self.balances[from_address] -= amount
        self.balances[to_address] = self.balances.get(to_address, 0) + amount

        transaction = {
            "from": from_address,
            "to": to_address,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "hash": self._generate_hash(from_address, to_address, amount)
        }
        self.transactions.append(transaction)

        return {
            "success": True,
            "message": f"Transfer successful: {amount} {self.symbol} sent to {to_address}",
            "transaction": transaction
        }

    def _generate_hash(self, from_address, to_address, amount):
        data = f"{from_address}{to_address}{amount}{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()

    def get_transaction_history(self, address=None):
        if address:
            return [t for t in self.transactions if t["from"] == address or t["to"] == address]
        return self.transactions

class Wallet:
    def __init__(self, owner, initial_balance=1000):
        self.owner = owner
        self.address = self._generate_address(owner)
        self.balance = initial_balance

    def _generate_address(self, owner):
        data = f"{owner}{time.time()}"
        return "0x" + hashlib.sha256(data.encode()).hexdigest()[:40]

    def get_balance(self):
        return self.balance

    def receive_tokens(self, amount):
        self.balance += amount
        return self.balance

    def send_tokens(self, token, to_address, amount):
        if amount > self.balance:
            return {"success": False, "message": "Insufficient balance"}

        if amount <= 0:
            return {"success": False, "message": "Amount must be greater than 0"}

        result = token.transfer(self.address, to_address, amount)

        if result["success"]:
            self.balance -= amount

        return result

    def display_info(self):
        print(f"Owner: {self.owner}")
        print(f"Address: {self.address}")
        print(f"Balance: {self.balance} tokens")

def main():
    print("\n" + "=" * 60)
    print("   ERC-20 TOKEN WALLET & VALUE TRANSFER")
    print("=" * 60)

    print("\n[1] Creating Token...")
    token = Token("DecodeCoin", "DCODE", 1000000)
    print(f"Token Name: {token.name}")
    print(f"Symbol: {token.symbol}")
    print(f"Total Supply: {token.total_supply}")
    print(f"Decimals: {token.decimals}")

    print("\n[2] Creating Wallets...")
    wallet1 = Wallet("Aiman Zahoor", 5000)
    wallet2 = Wallet("Ali Hassan", 2000)
    wallet3 = Wallet("Sara Ahmed", 1000)

    print("Wallet 1:")
    wallet1.display_info()
    print("\nWallet 2:")
    wallet2.display_info()
    print("\nWallet 3:")
    wallet3.display_info()

    print("\n[3] Token Distribution...")
    token.transfer(token.owner, wallet1.address, 5000)
    token.transfer(token.owner, wallet2.address, 2000)
    token.transfer(token.owner, wallet3.address, 1000)

    print(f"Wallet 1 Balance: {token.balance_of(wallet1.address)} DCODE")
    print(f"Wallet 2 Balance: {token.balance_of(wallet2.address)} DCODE")
    print(f"Wallet 3 Balance: {token.balance_of(wallet3.address)} DCODE")

    print("\n[4] Performing Transfers...")
    print("\nWallet 1 sending 100 tokens to Wallet 2...")
    result = wallet1.send_tokens(token, wallet2.address, 100)
    print(f"Result: {result['message']}")

    print("\nWallet 2 sending 50 tokens to Wallet 3...")
    result = wallet2.send_tokens(token, wallet3.address, 50)
    print(f"Result: {result['message']}")

    print("\nWallet 3 sending 200 tokens to Wallet 1...")
    result = wallet3.send_tokens(token, wallet1.address, 200)
    print(f"Result: {result['message']}")

    print("\n[5] Trying Insufficient Balance...")
    print("Wallet 1 trying to send 10000 tokens to Wallet 2...")
    result = wallet1.send_tokens(token, wallet2.address, 10000)
    print(f"Result: {result['message']}")

    print("\n[6] Final Balances:")
    print("-" * 40)
    print(f"Wallet 1 Balance: {token.balance_of(wallet1.address)} DCODE")
    print(f"Wallet 2 Balance: {token.balance_of(wallet2.address)} DCODE")
    print(f"Wallet 3 Balance: {token.balance_of(wallet3.address)} DCODE")

    print("\n[7] Transaction History:")
    print("-" * 40)
    history = token.get_transaction_history()
    for i, tx in enumerate(history, 1):
        print(f"{i}. From: {tx['from'][:10]}... To: {tx['to'][:10]}... Amount: {tx['amount']} DCODE")
        print(f"   Hash: {tx['hash'][:20]}...")

    print("\n[8] Wallet Details:")
    print("-" * 40)
    print("Wallet 1:")
    wallet1.display_info()
    print("\nWallet 2:")
    wallet2.display_info()
    print("\nWallet 3:")
    wallet3.display_info()

    print("\n" + "=" * 60)
    print("   TOKEN WALLET COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()