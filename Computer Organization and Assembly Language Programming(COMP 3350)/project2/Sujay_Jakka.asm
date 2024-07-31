.386
.model flat, stdcall
.stack 4096
ExitProcess proto, dwExitCode:dword

.data
		input BYTE 1,2,3,4,5,6,7,8
		shift BYTE 2
.code
		main proc
			; clear up the registers to make sure there is no old values inside them
			mov EAX, 0                   ; clear up EAX                       
			mov EBX, 0		             ; clear up EBX
			mov ECX, 0                   ; clear up ECX
			mov EDX, 0                   ; clear up EDX

			; setup EAX register with 1st and 2nd values from the input array
		    mov AH, [input + 0]               ; add 1st value from input into register
			add AH, shift                     ; shift the value inside the register
            mov AL, [input + 1]               ; add 2nd value from input into register
			add AL, shift                     ; shift the value inside the register
				
			; setup EBX register with 3rd and 4th values from the input array
			mov BH, [input + 2]               ; add 3rd value from input into register
			add BH, shift                     ; shift the value inside the register
            mov BL, [input + 3]               ; add 4th value from input into register
			add BL, shift                     ; shift the value inside the register

			; setup ECX register with 5th and 6th values from the input array
			mov CH, [input + 4]               ; add 5th value from input into register
			add CH, shift                     ; shift the value inside the register
            mov CL, [input + 5]               ; add 6th value from input into register
			add CL, shift                     ; shift the value inside the register

			; setup EDX register with 7th and 8th values from the input array
			mov DH, [input + 6]               ; add 7th value from input into register
			add DH, shift                     ; shift the value inside the register
            mov DL, [input + 7]               ; add 8th value from input into register
			add DL, shift                     ; shift the value inside the register

			; exit the program
			invoke ExitProcess, 0
		main endp
end main
