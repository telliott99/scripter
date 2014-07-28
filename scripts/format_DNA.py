import os
import utils as ut
# internally, we use lowercase sequence
# just like Genbank  :)

def reverse_complement(seq):
    # call on the sequence only, no title
    # assume it's DNA
    D = {'a':'t','c':'g','g':'c','t':'a',
         'A':'T','C':'G','G':'C','T':'A' }
    rseq = [D[nt] for nt in seq]
    return ''.join(rseq)

def pretty_fmt(seq):
    # printable, double-stranded, numbered seq
    pL = list()
    rseq = reverse_complement(seq)
    seqL = ut.fmt_seq(seq,as_string=False)
    rseqL = ut.fmt_seq(rseq,as_string=False)
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
    title,seq = ut.split_seq(data)
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