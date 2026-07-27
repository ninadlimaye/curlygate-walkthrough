import urllib.request
import json
import sys
import re

def base58_decode(encoded: str) -> bytes:
    """
    decodes a Base58-encoded string into a byte string.

    :param encoded: Base58-encoded string
    :return: Decoded byte string
    :raises ValueError: If the string contains invalid Base58 characters
    """
    base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base = len(base58_chars)
    char_map = {char: index for index, char in enumerate(base58_chars)}
    
    # convert Base58 string to an integer
    decoded_int = 0
    for char in encoded:
        if char not in char_map:
            raise ValueError(f"Invalid character '{char}' in Base58 string.")
        decoded_int = decoded_int * base + char_map[char]
    
    # convert the integer to a byte string
    # calculate the minimum number of bytes needed to store the integer
    num_bytes = (decoded_int.bit_length() + 7) // 8
    decoded_bytes = decoded_int.to_bytes(num_bytes, byteorder='big')
    
    # add padding for leading "1"s (which encode as \x00 bytes)
    num_leading_zeros = len(encoded) - len(encoded.lstrip('1'))
    return b'\x00' * num_leading_zeros + decoded_bytes
    
    return decoded_value

def getc2(walletAddr:str, outfile:str):
    try: 
        res = urllib.request.urlopen(f"https://blockstream.info/api/address/{walletAddr}/txs").read()
        response_json = json.loads(res)
        
        with open(outfile, "w") as out:
            for transaction in response_json:
                try:
                    domain = re.findall(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]",base58_decode(transaction["vout"][0]["scriptpubkey_address"]).decode("utf-8",errors="ignore"))[0]
                    out.write(domain + "\n")
                except ValueError:
                    continue
                except IndexError:
                    continue
    except Exception as e:
        print("An exception has occured: ", e)


# bc1qvmvz53hdauzxuhs7dkm775tlqtd9vpk8ux7mqj
if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print("Usage: python getc2list.py <wallet_address> <output_file>\nblockchain wallet address\n")
        exit()
    walletAddr = sys.argv[1]
    outfile = sys.argv[2]
    getc2(walletAddr, outfile)


    

    