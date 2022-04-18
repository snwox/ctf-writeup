
import time
print("="*0x30)
start=0x113F
end=get_name_ea_simple("cat_flag")

#U D L R 
rev={
    "U":"D",
    "D":"U",
    "R":"L",
    "L":"R"
}
x={
    "U":-1,
    "D":1,
    "R":0,
    "L":0
}
y={
    "U":0,
    "D":0,
    "R":1,
    "L":-1
}

ff=[""]*101
chks={
    0x112a:["D","R"],
    get_name_ea_simple("down"):["D"],
    get_name_ea_simple("left"):["L"],
    get_name_ea_simple("right"):["R"],
    get_name_ea_simple("up"):["U"],

    get_name_ea_simple("down_left"):["D","L"],
    get_name_ea_simple("down_up"):["D","U"],
    get_name_ea_simple("left_up"):["L","U"],
    get_name_ea_simple("down_right"):["D","R"],
    get_name_ea_simple("left_right"):["L","R"],
    get_name_ea_simple("up_right"):["U","R"],

    get_name_ea_simple("no_right"):["U","D","L"],
    get_name_ea_simple("no_left"):["U","D","R"],
    get_name_ea_simple("no_down"):["U","L","R"],
    get_name_ea_simple("no_up"):["D","L","R"],
    get_name_ea_simple("fine"):["D","L","R","U"],
}

def get_chk_func(addr):
    chk=-1
    f=ida_funcs.get_func(addr)
    for ea in Heads(f.start_ea,f.end_ea):
        if print_insn_mnem(ea)=="call":
            chk=get_operand_value(ea,0)
            break
    return chk

def OOB(addr):
    n_func=ida_funcs.get_func(addr)
    if n_func!=None and n_func.start_ea == addr\
        and (addr-0x113f)%220==0:
        return 1
    return 0
def back(idx,addr,prev):

    if idx==100:
        return

    if addr == start:
        print(f"yaho {''.join(ff)[::-1]}")

    chk=get_chk_func(addr)
    flags=chks[chk][:]
    for f in flags:
        if f == prev:
            continue
        nxt = addr+30*x[rev[f]]*220+y[rev[f]]*220
        if OOB(nxt):
            ff[idx]=f
            back(idx+1,nxt,rev[f])
            ff[idx]=''
    

back(0,end,'U')

# for i,j,c in zip([1,0],[0,1],["D","R"]):
#     ff[0]=c
#     print("asdf")
#     back(1,start+30*i*220+j*220,c)


#    for c,(i,j) in enumerate(zip([-1,1,0,0],[0,0,-1,1])):
#        nxt=f.start_ea+30*(v6+i)*0xdc+(v7+j)*0xdc
#        n_func = ida_funcs.get_func(nxt)
#        if n_func!=None and n_func.start_ea==nxt and nxt>addr:
#                ff[idx]=flags[c]
#                if f
#                back(idx+1,v6+i,v7+j,nxt,ff[idx])
#                ff[idx]=""

    # if addr == get_name_ea_simple("cat_flag"):
    #     print(hex(addr))
    #     print(''.join(ff))
    #     print("cat flag!!")
    #     return
    # if idx==10:
    #     print(hex(addr))
    #     print(''.join(ff))
    #     return
        

    # flags=chks[chk][:]
    # try:                        ## don't return to prev
    #     flags.remove(rev[prev])
    # except:
    #     pass
    # print(f"{idx} : prev : {prev}, {flags}, {hex(addr)}")
    # print(chks)
    # for f in flags:
    #     nxt=addr+30*x[f]*220+y[f]*220
    #     if OOB(nxt):
    #         ff[idx]=f
    #         back(idx+1,nxt,f)
    #         ff[idx]=''
