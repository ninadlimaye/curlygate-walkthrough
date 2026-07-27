import base64
import sys
import os
import re
def decode_powershell_hashlist(encoded_hashlist: str, outfile:str, extractFiles:bool, extDirectory:str):
    
    # parse PowerShell hash table
    encoded_hashlist = encoded_hashlist[2:-2]
    
    pairs = encoded_hashlist.split('),@(')
    if len(pairs) == 1:
        print("hash table format not recognized")
        exit()

    # create directory if it doesn't exist
    if extractFiles and extDirectory != None:
        try:
            os.mkdir(extDirectory)
        except FileExistsError:
            pass
        except Exception as e:
            print(f"couldn't create directory: {e}")
            exit()

    x = open(outfile, "wb")

    # initialize Python dictionary to store decoded key-value pairs
    decoded_dict = {}
    for pair in pairs:
        # remove remaining parentheses and split the key-value pair
        key_b64, val_b64 = pair.split(',')
        
        # decode Base64 values
        key = base64.b64decode(key_b64.strip("'"))
        value = base64.b64decode(val_b64.strip("'"))
        x.write(key + b"\n")
        # extract files to directory if option selected
        if extractFiles and extDirectory is not None:
            fName = re.sub(r"[\\/]","_", key.decode("utf-8"))

            filePath = extDirectory + "/" + fName
            open(filePath, "wb").write(value)
        # add to dictionary
        decoded_dict[key] = value
    
    return decoded_dict

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 5:
        print("Usage: python hashlistdecode.py <input_file> <output_file>\nFilenames are stored in <output_file>\nOptions: \n\tA - extract all files from table to <output_directory> \nUsage: python script.py <input_file> <output_file> A <output_directory>")
        exit()
    filename = sys.argv[1]
    outfile = sys.argv[2]
    if len(sys.argv) == 5 and sys.argv[3].strip().upper() == "A":
        extractFiles = True
        extDirectory = sys.argv[4]
    else:
        extractFiles = False
        extDirectory = None
    
    with open(f"{filename}","r") as m:
        powershell_hashlist = m.read()

    # run the function and print the result
    decoded_hashlist = decode_powershell_hashlist(powershell_hashlist, outfile, extractFiles, extDirectory)
    print("Execution Completed")