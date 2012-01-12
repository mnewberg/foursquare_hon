def chunk(it, n=0):
	if n == 0:
		return iter([it])
	grouped = groupby(enumerate(it), lambda x: int(x[0]/n))
	counted = imap(lambda x:x[1], grouped)
	return imap(lambda x: imap(lambda y: y[1], x), counted)
