.text
.global _start

_start:
    MOV R0, #15       @ Primer n�mero
    MOV R1, #5        @ Segundo n�mero

    ADD R2, R0, R1    @ R2 = 15 + 5 = 20
    SUB R3, R0, R1    @ R3 = 15 - 5 = 10

    CMP R2, R3
    BGT mayor
    BLT menor
    BEQ iguales

mayor:
    LDR R0, =msg_mayor
    BL print_string
    B fin

menor:
    LDR R0, =msg_menor
    BL print_string
    B fin

iguales:
    LDR R0, =msg_iguales
    BL print_string

fin:
    MOV R7, #1
    MOV R0, #0
    SWI 0

.data
msg_mayor: .asciz "Rama mayor ejecutada\n"
msg_menor: .asciz "Rama menor ejecutada\n"
msg_iguales: .asciz "Rama iguales ejecutada\n"

.text
print_string:
    MOV R7, #4
    MOV R1, R0
    MOV R2, #100
    SWI 0
    BX LR
