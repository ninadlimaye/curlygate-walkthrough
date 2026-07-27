 import base64
import sys

def xor(i: int) -> chr:
    return chr(i ^ 167 ^ 18)  # XOR logic

def process_file(input_file: str, output_file: str):
    
    # read and preprocess the Base64-encoded input
    with open(input_file, "r") as fm:
        b64 = fm.read()
        b64 = b64.replace("!", "b").replace("@", "h").replace("$", "m").replace("^", "v").replace("%", "p") 
        # b64 = b64.replace("!", "b").replace("@", "d").replace("$", "g").replace("^", "s").replace("%", "m") --> from other command line arguments
        
    # validate and decode Base64
    try:
        d64 = base64.b64decode(b64, validate=True)
    except base64.binascii.Error as e:
        print(f"Base64 decoding error: {e}")
        exit()

    # apply XOR operation and treat as bytes
    l64 = list(d64)
    result = map(xor, l64)
    f = bytes(map(ord, result))  # convert char to byte directly

    # write output
    with open(output_file, "wb") as m:
        m.write(f)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python b64decoder.py <input_file> <output_file>")
        exit()

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_file(input_file, output_file)