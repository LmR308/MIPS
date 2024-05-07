var rFormat = 'op rs rt rd sa funct'
var iFormat = 'op rs rt imm'
var jFormat = 'op target'

var registerTableName = {
	'00000': '$zero',
	'00001': '$at',
	'00010': '$v0',
	'00011': '$v1',
	'00100': '$a0',
	'00101': '$a1',
	'00110': '$a2',
	'00111': '$a3',
	'01000': '$t0',
	'01001': '$t1',
	'01010': '$t2',
	'01011': '$t3',
	'01100': '$t4',
	'01101': '$t5',
	'01110': '$t6',
	'01111': '$t7',
	10000: '$s0',
	10001: '$s1',
	10010: '$s2',
	10011: '$s3',
	10100: '$s4',
	10101: '$s5',
	10110: '$s6',
	10111: '$s7',
	11000: '$t8',
	11001: '$t9',
	11010: '$k0',
	11011: '$k1',
	11100: '$gp',
	11101: '$sp',
	11110: '$fp',
	11111: '$ra',
}

var registerTableNum = {
	'00000': '$0',
	'00001': '$1',
	'00010': '$2',
	'00011': '$3',
	'00100': '$4',
	'00101': '$5',
	'00110': '$6',
	'00111': '$7',
	'01000': '$8',
	'01001': '$9',
	'01010': '$10',
	'01011': '$11',
	'01100': '$12',
	'01101': '$13',
	'01110': '$14',
	'01111': '$15',
	10000: '$16',
	10001: '$17',
	10010: '$18',
	10011: '$19',
	10100: '$20',
	10101: '$21',
	10110: '$22',
	10111: '$23',
	11000: '$24',
	11001: '$25',
	11010: '$26',
	11011: '$27',
	11100: '$28',
	11101: '$29',
	11110: '$30',
	11111: '$31',
}

var hexTable = {
	0: '0000',
	1: '0001',
	2: '0010',
	3: '0011',
	4: '0100',
	5: '0101',
	6: '0110',
	7: '0111',
	8: '1000',
	9: '1001',
	a: '1010',
	b: '1011',
	c: '1100',
	d: '1101',
	e: '1110',
	f: '1111',
	A: '1010',
	B: '1011',
	C: '1100',
	D: '1101',
	E: '1110',
	F: '1111',
}

var registerToBinary = {
	$zero: '00000',
	$at: '00001',
	$v0: '00010',
	$v1: '00011',
	$a0: '00100',
	$a1: '00101',
	$a2: '00110',
	$a3: '00111',
	$t0: '01000',
	$t1: '01001',
	$t2: '01010',
	$t3: '01011',
	$t4: '01100',
	$t5: '01101',
	$t6: '01110',
	$t7: '01111',
	$s0: '10000',
	$s1: '10001',
	$s2: '10010',
	$s3: '10011',
	$s4: '10100',
	$s5: '10101',
	$s6: '10110',
	$s7: '10111',
	$t8: '11000',
	$t9: '11001',
	$k0: '11010',
	$k1: '11011',
	$gp: '11100',
	$sp: '11101',
	$fp: '11110',
	$ra: '11111',
	$0: '00000',
	$1: '00001',
	$2: '00010',
	$3: '00011',
	$4: '00100',
	$5: '00101',
	$6: '00110',
	$7: '00111',
	$8: '01000',
	$9: '01001',
	$10: '01010',
	$11: '01011',
	$12: '01100',
	$13: '01101',
	$14: '01110',
	$15: '01111',
	$16: '10000',
	$17: '10001',
	$18: '10010',
	$19: '10011',
	$20: '10100',
	$21: '10101',
	$22: '10110',
	$23: '10111',
	$24: '11000',
	$25: '11001',
	$26: '11010',
	$27: '11011',
	$28: '11100',
	$29: '11101',
	$30: '11110',
	$31: '11111',
	zero: '00000',
	at: '00001',
	v0: '00010',
	v1: '00011',
	a0: '00100',
	a1: '00101',
	a2: '00110',
	a3: '00111',
	t0: '01000',
	t1: '01001',
	t2: '01010',
	t3: '01011',
	t4: '01100',
	t5: '01101',
	t6: '01110',
	t7: '01111',
	s0: '10000',
	s1: '10001',
	s2: '10010',
	s3: '10011',
	s4: '10100',
	s5: '10101',
	s6: '10110',
	s7: '10111',
	t8: '11000',
	t9: '11001',
	k0: '11010',
	k1: '11011',
	gp: '11100',
	sp: '11101',
	fp: '11110',
	ra: '11111',
}

