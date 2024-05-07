import pandas as pd
import argparse

def load_MIPS32_manual():
    opcode_table = pd.read_excel(f'MIPS_manunal.xlsx', sheet_name='opcode',header=None)
    function_table = pd.read_excel(f'MIPS_manunal.xlsx',sheet_name='function', header=None)
    rt_table = pd.read_excel(f'MIPS_manunal.xlsx', sheet_name='rt',header=None)
    Instruction_format_table = pd.read_excel(f'table_data.xlsx',dtype=str)
    Instruction_format_table = Instruction_format_table.fillna("empty")
    Instruction_format_table.replace({'imm': 'offset'}, inplace=True)
    Instruction_name, Register_dict, Register_idx_dict, Instruction_information = {}, {}, {}, {}

    for idx, row in Instruction_format_table.iterrows():
        row[0] = row[0].replace('(', ' ')
        row[0] = row[0].replace(')', ' ')
        row[0] = row[0].replace(',', ' ')
        one_Instruction_format = row[0].split()
        name = one_Instruction_format[0]
        Instruction_information[name] = {}
        Instruction_information[name]['opcode'] = row[3]
        for va in row:
            if va == "empty":
                break
            Instruction_information[name]['func'] = va
        if len(one_Instruction_format) >= 2:
            Instruction_information[name]['format'] = [i for i in one_Instruction_format[1:]]
        else:
            Instruction_information[name]['format'] = []
    Register_dict[0] = str('zero')
    Register_dict[1] = str('at')
    Register_dict[2] = str('v0')
    Register_dict[3] = str('v1')
    for idx in range(4, 7, 1):
        Register_dict[idx] = str('a') + str(int(idx - 4))
    for idx in range(8, 15, 1):
        Register_dict[idx] = str('t') + str(int(idx - 8))
    for idx in range(16, 23, 1):
        Register_dict[idx] = str('s') + str(int(idx - 16))
    Register_dict[24] = str('t8')
    Register_dict[25] = str('t9')
    Register_dict[26] = str('k0')
    Register_dict[27] = str('k1')
    Register_dict[28] = str('gp')
    Register_dict[29] = str('sp')
    Register_dict[30] = str('fp')
    Register_dict[31] = str('ra')
    for ke, va in Register_dict.items():
        Register_idx_dict[va] = ke
    return opcode_table, function_table, rt_table, Register_dict, Register_idx_dict, Instruction_information

def Hex_to_bin(input, length):
    input = bin(input)[2:]
    num_zeros_to_add = max(0, length - len(input))
    input = "0" * num_zeros_to_add + input
    return input

def match_Instruction_format(formats, Hex, rs, rt, rd, sa, function, offset):
    for idx in range(len(formats)):
        if idx != 0:
            Hex = Hex + str(',')
        if formats[idx] == 'rs':
            Hex = Hex + str(' $') + rs
        elif formats[idx] == 'rt':
            Hex = Hex + str(' $') + rt
        elif formats[idx] == 'rd':
            Hex = Hex + str(' $') + rd
        elif formats[idx] == 'sa':
            Hex = Hex + str(' ') + sa
        else:
            Hex = Hex + str(' ') + offset
    return Hex

def Hex_to_Instruction(input, opcode_table, function_table, rt_table, Register_dict, Instruction_formation, tp):
    binary = Hex_to_bin(input, 32)
    opcode = int(binary[:6], 2)
    Instruction, rs, rt, rd, sa, function, offset = str(''), 0, 0, 0, 0, 0, 0
    if opcode == 0:#R-Type Institution
        rs, rt, rd, sa, function = int(binary[6:11], 2), int(binary[11:16], 2), int(binary[16:21], 2), str(int(binary[21:26], 2)), int(binary[-6:], 2)
        Instruction_name = str(function_table[function % int(2 ** 3)][int(function / int(2 ** 3))])
        if tp == 'name':
            rs, rt, rd = Register_dict[rs], Register_dict[rt], Register_dict[rd]
        else:
            rs, rt, rd = str(rs), str(rt), str(rd)
    elif opcode == 1:
        rs, rt, offset = int(binary[6:11], 2), int(binary[11:16], 2), str(int(binary[16:], 2))
        Instruction_name = str(rt_table[rt % int(2 ** 2)][int(rt / int(2 ** 3))])
        if tp == 'name':
            rs, rt = Register_dict[rs], Register_dict[rt]
        else:
            rs, rt = str(rs), str(rt)
    else :
        Instruction_name = str(opcode_table[opcode % int(2 ** 3)][int(opcode / int(2 ** 3))])
        if Instruction_name == 'J' or Instruction == 'JAL':
            offset = Hex_to_bin(int(binary[6:], 2), 26)
        else:
            rs, rt, offset = int(binary[6:11], 2), int(binary[11:16], 2), Hex_to_bin(int(binary[16:], 2), 16)
            if tp == 'name':
                rs, rt = Register_dict[rs], Register_dict[rt]
            else:
                rs, rt = str(rs), str(rt)
    Instruction = Instruction + Instruction_name
    formats = Instruction_formation[Instruction_name]['format']
    Instruction = match_Instruction_format(formats, Instruction, rs, rt, rd, sa, function, offset)
    return Instruction

