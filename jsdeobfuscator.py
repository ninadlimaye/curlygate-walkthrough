import sys
import os

def deobfuscate_files(input_dir:str):
    li = os.listdir(input_dir)
    for file in li:
        if file.endswith(".js") and file != "config.js":
            os.system(f"obfuscator-io-deobfuscator {input_dir+'/'+file} -o {input_dir + '/' + file[:-2]}deobfuscated.js")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python jsdeobfuscator.py <input_directory> \nMake sure node js and obfuscator.io module is installed.")
        exit()

    input_directory = sys.argv[1]

    deobfuscate_files(input_directory)