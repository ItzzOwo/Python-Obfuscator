# Python Code Obfuscator

This Python script provides functionality to obfuscate Python code, making it more difficult to understand while maintaining its functionality. It employs various techniques such as adding junk code, encrypting strings, and generating random functions to obscure the original code.

## Usage

1. **Input File Selection**: Run the script and select the Python file you want to obfuscate using the file dialog that appears.

2. **Output**: The obfuscated code will be saved in a file named `obfuscated_code.py` in the same directory as the input file.

## Dependencies

- Python 3.x
- tkinter (for file dialog)

## Important Note

This script utilizes advanced obfuscation techniques which may not be compatible with certain Python scripts, especially those employing complex dependencies or advanced syntax structures.
## Disclaimer

This script is intended for educational purposes and should only be used on code for which you have appropriate authorization. The authors take no responsibility for any misuse of this tool.

## How It Works

The script performs the following steps to obfuscate the code:

1. **Adding Junk Code**: Random junk lines are inserted into the code to increase complexity and make it harder to understand.

2. **String Encryption**: String literals within the code are encrypted using base64 encoding, making them unreadable in the source code.

3. **Custom Function Generation**: Random custom functions are generated and added to the code, further increasing complexity.

4. **Compression**: The obfuscated code is compressed using zlib and lzma to reduce its size and make it harder to analyze.

5. **Compilation and Marshalling**: The obfuscated code is compiled and marshalled to binary format, making it more difficult to reverse engineer.

6. **Final Obfuscation**: Additional obfuscation techniques, such as adding random variable names and function replacements, are applied to make the code even more obscure.
