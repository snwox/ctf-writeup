f=list(open("./bin","rb").read())
print(f)
ar=[0]*256
ops=[x for x in range(9)]
ip=1
ar=list(map(ord,list('flag{my_sh1fti35_453_n1fty}')))+[0]*250
print((ar[17]))
print((ar[18]))
op=f[0]
while True:
  if op == ops[0]:
    ops[0]+=1
    a = ip;
    b = ip + 1;
    v4 = f[a];
    if v4 == 1:
      v50 = f[b];
      v5 = b + 1;
      ip = b + 2;
      ar[v50] += f[v5];
      print(f"op {op} : ar[{v50}] ({ar[v50]}) += f[{v5}] ({f[v5]})")
    elif v4 ==2:
      v49 = f[b];
      v6 = b + 1;
      ip = b + 2;
      ar[v49] += ar[f[v6]];
      print(f"op {op} : ar[{v49}] ({ar[v49]}) += ar[f[{v6}]] ({f[v6]},{ar[f[v6]]})")
  elif (op == ops[1] ):
    ops[1]+=1
    v7 = ip;
    v55 = ip + 1;
    v8 = f[v7];
    if ( v8 == 1 ):
      v48 = f[v55];
      v9 = v55 + 1;
      ip = v55 + 2;
      ar[v48] -= f[v9];
      print(f"op {op} : ar[{v48}] ({ar[v48]}) -= f[{v9}] ({f[v9]})")
    else:
      if ( v8 != 2 ):
        print(f"op {op} {v8}!=2")
        break
      v47 = f[v55];
      v10 = v55 + 1;
      ip = v55 + 2;
      ar[v47] -= ar[f[v10]];
      print(f"op {op} : ar[{v47}] ({ar[v47]}) -= ar[f[{v10}]] ({f[v10]},{ar[f[v10]]})")
  
  elif ( op == ops[2] ):
    ops[2]+=1
    v11 = ip;
    v56 = ip + 1;
    v12 = f[v11];
    if ( v12 == 1 ):
      v46 = f[v56];
      v13 = v56 + 1;
      ip = v56 + 2;
      ar[v46] *= f[v13];
      print(f"op {op} : ar[{v46}] ({ar[v46]}) *= f[{v13}] ({f[v13]})")
    
    else:
      if ( v12 != 2 ):
        print(f"op {op} : v12 != 2")
        break
      v45 = f[v56];
      v14 = v56 + 1;
      ip = v56 + 2;
      ar[v45] *= ar[f[v14]];
      print(f"op {op} : ar[{v45}] ({ar[v45]}) *= ar[f[{v14}]] ({f[v14]},{ar[f[v14]]})")
    
  
  elif ( op == ops[3] ):
    ops[3]+=1
    v15 = ip;
    v57 = ip + 1;
    v16 = f[v15];
    if ( v16 == 1 ):
      v44 = f[v57];
      v17 = v57 + 1;
      ip = v57 + 2;
      ar[v44] = ar[v44] / f[v17];
      print(f"op {op} : ar[{v44}] ({ar[v44]}) /= f[{v17}] ({f[v17]})")
    
    else:
    
      if ( v16 != 2 ):
        exit(1)
      v43 = f[v57];
      v18 = v57 + 1;
      ip = v57 + 2;
      ar[v43] = ar[v43] / ar[f[v18]];
      print(f"op {op} : ar[{v43}] ({ar[v43]}) /= ar[f[{v18}]] ({f[v18]},{ar[f[v18]]})")
  elif ( op == ops[4] ):
    v19 = ip;
    ip+=1
    print(f"op {op} : print(ar[f[{v19}]]) ({f[v19]},{ar[f[v19]]})")
  
  elif ( op == ops[5] ):
    ops[5]+=1
    v20 = ip;
    v58 = ip + 1;
    v21 = f[v20];
    if ( v21 == 1 ):
      v22 = v58;
      ip = v58 + 1;
      print(f"op {op} : flags {flags}, ip = v58+1 ({v58+1})")
      if ( flags ):
        ip += f[v22];
        print(f"op {op} : flags {flags}, ip = v58+1+f[{v22}] ({v58+1},{f[v22]})")
    else:
      if ( v21 != 2 ):
        exit(1)
      v23 = v58;
      ip = v58 + 1;
      print(f"op {op} : flags {flags}, ip = {ip}")
      if not flags:
        ip += f[v23];
        print(f"op {op} : flags {flags}, ip = {ip}")
    

  elif ( op == ops[6] ):
    ops[6]+=1
    v24 = ip;
    ip+=1
    v42 = f[v24];
    # ar[v42] = 102
    print(f"op : {op} : input ar[{v42}]")  
  elif ( op == ops[7] ):
    ops[7]+=1
    v25 = ip;
    v59 = ip + 1;
    print(f"switch f[{v25}] ({f[v25]})")
    match f[v25]:
      case 1:
        v26 = ar[f[v59]];
        v27 = v59 + 1;
        ip = v59 + 2;
        flags = v26 != f[v27];
        print(f"op {op} : flags({flags}) = ar[{f[v59]}] != f[{v27}] ({f[v27]})")
      case 2:
        v41 = f[v59];
        v28 = v59 + 1;
        ip = v59 + 2;
        flags = ar[v41] != ar[f[v28]];
        print(f"op {op} : flags({flags}) = ar[{v59}] ({ar[v41]}) != ar[f[{v28}]] ({f[v28]},{ar[f[v28]]})")
      case 3:
        v29 = ar[f[v59]];
        v30 = v59 + 1;
        ip = v59 + 2;
        flags = v29 >= f[v30];
        print(f"op {op} : flags({flags}) = ar[{f[v59]}] >= f[{v30}] ({f[v30]})")
      case 4:
        v31 = ar[f[v59]];
        v32 = v59 + 1;
        ip = v59 + 2;
        flags = v31 <= f[v32];
        print(f"op {op} : flags({flags}) = ar[{f[v59]}] <= f[{v32}] ({f[v32]})")
      case 5:
        v33 = ar[f[v59]];
        v34 = v59 + 1;
        ip = v59 + 2;
        flags = v33 >= ar[f[v34]];
        print(f"op {op} : flags({flags}) = ar[{f[v59]}] >= ar[f[{v34}]] ({f[v34]},{ar[f[v34]]})")
      case 6:
        v35 = ar[f[v59]];
        v36 = v59 + 1;
        ip = v59 + 2;
        flags = v35 <= ar[f[v36]];
        print(f"op {op} : flags({flags}) = ar[{f[v59]}] <= ar[f[{v36}]] ({f[v36]},{ar[f[v36]]})")
  else:
    print(f"op : {op}")
    break
  p_ip=ip
  ip+=1
  op = f[p_ip];

