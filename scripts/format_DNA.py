import os
import utils as ut
# internally, we use lowercase sequence
# just like Genbank  :)

def split_seq(data):
    split_char = '\n'
    if '%0A' in data:
        split_char = '%0A'
    title, seq = data.strip().split(split_char,1)
    return title, seq

def reverse_complement(seq):
    # call on the sequence only, no title
    # assume it's DNA
    D = {'a':'t','c':'g','g':'c','t':'a',
         'A':'T','C':'G','G':'C','T':'A' }
    rseq = [D[nt] for nt in seq]
    return ''.join(rseq)

def fmt_seq(seq,uppercase=True,
            group_sz=10,groups_per_line=5,
            as_string = False):
    # format a sequence 
    # returning a list of elements
    # containing 5 groups of 10 char
    if uppercase:
        seq = seq.upper()
    rL = list()
    seqL = ut.chunks(seq,group_sz)
    for line in ut.chunks(seqL,groups_per_line):
        rL.append(' '.join(line))
    if not as_string:
        return rL
    return '\n'.join(rL)

def pretty_fmt(seq):
    # printable, double-stranded, numbered seq
    pL = list()
    rseq = reverse_complement(seq)
    seqL = fmt_seq(seq,as_string=False)
    rseqL = fmt_seq(rseq,as_string=False)
    # we could cache this info here but for now:
    line0 = seqL[0]
    N = len(line0) - line0.count(' ')
    for i,(s,r) in enumerate(zip(seqL,rseqL)):
        sL = [str(N*(i+1)).rjust(len(line0))]
        sL.extend([s,r])
        pL.append('\n'.join(sL))
    return '\n\n'.join(pL)

def test():
    data = ut.load_data('SThemA.txt')
    title,seq = split_seq(data)
    print pretty_fmt(seq)

def run(D):
    print 'in script: ', os.path.basename(__file__)
    print 'dict:'
    for k in D:
        if k == 'seq':
            print '  ', k, '=', D[k][:25]
        else:
            print '  ', k, '=', D[k]
    # for now, assuming it is a sequence and not filename
    seq = D['seq']
    if seq.startswith('>') or seq.startswith('%3E'):
        title, seq = split_seq(seq)
    result = pretty_fmt(seq)
    return result
        
if __name__ == "__main__":
    test()