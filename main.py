import pandas as pd
import argparse

def load_MIPS32_manual():
    opcode_table = pd.read_excel(f'MIPS_manunal.xlsx', sheet_name='opcode',header=None)
    function_table = pd.read_excel(f'MIPS_manunal.xlsx',sheet_name='function', header=None)
    rt_table = pd.read_excel(f'MIPS_manunal.xlsx', sheet_name='rt',header=None)
    Institution_format_table = pd.read_excel(f'table_data.xlsx',dtype=str)
    Institution_format_table = Institution_format_table.fillna("empty")
    Institution_format_table.replace({'imm': 'offset'}, inplace=True)
    Institution_name, Register_dict, Register_idx_dict, Institution_information = {}, {}, {}, {}

    for idx, row in Institution_format_table.iterrows():
        row[0] = row[0].replace('(', ' ')
        row[0] = row[0].replace(')', ' ')
        row[0] = row[0].replace(',', ' ')
        one_institution_format = row[0].split()
        name = one_institution_format[0]
        Institution_information[name] = {}
        Institution_information[name]['opcode'] = row[3]
        for va in row:
            if va == "empty":
                break
            Institution_information[name]['func'] = va
        if len(one_institution_format) >= 2:
            Institution_information[name]['format'] = [i for i in one_institution_format[1:]]
        else:
            Institution_information[name]['format'] = []
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
    return opcode_table, function_table, rt_table, Register_dict, Register_idx_dict, Institution_information

def Hex_to_bin(input, length):
    input = bin(input)[2:]
    num_zeros_to_add = max(0, length - len(input))
    input = "0" * num_zeros_to_add + input
    return input

def match_institution_format(formats, Hex, rs, rt, rd, sa, function, offset):
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

def Hex_to_Institution(input, opcode_table, function_table, rt_table, Register_dict, Intitution_formation, tp):
    binary = Hex_to_bin(input, 32)
    opcode = int(binary[:6], 2)
    Institution, rs, rt, rd, sa, function, offset = str(''), 0, 0, 0, 0, 0, 0
    if opcode == 0:#R-Type Institution
        rs, rt, rd, sa, function = int(binary[6:11], 2), int(binary[11:16], 2), int(binary[16:21], 2), str(int(binary[21:26], 2)), int(binary[-6:], 2)
        institution_name = str(function_table[function % int(2 ** 3)][int(function / int(2 ** 3))])
        if tp == 'name':
            rs, rt, rd = Register_dict[rs], Register_dict[rt], Register_dict[rd]
        else:
            rs, rt, rd = str(rs), str(rt), str(rd)
    elif opcode == 1:
        rs, rt, offset = int(binary[6:11], 2), int(binary[11:16], 2), str(int(binary[16:], 2))
        institution_name = str(rt_table[rt % int(2 ** 2)][int(rt / int(2 ** 3))])
        if tp == 'name':
            rs, rt = Register_dict[rs], Register_dict[rt]
        else:
            rs, rt = str(rs), str(rt)
    else :
        institution_name = str(opcode_table[opcode % int(2 ** 3)][int(opcode / int(2 ** 3))])
        if institution_name == 'J' or institution_name == 'JAL':
            offset = Hex_to_bin(int(binary[6:], 2), 26)
        else:
            rs, rt, offset = int(binary[6:11], 2), int(binary[11:16], 2), Hex_to_bin(int(binary[16:], 2), 16)
            if tp == 'name':
                rs, rt = Register_dict[rs], Register_dict[rt]
            else:
                rs, rt = str(rs), str(rt)
    Institution = Institution + institution_name
    formats = Intitution_formation[institution_name]['format']
    Institution = match_institution_format(formats, Institution, rs, rt, rd, sa, function, offset)
    return Institution

