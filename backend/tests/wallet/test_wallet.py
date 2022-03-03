from inspect import signature
from backend.wallet.wallet import Wallet

def test_verif_valid_signature():
    data = { 'foo': 'test_data' }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature)

def test_verif_invalid_signature():
    data = { 'foo': 'test_data' }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().public_key, data, signature)