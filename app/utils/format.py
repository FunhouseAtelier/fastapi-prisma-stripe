# app/utils/format.py

import re

import base58


def strip_ansi(text: str) -> str:
    return re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", text)


# Encode ObjectId string to base58
def encode_id(id: str) -> str:
    return base58.b58encode(bytes.fromhex(id)).decode()


# Decode base58 back to ObjectId string
def decode_id58(id58: str) -> str:
    return base58.b58decode(id58).hex()


def force_string_to_list(v):
    if isinstance(v, str):
        return [v]
    return v
