def load_data(fn):
    wnl = '\r\n'    # Windows newline
    unl = '\n'
    with open(fn,'r') as f:
        data = f.read()
    return data.replace(wnl,unl)

def split_seq(data):
    split_char = '\n'
    if '%0A' in data:
        split_char = '%0A'
    title, seq = data.strip().split(split_char,1)
    return title, seq

def chunks(seq,SZ):
    rL = list()
    for i in range(0,len(seq),SZ):
        rL.append(seq[i:i+SZ])
    return rL

def fmt_seq(seq,uppercase=True,
            group_sz=10,groups_per_line=5,
            as_string = False):
    # format a sequence 
    # returning a list of elements
    # containing 5 groups of 10 char
    if uppercase:
        seq = seq.upper()
    rL = list()
    seqL = chunks(seq,group_sz)
    for line in chunks(seqL,groups_per_line):
        rL.append(' '.join(line))
    if not as_string:
        return rL
    return '\n'.join(rL)

def make_code():
    nt = 'TCAG'
    L = list(nt)
    codons = [n1+n2+n3 for n1 in L for n2 in L for n3 in L]
    aa =  'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRR'
    aa += 'IIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
    return dict(zip(codons, list(aa)))
