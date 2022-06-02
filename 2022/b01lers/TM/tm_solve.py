# HeapArray
# 0x200 단위로 함수 0xff 개 + 1~26까지의 숫자 0xff 개 반복

# HeapArray 0 
# +0     (void*) return 1 func * 64 
# +0x200 (int) 1 * 0x100

# HeapArray 1
# +0     (void*) *ptrPointer = *buf; buf = buf+1; func * 64
# +0x200 (int) 2 * 0x100

# HeapArray 2 
# +0     (void*) return 1 func * 32 (even index) / (void*) *ptrPointer+=10 * 32 (odd index)
# +0x200 (int) 4 *1
# +0x204 (int) 3 * 0x100-1

# HeapArray 3 
# +0     (void*) *ptrPointer^=0x45, ptrPointer+=1 
# +0x200 (int) 1 * 0x100

# HeapArray 4 
# +0     (void*) ptrPointer-=2 * 64
# +0x200 (int) 7 * 0x100

# HeapArray 5 
# +0     (void*) print rejected * 0x100

# HeapArray 6
# +0     (void*) print accepted * 0x100

# HeapArrray 7 ~ 27
# +0     (void*) --ptrPointer
# +0x200 ~ 0x300 = 5
# +0x2XX = 0x8 ~ 0x1b

# v7 = HeapArray[Heap[0x200+ptrPointer]]
# v4 = *Heap[ptrPointer]()
# Heap = v7

start=0x555555555704

f=ida_funcs.get_func(start)
c=7
flag=''
for ea in Heads(f.start_ea,f.end_ea):
    if get_operand_value(ea,1)==0x555555555342:
        to=get_operand_value(ea+0x32,1)
        idx=get_operand_value(ea+0x4a,0)
        value=get_operand_value(ea+0x4a,1)
        print(f"{c}: default : {to}, {(idx//4)-0x200}={value}")
        c+=1
        if ((idx//4-0x200)^0x45) & 1 == 0:
            flag+=chr(((idx//4-0x200)^0x45)-10)
        else:
            flag+=chr(((idx//4-0x200)^0x45))
print(flag[::-1])
    