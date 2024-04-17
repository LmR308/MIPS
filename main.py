import pandas as pd
import csv

def load_MIPS_table(table, dict):
    for idx, row in table.iterrows():
        for j in range(len(row)):
            dict[row[j]] = (int)(j + idx * table.shape[0])
    return dict

def Hex_to_Institution(input, opcode_table, function_table, rt_table, Register_dict):
    binary = bin(int(input[2:], 16))[2:]
    num_zeros_to_add = max(0, 32 - len(binary))  # 如果你想要32位二进制，将8替换成32
    # 在二进制字符串前面添加零
    binary = "0" * num_zeros_to_add + binary
    opcode = int(binary[:6], 2)
    Hex = str('')
    if opcode == 0:#R-Type Institution
        rs, rt, rd, sa, function = int(binary[6:11], 2), int(binary[11:16], 2), int(binary[16:21], 2), int(binary[21:26], 2), int(binary[-6:], 2)
        rs, rt, rd = Register_dict[rs], Register_dict[rt], Register_dict[rd]
        Hex = Hex + str(function_table[function % int(2 ** 3)][int(function / int(2 ** 3))]) + str(' $') + rd
        if function != 0 or function != 2 or function != 3:
            Hex = Hex + str(', ') + rs
        Hex = Hex + str(', ') + rt
    elif opcode == 1:#I-Type Institution
        rs, rt, offset = int(binary[6:11], 2), int(binary[11:16], 2), int(binary[16:], 2)
        Hex = Hex + str(rt_table[rt % int(2 ** 2)][int(rt / int(2 ** 3))]) + str(' ')
        if opcode != 15:
            rs, rt = int(binary[6:11], 2), int(binary[11:16], 2)
            rs, rt = Register_dict[rs], Register_dict[rt]
            Hex = Hex + str(', ') + rs
        Hex = Hex + str(', ') + rt
    else :#J-Type Institution
        instr_index = int(binary[6:], 2)
        Hex = Hex + str(opcode_table[opcode % int(2 ** 3)][int(opcode / int(2 ** 3))])
        if opcode_table[opcode % int(2 ** 3)][int(opcode / int(2 ** 3))] == 'J' or opcode_table[opcode % int(2 ** 3)][int(opcode / int(2 ** 3))] == 'JAL':
            Hex = Hex + str(' ') + hex(instr_index)
        else :
            rs, rt, offset = int(binary[6:11], 2), int(binary[11:16], 2), int(binary[16:], 2)
            if opcode != 15:
                rs, rt = int(binary[6:11], 2), int(binary[11:16], 2)
                rs, rt = Register_dict[rs], Register_dict[rt]
                Hex = Hex + str(' $') + rs + str(', $') + rt
            Hex = Hex + str(' ') + rt
    return Hex

def Institution_to_Hex(input, opcode_table, function_table, rt_table, Register_dict, Institution_name):
    tl_institution = input.split()
    institution_name = tl_institution[0]
    Hex = str('')
    if function_table.isin([institution_name]).any().any():
        opcode = 0
    elif rt_table.isin([institution_name]).any().any():
        opcode = 1
    else:
        opcode = Institution_name[institution_name]
        if institution_name == 'J' or institution_name == 'JAL':
            institution_val = bin(int(opcode / 4) * 2 ** 28 + int(bin(int(tl_institution[1], 16))[2:], 2) + (opcode % 4 * 2 ** 26))[2:]
            num_zeros_to_add = max(0, 32 - len(institution_val))  # 如果你想要32位二进制，将8替换成32
            # 在二进制字符串前面添加零
            Hex = "0" * num_zeros_to_add + institution_val
            return Hex


if __name__ == '__main__':
    opcode_table = pd.read_excel(f'D:\学习资料\课程学习\计算机体系结构\mips\MIPS_encode_decode\MIPS_manunal.xlsx', sheet_name='opcode', header=None)
    function_table = pd.read_excel(f'D:\学习资料\课程学习\计算机体系结构\mips\MIPS_encode_decode\MIPS_manunal.xlsx', sheet_name='function', header=None)
    rt_table = pd.read_excel(f'D:\学习资料\课程学习\计算机体系结构\mips\MIPS_encode_decode\MIPS_manunal.xlsx', sheet_name='rt', header=None)
    Institution_name, Register_dict = {}, {}
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
    Institution_name = load_MIPS_table(opcode_table, Institution_name)
    Institution_name = load_MIPS_table(function_table, Institution_name)
    Institution_name = load_MIPS_table(rt_table, Institution_name)
    # result = Hex_to_Institution('0x0002001A', opcode_table, function_table, rt_table, Register_dict)
    result = Institution_to_Hex('J 0x000000', opcode_table, function_table, rt_table, Register_dict, Institution_name)
    print(result)
    # print(opcode_table.info())