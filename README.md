# Computer Architecture Experiment
## Project background
This project achieved Institution encode and decode based on MIPS32 manual.  
It implements the mutual conversion between assembly instructions and binary encoding.  
## Project File Function Description
The get_table.py is used to Crawling MIPS Opcode Reference information from web pages[http://mipsconverter.com/opcodes.html] to generate table_data.xlsx.  
The hexToInst.js is used to generate test data for binary encoding and corresponding assembly instruction representations through the MIPS32 binary and assembly instruction converter on the webpage[http://mipsconverter.com/instruction.html] and generate test_data.txt for tesing.  
This file is generated by Adobe ACrboat's PDF extraction function, which extracts the table information of MIPS IV Architecture from mips isa. pdf into Excel.  
## Note:  
We specify that the assembly instruction format follows the assembly representation definition.  
eg.add $s1,$t0,$s4 or add $17,$8,$20.  

The data flow diagram of this project is shown below:![数据流图](数据流图.png)