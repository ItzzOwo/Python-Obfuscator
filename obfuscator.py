import random
import string
import base64
import tkinter as tk
from marshal import dumps
import os, random, zlib, lzma
from tkinter import filedialog

def add_junk_code(code, junk_ratio=0.5):
    lines = code.split('\n')
    num_lines = len(lines)
    num_junk_lines = int(num_lines * junk_ratio)
    junk_lines = []
    for _ in range(num_junk_lines):
        junk_line = ' ' * random.randint(4, 8)
        length = random.randint(100, 400)
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        junk_line += '#' * random.randint(20, 40)
        final = junk_line + random_string
        junk_lines.append(final)
    for _ in range(num_junk_lines):
        index = random.randint(0, len(lines) - 1)
        lines.insert(index, junk_lines.pop())
    return '\n'.join(lines)

def generate_random_function():
    length = random.randint(100, 400)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    while random_string[0].isdigit():
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_string

def add_custom_functions(code):
    custom_functions = ""
    for _ in range(20):
        function_name = generate_random_function()
        function_code = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(50, 200)))
        while function_code[0].isdigit():
            function_code = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(50, 200)))
        custom_functions += f"""
def {function_name}():
    {function_code}
"""
    return custom_functions + code

decode_function = generate_random_function()

def encrypt_strings(code):
    strings = []
    index = 0
    while True:
        start_index = code.find('"', index)
        if start_index == -1:
            break
        end_index = code.find('"', start_index + 1)
        if end_index == -1:
            break
        strings.append(code[start_index:end_index + 1])
        index = end_index + 1
    for s in strings:
        encrypted_string = base64.b64encode(s.encode()).decode()
        code = code.replace(s, f'{decode_function}("{encrypted_string}")')

    return code

def create_decode_function():
    return f"""
def {decode_function}(encoded_string):
    import base64
    return base64.b64decode(encoded_string).decode()
"""

junk = ''.join(random.choices(string.ascii_letters + string.digits, k=200))

chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def generate_random_variable():
    random_variable = ''
    for _ in range(10):
        random_variable += random.choice(chars)
    return random_variable

def compress_text(text):
    compressed_text = zlib.compress(text.encode())
    compressed_text = lzma.compress(compressed_text)
    return compressed_text

def encrypt_with_compilation(text):
    compiled_source = compile(text, 'code', 'exec')
    marshalled_source = dumps(compiled_source)
    encrypted_code = f'{junk}="{junk}";{junk}="{junk}";{junk}="{junk}";exec(loads({marshalled_source}));{junk}="{junk}";{junk}="{junk}"'
    compressed_encrypted_code = compress_text(encrypted_code)
    final_encrypted_code = f"import zlib,lzma\nexec(zlib.decompress(lzma.decompress({compressed_encrypted_code})))"
    return final_encrypted_code

def encrypt_with_marshal(text):
    random_variable = generate_random_variable()
    compiled_code = compile(text, 'code', 'exec')
    marshalled_code = dumps(compiled_code)
    stub = f'from marshal import loads;exec(loads({marshalled_code}));'
    final_code = f'{junk}="{junk}";{junk}="{junk}";{stub}{junk}="{junk}";{junk}="{junk}";'
    return final_code

def obfuscate_file(input_file, output_file):
    print_function = generate_random_function()
    return_function = generate_random_function()
    decode_function_name = generate_random_function()
    with open(input_file, 'r') as file:
        original_code = file.read()

    original_code = add_custom_functions(original_code)
    obfuscated_code = add_junk_code(original_code)
    print_indices = [pos for pos, char in enumerate(obfuscated_code) if obfuscated_code.startswith("print(", pos)]
    for idx in reversed(print_indices):
        obfuscated_code = obfuscated_code[:idx] + f'{print_function}(' + obfuscated_code[idx + 6:]
    obfuscated_code = encrypt_strings(obfuscated_code)
    lines = obfuscated_code.split('\n')
    for i in range(len(lines)):
        if "return " in lines[i]:
            lines[i] = lines[i].replace("return ", f"{return_function}(") + ")"
    obfuscated_code = '\n'.join(lines)
    obfuscated_code = create_decode_function() + obfuscated_code
    
    custom_functions = f"""
def {print_function}(*args):
    modified_args = [arg.strip('"').strip("'") for arg in args]
    print(*modified_args)

def {return_function}(*args):
    return args
"""

    obfuscated_code = custom_functions + obfuscated_code
    obfuscated_code_base64 = base64.b64encode(obfuscated_code.encode()).decode()
    base64_executor = f"""
import base64
exec(base64.b64decode("{obfuscated_code_base64}"))
"""
    code = base64_executor
    code = encrypt_with_compilation(code)
    code = encrypt_with_marshal(code)
    with open(output_file, 'w') as file:
        file.write(code)

    print("Obfuscation complete.")

root = tk.Tk()
root.withdraw()
input_file = filedialog.askopenfilename(title="Select Input File", filetypes=(("Python files", "*.py"), ("All files", "*.*")))

if not input_file:
    print("No input file selected. Exiting.")
else:
    output_file = 'obfuscated_code.py'
    obfuscate_file(input_file, output_file)
