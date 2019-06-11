import math
import matplotlib.pyplot as pyplot
import numpy
def comparer(schemeToCompare, invite_schema, N_MESURE, cas='client'):
	"""using normalized correlation on descrete signals to compare 2 schemes"""
	""" renvoie le degre de similitude entre les 2 schemas """
	tab_to_compare = []
	max_to_compare = max(schemeToCompare)
	max_invite_schema = max(invite_schema)
	for i in range(N_MESURE):
		stop = False
		if schemeToCompare[i] > 0:
			for _ in range(3):
				tab_to_compare.append(1)
				if len(tab_to_compare) == N_MESURE:
					stop = True
					break
	
			if i < N_MESURE - 3:
				for _ in range(3):
					if i == N_MESURE:
						stop = True
						break
			
			if stop:
				stop = False
				break
		else:
			tab_to_compare.append(0)
			if len(tab_to_compare) == N_MESURE:
				break
			
	tab_invite = []
	for i in range(N_MESURE):
		stop = False
		if invite_schema[i] > 0:
			for _ in range(3):
				tab_invite.append(1)
				if len(tab_invite) == N_MESURE:
					stop = True
				 	break

			if i < N_MESURE - 3:
				for _ in range(3):
					i += 1
					if i == N_MESURE:
						stop = True
						break
			if stop:
				stop = False
				break

		else:
			tab_invite.append(0)
			if len(tab_invite) == N_MESURE:
				break

	if cas == 'client':
		print 'TAB TO COMPARE : \n',tab_to_compare
		print 'TAB INVITE : \n',tab_invite
	
	moy_correlation_M = 0
	moy_correlation_N = 0
	correlation = 0
	for k in range(N_MESURE):
		correlation += (tab_to_compare[k]*tab_invite[k])
		moy_correlation_M += math.pow(tab_invite[k], 2) 
		moy_correlation_N += math.pow(tab_to_compare[k],2)
	norm_correlation_denominateur = math.sqrt(moy_correlation_M * moy_correlation_N)
	norm_correlation = correlation / norm_correlation_denominateur #value between 0 and 1
	
	
	# return norm_correlation
	return numpy.corrcoef(tab_to_compare, tab_invite)[0][1]



