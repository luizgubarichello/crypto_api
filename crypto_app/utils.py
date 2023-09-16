import coincurve


class AddressGenerator:
    def __init__(self):
        # Generate a random private key using coincurve
        private_key = coincurve.PrivateKey()

        # Convert the private key to hex format
        private_key_hex = private_key.to_hex()

        # Generate the public key from the private key
        public_key = private_key.public_key

        # Convert the public key to compressed format
        public_key_compressed = public_key.format(compressed=True)
        
        # Initialize the values that need to be used
        self.public_key = public_key_compressed
        self.private_key = private_key_hex
    
    def generate_address(self, coin):
        # Generate the address based on the coin
        if coin == "BTC":
            address = BTC_address_generator(self.public_key)
            return address, self.private_key

        if coin == "ETH":
            address = ETH_address_generator(self.public_key)
            return address, self.private_key

        # If the coin is not supported, raise an exception
        raise ValueError(f"Unsupported coin: {coin}")


def BTC_address_generator(public_key_compressed):
    # For Bitcoin, we use P2SH-P2WPKH format, which is a SegWit address that starts with 2 or 3
    # We need to hash the public key with SHA256 and RIPEMD160, and add a prefix of 0x00 for mainnet or 0x6f for testnet
    # We also need to add a checksum of 4 bytes at the end, which is the first 4 bytes of the double SHA256 hash of the previous data
    # Finally, we encode the result with Base58 encoding

    import hashlib
    import base58

    # Hash the public key with SHA256 and RIPEMD160
    sha256_hash = hashlib.sha256(public_key_compressed).digest()
    ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()

    # Add the prefix of 0x6f for testnet (change this to 0x00 for mainnet)
    prefix = b"\x6f"
    data = prefix + ripemd160_hash

    # Add the checksum of 4 bytes at the end
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    data += checksum

    # Encode the result with Base58 encoding
    address = base58.b58encode(data).decode()
    return address


def ETH_address_generator(public_key_compressed):
    # For Ethereum, we use the standard address format, which is a hex string that starts with 0x
    # We need to hash the public key with Keccak-256 (not SHA3-256), and take the last 20 bytes as the address
    # We also need to apply checksum encoding, which means that each letter in the hex string is capitalized if the corresponding bit in the hash of the address is 1

    import sha3

    # Hash the public key with Keccak-256
    keccak_hash = sha3.keccak_256(public_key_compressed).digest()

    # Take the last 20 bytes as the address
    address_bytes = keccak_hash[-20:]

    # Convert the address to hex format and add 0x at the beginning
    address_hex = "0x" + address_bytes.hex()

    # Apply checksum encoding
    address_hash = sha3.keccak_256(address_hex.encode()).hexdigest()
    address_checksum = ""

    for i in range(len(address_hex)):
        char = address_hex[i]
        if char in "0123456789":
            # If the character is a digit, do not change it
            address_checksum += char
        else:
            # If the character is a letter, capitalize it if the corresponding bit in the hash is 1, otherwise keep it lowercase
            bit = address_hash[i]
            if bit in "89ABCDEF":
                address_checksum += char.upper()
            else:
                address_checksum += char.lower()

    address = address_checksum
    return address
