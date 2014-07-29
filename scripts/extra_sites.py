import os
import utils as ut
import GeneticCode as GC
import renzymes

def loadSequence(fn):
	FH = open(fn,'r')
	data = FH.read()
	seq = data.strip().split('\n',1)[1]
	return seq

def onlySixCutters(D):
	D2 = dict()
	for k in D.keys():
		if len(D[k]) == 6:	D2[k] = D[k]
	return D2

def reverseD(D):
	# reverse dict (REnzymes)
	# values become keys, keys become values
	D2 = dict()
	for k in D.keys():	D2[D[k]] = k
	return D2
	
def make_enzyme_dict():
	s = renzymes.renzymes
	L = s.strip().split('\n')
	D = dict()
	for line in L:
		k,v = line.strip().split()
		D[k] = v
	return D
#----------------------------------------

# we will iterate through codons
# since we're testing six-cutters we'll need
# two flanking codons upstream and down

def upstream(i,codons):
	L = list()
	if i == 0:	return ''
	if i == 1:	return ''.join(codons[:1])
	return ''.join(codons[i-2:i])

def downstream(i,codons):
	if i == len(codons)-1:	
		return ''
	if i == len(codons)-2:	
		return ''.join(codons[-1:])
	return ''.join(codons[i+1:i+3])

def getContext(i,codons):
	return ( upstream(i,codons), 
			 downstream(i,codons) )
#----------------------------------------

# initial setup
def setup():
	eD = make_enzyme_dict()
	enzymes = onlySixCutters(eD)
	revEnzD = reverseD(enzymes)
	sites = revEnzD.keys()
	synonymsD = GC.GeneticCode().sD
	return revEnzD,sites,synonymsD

def get_codons(seq):
	seq = seq.upper()
	codons = ut.chunks(seq,3)
	return codons
  
#----------------------------------------

def find_sites(seq):
	codons = get_codons(seq)
	revEnzD,sites,synonymsD = setup()

	pL = list()
	for i, codon in enumerate(codons):
		sL = list()
		up, down = getContext(i,codons)
		wt = up + codon + down
		wtcuts = [s for s in sites if s in wt]
	
		syns = synonymsD[codon]
		for syn in syns:
			mut = up + syn + down
			mutcuts = [s for s in sites if s in mut]
			L = [s for s in mutcuts if not s in wtcuts]
		
			if L:
				sL.append(' '.join(['codon', str(i+1), 
				          codon + ' => ' + syn]))
				sL.append(up + ' ' + codon + ' ' + down)
				sL.append(up + ' ' + syn + ' ' + down)
				for site in L:
					sL.append(' '.join([revEnzD[site], site]))
		if sL:
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
    result = find_sites(seq)
    return result

def test():
    pass
        
if __name__ == "__main__":
    test()
