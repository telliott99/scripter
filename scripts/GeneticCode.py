class GeneticCode:
	def __init__(self):
		self.D = self.makeCode()
		self.rD = self.reverseCodonDict()
		self.sD = self.synonomousCodons()

	def makeCode(self):
		nt = 'TCAG'
		L = list(nt)
		codons = [n1+n2+n3 for n1 in L for n2 in L for n3 in L]
		aa1 = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRR'
		aa2 = 'IIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
		return dict(zip(codons, list(aa1 + aa2)))
		
	def codoncomp(self, codon1, codon2):
		nt = 'TCAG'
		c11, c12, c13 = list(codon1)
		c21, c22, c23 = list(codon2)
		
		result = cmp(nt.index(c11), nt.index(c21))
		if result:	return result
		result = cmp(nt.index(c12), nt.index(c22))
		if result:	return result
		result = cmp(nt.index(c13), nt.index(c23))
		if result:	return result
		return 'error'

	def reverseCodonDict(self):
		D = self.D
		D2 = dict()
		for codon in D.keys():
			aa = D[codon]
			if aa in D2.keys():	
				D2[aa].extend([codon])
			else:		
				D2[aa] = [codon]
		return D2

	def synonomousCodons(self):
		D = self.D
		rD = self.rD
		sD = dict()
		for codon in D.keys():
			aa = D[codon]
			synonyms = set(rD[D[codon]])
			synonyms.discard(codon)
			sD[codon] = list(synonyms)
		return sD	

	def test(self):
		D = self.D
		L = D.keys()
		L.sort(self.codoncomp)
		k = L.pop(0)
		previousAA = D[k]
		previouscodon = k
		s = ''
		for k in L:
			currentAA = D[k]
			currentcodon = k
			new = not currentAA == previousAA
			s += previouscodon + '  '
			if new:		
				print s.ljust(25) + previousAA
				s = ''
			previousAA = currentAA
			previouscodon = currentcodon
		print s.ljust(25) + D[k]
		print
		print 'reverse'
		L = self.rD.keys()
		L.sort()
		for k in L:	print k, self.rD[k]
		print
		print 'synonomous'
		L = self.sD.keys()
		L.sort(self.codoncomp)
		for k in L:	print k, self.sD[k]

# utility function

def splitintocodons(seq, frame=1):
	# guard against obvious errors
	if not type(seq) == str:	return 'error'
	
	# adjust frame
	if frame == 2:	seq = seq[1:]
	if frame == 3:	seq = seq[2:]
	if len(seq) < 3:	return 'error'
	
	# chop it into groups of three
	codons = list()
	while seq:
		codons.append(seq[:3])
		seq = seq[3:]
	# leave the last if it's just a part
	if len(codons[-1]) < 3:	codons.pop()
	return codons

		
if __name__ == '__main__':
	code = GeneticCode()
	code.test()