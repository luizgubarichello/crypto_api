import coincurve
import hashlib
import base58
import sha3

# Define an abstract base class for address generators
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
    
    def generate_address(self):
        # Define an abstract method for generating the address
        raise NotImplementedError("This method must be implemented by subclasses")

# Define a subclass for Bitcoin address generator
class BTCAddressGenerator(AddressGenerator):
    def generate_address(self):
        # For Bitcoin, we use P2SH-P2WPKH format, which is a SegWit address that starts with 2 or 3
        # We need to hash the public key with SHA256 and RIPEMD160, and add a prefix of 0x00 for mainnet or 0x6f for testnet
        # We also need to add a checksum of 4 bytes at the end, which is the first 4 bytes of the double SHA256 hash of the previous data
        # Finally, we encode the result with Base58 encoding

        # Hash the public key with SHA256 and RIPEMD160
        sha256_hash = hashlib.sha256(self.public_key).digest()
        ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()

        # Add the prefix of 0x6f for testnet (change this to 0x00 for mainnet)
        prefix = b"\x6f"
        data = prefix + ripemd160_hash

        # Add the checksum of 4 bytes at the end
        checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
        data += checksum

        # Encode the result with Base58 encoding
        address = base58.b58encode(data).decode()
        
        # Return the address and the private key as a tuple
        return address, self.private_key

# Define a subclass for Ethereum address generator
class ETHAddressGenerator(AddressGenerator):
    def generate_address(self):
        # For Ethereum, we use the standard address format, which is a hex string that starts with 0x
        # We need to hash the public key with Keccak-256 (not SHA3-256), and take the last 20 bytes as the address
        # We also need to apply checksum encoding, which means that each letter in the hex string is capitalized if the corresponding bit in the hash of the address is 1

        # Hash the public key with Keccak-256
        keccak_hash = sha3.keccak_256(self.public_key).digest()

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
        
         # Return the address and the private key as a tuple
        return address, self.private_key

# Define a factory function that returns an instance of an appropriate subclass based on the coin parameter
def get_address_generator(coin):
    if coin == "BTC":
       return BTCAddressGenerator()
    elif coin == "ETH":
       return ETHAddressGenerator()
    else:
       raise ValueError(f"Unsupported coin: {coin}")