def Instruction_to_Hex(input, Instruction_formation, Register_idx_dict, tp):
    tl_Instruction = input.split()
    Instruction_name = tl_Instruction[0]
    Hex, formats = str(''), [tl_Instruction[idx].replace(',', '') for idx in range(1, len(tl_Instruction), 1)]
    formats = [i.replace('$', '') for i in formats]
    if tp == 'name':
        name_to_idx = lambda f: [str(Register_idx_dict[x]) if i != len(f) - 1 else x for i, x in enumerate(f)]
        formats = name_to_idx(formats)
    opcode = Instruction_formation[Instruction_name]['opcode']
    if Instruction_name == 'J' or Instruction_name == 'JAL':
        instr_index = Hex_to_bin(int(tl_Instruction[1], 16), 26)
        Hex = Hex + opcode + instr_index
    elif str('offset') in Instruction_formation[Instruction_name]['format']:
        rs, rt = str('00000'), str('000000')
        for idx in range(len(formats)):
            va = Instruction_formation[Instruction_name]['format'][idx]
            if va == 'rt':
                rt = Hex_to_bin(int(formats[idx]), 5)
            elif va == 'rs':
                rs = Hex_to_bin(int(formats[idx]), 5)
            else:
                offset = Hex_to_bin(int(formats[idx]), 16)
        Hex = Hex + opcode + rs + rt + offset
    else:
        rs, rt, rd, sa = [str('00000') for _ in range(4)]
        func = Instruction_information[Instruction_name]['func']
        for idx in range(len(formats)):
            va = Instruction_formation[Instruction_name]['format'][idx]
            if va == 'rt':
                rt = Hex_to_bin(int(formats[idx]), 5)
            elif va == 'rs':
                rs = Hex_to_bin(int(formats[idx]), 5)
            elif va == 'rd':
                rd = Hex_to_bin(int(formats[idx]), 5)
            else:
                sa = Hex_to_bin(int(formats[idx]), 5)
        Hex = Hex + opcode + rs + rt + rd + sa + func
    return Hex

def test_Hex_to_Instruction(own, std):
    if len(own) != len(std):
        print('error')
    for idx in range(len(own) - 1):
        own[idx] = own[idx].replace(',', '')
        if own[idx] != std[idx]:
            print(f'error occured')

def extract_format(binary, Instruction_name, formats):
    extract_binary = binary[:6]
    for idx in range(1, len(formats), 1):
        if formats[idx] == 'rs':
            extract_binary = extract_binary + binary[6:11]
        elif formats[idx] == 'rt':
            extract_binary = extract_binary + binary[11:16]
        elif formats[idx] == 'rd':
            extract_binary = extract_binary + binary[16:21]
        elif formats[idx] == 'sa':
            extract_binary = extract_binary + binary[21:26]
        elif formats[idx] == 'offset':
            if Instruction_name == 'J' or Instruction_name == 'JAL':
                extract_binary = extract_binary + binary[6:]
            else:
                extract_binary = extract_binary + binary[16:]
    return extract_binary


def test_Instruction_to_Hex(own, std, Instruction_name, Instruction_information):
    ow = extract_format(own, Instruction_name, Instruction_information[Instruction_name]['format'])
    st = extract_format(std, Instruction_name, Instruction_information[Instruction_name]['format'])
    if ow != st:
        print(f'{ow} {st} {Instruction_name}')

def Verify_correctness(opcode_table, function_table, rt_table, Register_dict, Register_idx_dict ,Instruction):
    with open(f'test_data.txt', mode='r', encoding='utf-8') as file:
        for row in file:
            row = row.strip().split(' ')
            Hex = str('0x') + str(row[0])
            std_institution = [row[i] for i in range(1, len(row))]
            Hex = int(Hex[2:], 16)
            result = Hex_to_Instruction(Hex, opcode_table, function_table, rt_table, Register_dict,Instruction, tp='number')
            binary = Instruction_to_Hex(result, Instruction, Register_idx_dict, tp='number')
            result = result.split(' ')
            test_Hex_to_Instruction(result, std_institution)
            test_Instruction_to_Hex(binary, Hex_to_bin(Hex, 32), result[0], Instruction)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='0b00000000000100110100000011000000', help='The data to be converted')
    parser.add_argument('--type', type=str, default='bintoins', help='Data format conversion type')
    parser.add_argument('--format', type=str, default='name', help='Assembly instruction register format')
    opt = parser.parse_args()

    opcode_table, function_table, rt_table, Register_dict, Register_idx_dict, Instruction_information = load_MIPS32_manual()
    Verify_correctness(opcode_table, function_table, rt_table, Register_dict, Register_idx_dict, Instruction_information)
    if opt.type == str('bintoins'):
        if opt.input[:2] == str('0b'):
            input = int(opt.input[2:], 2)
        if opt.input[:2] == str('0x'):
            input = int(opt.input[2:], 16)
        convert_result = Hex_to_Instruction(input, opcode_table, function_table, rt_table, Register_dict,Instruction_information, tp=opt.format)
    else:
        convert_result = Instruction_to_Hex(opt.input, Instruction_information, Register_idx_dict, tp=opt.format)
    print(f'the input data is {opt.input}')
    print(f'the converted data is {convert_result}')
