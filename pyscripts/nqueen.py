board,cb = [5,10],[]
for i in range(board[0]):
	cb.append([0 for j in range(board[1])])
		
# print(cb)

def check(r,c):
	if 1 in cb[r]: return False
	if 1 in [cb[i][j] for i ,j in zip([i for i in range(r,-1,-1)],[j for j in range(c,-1,-1)])]: return False #checking left daigonal 
	if 1 in [cb[i][j] for i ,j in zip([i for i in range(r,-1,-1)],[j for j in range(c,board[1])])]: return False #checking right daigonal	
	if 1 in [cb[j][c] for j in range(r)]: return False
	return True

for i in [(i,j) for i in range(board[0]) for j in range(board[1])]:
	# print(i)
	if check(i[0], i[1]):
		cb[i[0]][i[1]] = 1

for i in cb: #printing chess board
	i = [str(j) for j in i]
	print(' '.join(i))