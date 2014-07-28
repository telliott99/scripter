def load_data(fn):
    wnl = '\r\n'    # Windows newline
    unl = '\n'
    with open(fn,'r') as f:
        data = f.read()
    return data.replace(wnl,unl)

def chunks(seq,SZ):
    rL = list()
    for i in range(0,len(seq),SZ):
        rL.append(seq[i:i+SZ])
    return rL