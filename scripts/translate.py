import os
import utils as ut

def translate(seq):
    seq = seq.upper()
    GeneticCode = ut.make_code()  # upper-case DNA
    sL = ut.chunks(seq,3)
    rL = [GeneticCode[c] for c in sL]
    return ''.join(rL)

def pretty_fmt(pep):
    # printable, numbered protein seq
    pL = list()
    seqL = ut.fmt_seq(pep,as_string=False)
    # we could cache this info here but for now:
    line0 = seqL[0]
    N = len(line0) - line0.count(' ')
    for i,s, in enumerate(seqL):
        sL = [str(N*(i+1)).rjust(len(line0))]
        sL.append(s)
        pL.append('\n'.join(sL))
    return '\n\n'.join(pL)
  
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
        title, seq = ut.split_seq(seq)
    result = pretty_fmt(translate(seq))
    return result

def test():
    print translate('ATGGAATAA')
        
if __name__ == "__main__":
    test()