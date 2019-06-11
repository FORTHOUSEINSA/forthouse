import math
import matplotlib.pyplot as pyplot 
import numpy

def comparer(schemeToCompare, invite_schema, N_MESURE, cas = 'client'):
	"""using normalized correlation on descrete signals to compare 2 schemes"""
	""" renvoie le degre de similitude entre les 2 schemas """
	tab_to_compare = []
	tab_invite = []
	max_to_compare = max(schemeToCompare)
	max_invite = max(invite_schema)
	

	for a in range(N_MESURE):
		if schemeToCompare[a] > max_to_compare/2:
			tab_to_compare.append(2)
		elif schemeToCompare[a] > 0 and schemeToCompare[a] <max_to_compare/2:
			tab_to_compare.append(1)
		else:
			tab_to_compare.append(0)
	if cas == 'client':

		pyplot.plot(tab_to_compare)
		pyplot.show()
		print 'SCHEMA UTILISATEURS : ',tab_to_compare

	for a in range(N_MESURE):
		if invite_schema[a] > max_invite/2:
			tab_invite.append(2)
		elif  invite_schema[a] > 0 and invite_schema[a] < max_invite/2:
			tab_invite.append(1)
		else:
			tab_invite.append(0)
	if cas == 'client':
		pyplot.plot(tab_invite)
		pyplot.show()
		print 'SCHEMA INVITE   : ',tab_invite
	
	return numpy.corrcoef(tab_invite, tab_to_compare)[0][1]




