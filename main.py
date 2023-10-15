func_choose = str(input("Choose function: [E]ncrypt/[D]ecrypt: "))
func_choose = func_choose.upper()

base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def base64_encode():
    input_file = input('Name of input file: ')
    output_file = input('Name of output file (without extension): ') + '.base64'

    if not output_file:
        output_file = input_file.replace('.txt', '.base64')

    with open(input_file, 'r', encoding='UTF-8') as file:
        open_text = file.readlines()
        for i in range(len(open_text)):
            if open_text[i].endswith("\n"):
                open_text[i] = open_text[i].rstrip("\n")

        message = []
        for item in open_text:
            parts = item.split('-')
            if parts[0].strip():
                message.append(parts[0].strip())
            if len(parts) > 1:
                second_part = parts[1].strip()
                if second_part:
                    message.append('-' + second_part)

    of_write = open(output_file, 'w', encoding='UTF-8')

    results = []

    for msg in message:
        if msg.startswith('-'):
            if len(msg) > 76:
                chunks = [msg[0:76]]
                chunks.extend(['-' + msg[i:i + 75] for i in range(76, len(msg), 75)])
                results.extend(chunks)
            else:
                results.append(msg)
        else:
            if isinstance(msg, str):
                msg_bytes = b""

                for char in msg:
                    char_bytes = bytes(char, 'utf-8')
                    msg_bytes += char_bytes

                msg = msg_bytes

            result = ""

            for i in range(0, len(msg), 3):
                chunk = msg[i:i + 3]
                byte1 = chunk[0]
                byte2 = chunk[1] if len(chunk) > 1 else 0
                byte3 = chunk[2] if len(chunk) > 2 else 0

                index1 = (byte1 >> 2) & 0x3F
                index2 = ((byte1 << 4 | (byte2 >> 4)) & 0x3F)
                index3 = ((byte2 << 2 | (byte3 >> 6)) & 0x3F)
                index4 = byte3 & 0x3F

                result += (base64_alphabet[index1] + base64_alphabet[index2] +
                           base64_alphabet[index3] + base64_alphabet[index4])

            if len(msg) % 3 == 1:
                result = result[:-2] + '=='
            elif len(msg) % 3 == 2:
                result = result[:-1] + '='

            results.extend([result[i:i + 76] for i in range(0, len(result), 76)])

    for line in results:
        of_write.write(line + '\n')

    print('Encrypted success')


def base64_decode():
    input_file = input('Name of input file: ')
    input_file_name = input_file.replace('.base64', '')
    user_input = input(f"Would you like to enter a new name for saving or agree with {input_file_name}? (y) or (n)? ")

    if user_input == 'y':
        output_file = input_file_name + '.txt'
    elif user_input == 'n':
        output_file = input("Enter the file name: ") + '.txt'
    else:
        print("Unable to determine your request")
        return

    with open(input_file, 'r', encoding='UTF-8') as file:
        open_text = file.readlines()
        for i in range(len(open_text)):
            if open_text[i].endswith("\n"):
                open_text[i] = open_text[i].rstrip("\n")

    of_write = open(output_file, 'w', encoding='UTF-8')

    decoding_table = {base64_alphabet[i]: i for i in range(64)}

    buffer = 0
    buffer_length = 0
    result = []

    for line_counter, line in enumerate(open_text):
        if len(line) != 76 and line_counter != len(open_text) - 1:
            print(f'Line len error!\nLine: {line_counter + 1}\nLen: {len(line)}\n')
            exit()
        else:
            if line.startswith('-'):
                result.append(line)
            else:
                for char_counter, char in enumerate(line):
                    if line_counter != len(open_text) - 1 and char == '=':
                        print(f'Padding error\nLine: {line_counter + 1}\nsymbol: {char_counter + 1}\n')
                        exit()

                    if line_counter == len(open_text) - 1:
                        without_last_two = line[:-2]
                        last_two = line[-2:]
                        if '=' in without_last_two:
                            position = without_last_two.index('=')
                            print(f'Padding error\nLine: {line_counter + 1}\nsymbol: {position + 1}\n')
                            exit()
                        elif last_two[0] == '=' and last_two[1] != '=':
                            position = len(without_last_two)
                            print(f'Padding error\nLine: {line_counter + 1}\nsymbol: {position + 1}\n')
                            exit()

                    if char not in base64_alphabet and char != '=':
                        print(f'Value error!\nLine: {line_counter + 1} symbol: ({char_counter + 1})\n'
                              f'Incorrect input symbol: ("{char}")')
                        exit()

                    char_index = decoding_table.get(char)
                    if char_index is not None:
                        buffer = (buffer << 6) | char_index
                        buffer_length += 6

                        while buffer_length >= 8:
                            result.append(chr((buffer >> (buffer_length - 8)) & 0xFF))
                            buffer_length -= 8
                            buffer &= (1 << buffer_length) - 1

    for line in result:
        of_write.write(line)

    print('Decrypted successfully')


if __name__ == '__main__':
    if func_choose == 'E':
        base64_encode()
    elif func_choose == 'D':
        base64_decode()
    else:
        print('Input error. Please, try again.\n')