var opcodeTable = {
	'000000': 'SPECIAL',
	'000001': 'REGIMM',
	'000010': 'J',
	'000011': 'JAL',
	'000100': 'BEQ',
	'000101': 'BNE',
	'000110': 'BLEZ',
	'000111': 'BGTZ',
	'001000': 'ADDI',
	'001001': 'ADDIU',
	'001010': 'SLTI',
	'001011': 'SLTIU',
	'001100': 'ANDI',
	'001101': 'ORI',
	'001110': 'XORI',
	'001111': 'LUI',
	100000: 'LB',
	100001: 'LH',
	100010: 'LWL',
	100011: 'LW',
	100100: 'LBU',
	100101: 'LHU',
	101000: 'SB',
	101001: 'SH',
	101011: 'SW',
}

var functTable = {
	'000000': 'SLL',
	'000010': 'SRL',
	'000011': 'SRA',
	'000100': 'SLLV',
	'000110': 'SRLV',
	'000111': 'SRAV',
	'001000': 'JR',
	'001001': 'JALR',
	'001100': 'SYSCALL',
	'001101': 'BREAK',
	'010000': 'MFHI',
	'010001': 'MTHI',
	'010010': 'MFLO',
	'010011': 'MTLO',
	'011000': 'MULT',
	'011001': 'MULTU',
	'011010': 'DIV',
	'011011': 'DIVU',
	100000: 'ADD',
	100001: 'ADDU',
	100010: 'SUB',
	100011: 'SUBU',
	100100: 'AND',
	100101: 'OR',
	100110: 'XOR',
	100111: 'NOR',
	101010: 'SLT',
	101011: 'SLTU',
}

var formatTable = {
	// ALU
	ADD: 'op rd rs rt',
	ADDI: 'op rt rs imm',
	ADDIU: 'op rt rs imm',
	ADDU: 'op rd rs rt',
	AND: 'op rd rs rt',
	ANDI: 'op rt rs imm',
	LUI: 'op rt imm',
	NOR: 'op rd rs rt',
	OR: 'op rd rs rt',
	ORI: 'op rt rs imm',
	SLT: 'op rd rs rt',
	SLTI: 'op rt rs imm',
	SLTIU: 'op rt rs imm',
	SLTU: 'op rd rs rt',
	SUB: 'op rd rs rt',
	SUBU: 'op rd rs rt',
	XOR: 'op rd rs rt',
	XORI: 'op rt rs imm',
	// SHIFTER
	SLL: 'op rd rt sa',
	SLLV: 'op rd rt rs',
	SRA: 'op rd rt sa',
	SRAV: 'op rd rt rs',
	SRL: 'op rd rt sa',
	SRLV: 'op rd rt rs',
	// MULTIPLY
	DIV: 'op rs rt',
	DIVU: 'op rs rt',
	MFHI: 'op rd',
	MFLO: 'op rd',
	MTHI: 'op rs',
	MTLO: 'op rs',
	MULT: 'op rs rt',
	MULTU: 'op rs rt',
	// BRANCH
	BEQ: 'op rs rt offset',
	BGEZ: 'op rs offset',
	BGEZAL: 'op rs offset',
	BGTZ: 'op rs offset',
	BLEZ: 'op rs offset',
	BLTZ: 'op rs offset',
	BLTZAL: 'op rs offset',
	BNE: 'op rs rt offset',
	BREAK: 'op',
	J: 'op target',
	JAL: 'op target',
	JALR: 'op rs',
	JR: 'op rs',
	MFC0: 'op rt rd',
	MTC0: 'op rt rd',
	SYSCALL: 'op',
	// MEMORY
	LB: 'op rt offset(rs)',
	LBU: 'op rt offset(rs)',
	LH: 'op rt offset(rs)',
	LHU: 'op rt offset(rs)',
	LW: 'op rt offset(rs)',
	SB: 'op rt offset(rs)',
	SH: 'op rt offset(rs)',
	SW: 'op rt offset(rs)',
}

