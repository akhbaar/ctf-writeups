### Hash 479 points

Let's start out by importing this file into ghidra
![inital_entry](images/inital_entry.png)
This looks very messy.....could it be packed/obfuscated somehow?
Running the command strings, it's clear that the file was packed with UPX.
![strings-upx](images/strings-upx.png)

After unpacking this with the command ```upx -d (filename)```
main() becomes much easier to read
![unpacked-main](images/unpacked-main.png)
But, going to main__main(), all that appears to be going on is
that 2 failure messages are printed out.
![wrong-path](images/wrong-path.png)

Go to the assembly listing of main__main.
There's a comparison being made (0x17 to 0x2d) that will never be equal, which jumps 
to the fail branch.
![1st-patch](images/1st-patch.png)

To get around this, use a hex editor of choice to patch the binary.
In my case, I chose to change the 0x2d to 0x17 with the tool "hexeditor"
![1st-hexedit](images/1st-hexedit.png)

Next, go to main__one and look at the assembly.

A similar comparsion is made to trick ghidra into
thinking that the code we want to execute (with the flag) is dead code
(so it won't show up in the decompiler)

![2nd-patch](images/2nd-patch.png)
So, we need to change comparison so that it will return 0, executing the dead code.
![2nd-hexedit](images/2nd-hexedit.png)

Do this again for main__two(), as shown here
![3rd-patch](images/3rd-patch.png)

![3rd-hexedit](images/3rd-hexedit.png)

Finally, we must change the

```  MOV        dword ptr [EBP + local_28],0x98c``` 
to move 0x4c so that main__two() will be called

![4th-patch](images/4th-patch.png)
![4th-hexedit](images/4th-hexedit.png)

Assuming that you patched everything correctly, you can run this modified file
and it will print the flag:

```flag{456789JKLq59U1337}```

![result](images/result.png)






