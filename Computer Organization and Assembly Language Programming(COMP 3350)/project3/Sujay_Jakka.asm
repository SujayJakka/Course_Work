;Sujay Jakka
;Svj0007
;Sujay_Jakka.asm
;3/22/2023
;Used tutorialspoint.com for cmp command and conditional jumps such as jnl(jump if not less) and jl(jump if less)

;This program reads a value from an array, and then places this value in another array with the location shifted by a certain amount. 

.386
.model flat,stdcall
.stack 4096
ExitProcess PROTO, dwExitCode:DWORD

.data
    shift dword 2                           ;Creates dword variable shift and sets it to the value 2
    input byte 1,2,3,4,5,6,7,8              ;Creates byte array input 
    output byte lengthof input dup(?)	    ;Creates byte array output which is uninitialized
.code
    main proc
	
    mov ecx, 0                      ; Sets ecx register as the loop variable
    mov eax, lengthof input         ; Sets eax register as the length of the array input 

    ;The loop l1 takes every value in array input and puts it in the corresponded shifted position in the array output

    l1:	

        mov ebx, ecx                ;Sets ebx to the value of ecx 
        add ebx, shift              ;Adds shift to ebx to find the array index to modify for the array output

        cmp ebx, eax                ;Compares ebx and eax to see if ebx is greater than eax
                                    ;If ebx is greater that means the value need to wrap around the array output to be put in the correct position

        jnl wrap                    ;If ebx is not less than eax it will jump to the wrap target and execute that code, if not it will execute below code

        mov edx, 0                  ;Sets edx to 0
        mov dl, [input + ecx]       ;Sets the register dl to the value of the current input array value
        mov [output + ebx], dl      ;Sets the shifted position in the array output to the input array value stored in register dl
        jmp check                   ;Jumps to target check to execute the code to see if it shall continue the loop

        
        ;Code for if the current input array value needs to wrapped around array output

        wrap:

            sub ebx, eax                ;Subtracts the value in eax from ebx to find the corresponding position in array output
   
            mov edx, 0                  ;Sets edx to 0
            mov dl, [input + ecx]       ;Sets the register dl to the value of the current input array value
            mov [output + ebx], dl      ;Sets the shifted position in the array output to the input array value stored in register dl
            jmp check                   ;Jumps to target check to execute the code to see if it shall continue the loop


        check:
            add ecx, 1                  ;Increments ecx which is the loop variable
            cmp ecx, eax                ;Compares ecx and eax values
            jl l1                       ;If exc is less than eax which is the length of the array it will continue the loop and jump to target l1, if not it will exit the loop

INVOKE ExitProcess,0
main ENDP
END main