def Institution_to_Hex(input, Institution_formation, Register_idx_dict, tp):
    tl_institution = input.split()
    institution_name = tl_institution[0]
    Hex, formats = str(''), [tl_institution[idx].replace(',', '') for idx in range(1, len(tl_institution), 1)]
    formats = [i.replace('$', '') for i in formats]
    if tp == 'name':
        name_to_idx = lambda f: [str(Register_idx_dict[x]) if i != len(f) - 1 else x for i, x in enumerate(f)]
        formats = name_to_idx(formats)
    opcode = Institution_formation[institution_name]['opcode']
    if institution_name == 'J' or institution_name == 'JAL':
        instr_index = Hex_to_bin(int(tl_institution[1], 16), 26)
        Hex = Hex + opcode + instr_index
    elif str('offset') in Institution_formation[institution_name]['format']:
        rs, rt = str('00000'), str('000000')
        for idx in range(len(formats)):
            va = Institution_formation[institution_name]['format'][idx]
            if va == 'rt':
                rt = Hex_to_bin(int(formats[idx]), 5)
            elif va == 'rs':
                rs = Hex_to_bin(int(formats[idx]), 5)
            else:
                offset = Hex_to_bin(int(formats[idx]), 16)
        Hex = Hex + opcode + rs + rt + offset
    else:
        rs, rt, rd, sa = [str('00000') for _ in range(4)]
        func = Institution_information[institution_name]['func']
        for idx in range(len(formats)):
            va = Institution_formation[institution_name]['format'][idx]
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

def test_Hex_to_Institution(own, std):
    if len(own) != len(std):
        print('error')
    for idx in range(len(own) - 1):
        own[idx] = own[idx].replace(',', '')
        if own[idx] != std[idx]:
            print(f'error occured')

def extract_format(binary, institution_name, formats):
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
            if institution_name == 'J' or institution_name == 'JAL':
                extract_binary = extract_binary + binary[6:]
            else:
                extract_binary = extract_binary + binary[16:]
    return extract_binary


def test_Institution_to_Hex(own, std, institution_name, Institution_information):
    ow = extract_format(own, institution_name, Institution_information[institution_name]['format'])
    st = extract_format(std, institution_name, Institution_information[institution_name]['format'])
    if ow != st:
        print(f'{ow} {st} {institution_name}')

def Verify_correctness(opcode_table, function_table, rt_table, Register_dict, Register_idx_dict ,Institution_information):
    with open(f'test_data.txt', mode='r', encoding='utf-8') as file:
        for row in file:
            row = row.strip().split(' ')
            Hex = str('0x') + str(row[0])
            std_institution = [row[i] for i in range(1, len(row))]
            Hex = int(Hex[2:], 16)
            result = Hex_to_Institution(Hex, opcode_table, function_table, rt_table, Register_dict,Institution_information, tp='number')
            binary = Institution_to_Hex(result, Institution_information, Register_idx_dict, tp='number')
            result = result.split(' ')
            test_Hex_to_Institution(result, std_institution)
            test_Institution_to_Hex(binary, Hex_to_bin(Hex, 32), result[0], Institution_information)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='0b00000000000100110100000011000000', help='The data to be converted')
    parser.add_argument('--type', type=str, default='bintoins', help='Data format conversion type')
    parser.add_argument('--format', type=str, default='name', help='Assembly instruction register format')
    opt = parser.parse_args()

    opcode_table, function_table, rt_table, Register_dict, Register_idx_dict, Institution_information = load_MIPS32_manual()
    # Verify_correctness(opcode_table, function_table, rt_table, Register_dict, Register_idx_dict, Institution_information)
    if opt.type == str('bintoins'):
        if opt.input[:2] == str('0b'):
            input = int(opt.input[2:], 2)
        if opt.input[:2] == str('0x'):
            input = int(opt.input[2:], 16)
        convert_result = Hex_to_Institution(input, opcode_table, function_table, rt_table, Register_dict,Institution_information, tp=opt.format)
    else:
        convert_result = Institution_to_Hex(opt.input, Institution_information, Register_idx_dict, tp=opt.format)
    print(f'the input data is {opt.input}')
    print(f'the converted data is {convert_result}')