function hexToInst(inputString = '0x014B4820') {
	//
	// CLEAR OUTPUT REGION
	// 清除输出区域
	// document.getElementById('output').innerHTML = ''
	// document.getElementById('test').innerHTML = ''
	// document.getElementById('outInst').innerHTML = ''
	//
	// INPUT PARSING (HEX TO BINARY)
	// 输入解析（十六进制转二进制）
	// var inputString = document.getElementById('hex').value
	var inputString = inputString

	if (inputString.length == 10) {
		inputString = inputString.replace('0x', '')
		inputString = inputString.replace('0X', '')
	}
	if (inputString.length != 8) {
		// 错误，请检查输入是否具有正确的位数
		// document.getElementById('output').innerHTML =
		// 	'Error, check that input has correct number of bits'

		return 'Error, check that input has correct number of bits'
	}
	var i = '',
		parsedString = ''
	for (i = 0; i < inputString.length; i += 1) {
		if (hexTable.hasOwnProperty(inputString[i]) == false) {
			parsedString = false
		} else {
			parsedString = parsedString + hexTable[inputString[i]]
		}
	}
	if (parsedString == false) {
		// 错误，请检查输入是否为有效十六进制数值
		// document.getElementById('output').innerHTML =
		// 	'Error, check that input is valid hex'
		return 'Error, check that input is valid hex'
	}

	//
	// DETERMINE INSTRUCTION (IF VALID)
	// 确定指令（如果有效）
	var opcode = parsedString.substring(0, 6)
	var operation = ''

	if (opcodeTable.hasOwnProperty(opcode)) {
		if (opcode == '000000') {
			operation = parsedString.substring(
				parsedString.length - 6,
				parsedString.length
			)
			operation = functTable[operation]
		} else {
			operation = opcodeTable[opcode]
		}
	} else {
		// 未识别的操作码
		// document.getElementById('output').innerHTML = 'Opcode not recognized'
		return 'Opcode not recognized'
	}

	//
	// DETERMINE FIELD VALUES BASED ON INSTRUCTION TYPE
	// 根据指令类型确定字段值

	var instructionOut = ''

	var rs = '',
		rd = '',
		rt = '',
		shamt = '',
		imm = '',
		target = ''
	var rs_c = '',
		rd_c = '',
		rt_c = '',
		shamt_c = '',
		imm_c = '',
		target_c = ''

	rs = parsedString.substring(6, 11)
	rt = parsedString.substring(11, 16)
	rd = parsedString.substring(16, 21)
	shamt = parsedString.substring(21, 26)
	imm = parsedString.substring(16)
	target = parsedString.substring(6)

	shamt_c = '0x' + parseInt(shamt, 2).toString(16).toUpperCase()
	imm_c = '0x' + parseInt(imm, 2).toString(16).toUpperCase()
	target_c = '0x' + parseInt(target, 2).toString(16).toUpperCase()

	// Depending on desired register convention, prep fields for output
	// 根据所需的寄存器约定，准备字段以供输出
	// if (1) {
		rs_c = registerTableNum[rs]
		rt_c = registerTableNum[rt]
		rd_c = registerTableNum[rd]
	// } else {
	// 	rs_c = registerTableName[rs]
	// 	rt_c = registerTableName[rt]
	// 	rd_c = registerTableName[rd]
	// }
	// if (document.getElementById('num_rad').checked) {
	// 	rs_c = registerTableNum[rs]
	// 	rt_c = registerTableNum[rt]
	// 	rd_c = registerTableNum[rd]
	// } else {
	// 	rs_c = registerTableName[rs]
	// 	rt_c = registerTableName[rt]
	// 	rd_c = registerTableName[rd]
	// }

	//
	// GET OUTPUT TEMPLATE FOR OPERATION AND SUBSTITUE REAL FIELD VALUES
	// 获取操作的输出模板，并替换实际字段值
	instructionOut = formatTable[operation.toUpperCase()]
	instructionOut = instructionOut.replace('op', operation.toString())
	instructionOut = instructionOut.replace('rd', rd_c.toString())
	instructionOut = instructionOut.replace('rs', rs_c.toString())
	instructionOut = instructionOut.replace('rt', rt_c.toString())
	instructionOut = instructionOut.replace('sa', shamt_c.toString())
	instructionOut = instructionOut.replace('target', target_c.toString())
	instructionOut = instructionOut.replace('offset', imm_c.toString())
	instructionOut = instructionOut.replace('imm', imm_c.toString())

	//
	// OUTPUT RESULTS TO PAGE
	// 将结果输出到页面
	// document.getElementById('resultsHeader').innerHTML = 'Results:'
	// document.getElementById('outInst').innerHTML =
	// 	'Instruction: ' + instructionOut
	// document.getElementById('output').innerHTML = 'Hex: 0x' + inputString
	// document.getElementById('test').innerHTML = 'Binary: ' + parsedString

	// 输出结果
	console.log(instructionOut)
	return instructionOut
}
hexToInst()
