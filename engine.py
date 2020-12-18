"""
This class stores all the information about the current gamestate. It will also determine 
all the valid moves for the current state + MoveLog
"""
class GameState(object):
	"""docstring for GameState"""
	def __init__(self):
		self.board = [
		["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
		["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["--", "--", "--", "--", "--", "--", "--", "--"],
		["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
		["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
		]
		self.moveGeneratingFunctions = {
										"p": self.generate_pawn_moves, 
										"R": self.generate_rook_moves,
										"N": self.generate_knight_moves,
										"B": self.generate_bishop_moves,
										"Q": self.generate_queen_moves,
										"K": self.generate_king_moves
										}
		self.whiteToMove = True #store whos turn it is
		self.moveLog = [] #Store the moves. Also needs to store all the captured and moved pieces.

		self.whitheKingSq = [7, 4] #Store the position of the white King 
		self.blackKingSq = [0, 4] #Store the position of the black King

		self.checkmate = False
		self.stalemate = False

		self.isCastleMove = False

	def make_move(self, move):
		"""
		Store move as [Starting Square, Ending Square, moved Piece, capturedPiece]
		"""
		## Use this to only execute the move
		self.board[move.startRow][move.startCol] = "--"
		self.board[move.endRow][move.endCol] = move.movedPiece
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove

	def get_all_possible_moves(self):
		moves = []
		for row in range(len(self.board)):
			for col in range(len(self.board)):
				color = self.board[row][col][0]
				if (self.whiteToMove and color == "w") or (not self.whiteToMove and color == "b"):
					piece = self.board[row][col][1]
					'''
					We check for all the pieces and generate its move according to its position
					'''
					self.moveGeneratingFunctions[piece](row, col, moves)
					# elif piece == "N":
					# 	self.generate_knight_moves(r, c, allPossiblemoves)
					# elif piece == "B":
					# 	self.generate_bishop_moves(r, c, allPossiblemoves)
					# elif piece == "Q":
					# 	self.generate_queen_moves(r, c, allPossiblemoves)
					# elif piece == "K":
					# 	self.generate_king_moves(r, c, allPossiblemoves)
		return moves

	def generate_pawn_moves(self, row, col, moves):
		if self.whiteToMove:
			if self.board[row - 1][col] == "--": # on square move
				moves.append(Move((row, col), (row - 1, col), self.board))
				if self.board[row - 2][col] == "--" and row == 6: # two square move
					moves.append(Move((row, col), (row - 2, col), self.board))

			if col - 1 > 0:
				if self.board[row - 1][col - 1][0] == "b":
					moves.append(Move((row, col), (row - 1, col - 1), self.board))  

			if col + 1 <= 7:
				if self.board[row - 1][col + 1][0] == "b":
					moves.append(Move((row, col), (row - 1, col + 1), self.board)) 

		elif not self.whiteToMove:
			if self.board[row + 1][col] == "--": # on square move
				moves.append(Move((row, col), (row + 1, col), self.board))
				if self.board[row + 2][col] == "--" and row == 1: # two square move
					moves.append(Move((row, col), (row + 2, col), self.board))	

			if col - 1 > 0:
				if self.board[row + 1][col - 1][0] == "w":
					moves.append(Move((row, col), (row + 1, col - 1), self.board))  

			if col + 1 <= 7:
				if self.board[row + 1][col + 1][0] == "w":
					moves.append(Move((row, col), (row + 1, col + 1), self.board)) 

	def generate_rook_moves(self, row, col, moves):
		pass

	def generate_knight_moves(self, row, col, moves):
		pass

	def generate_bishop_moves(self, row, col, moves):
		pass

	def generate_queen_moves(self, row, col, moves):
		pass

	def generate_king_moves(self, row, col, moves):
		pass
			

class Move(object):
	"""docstring for Move"""
	# map keys to values
	# key : value
	ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
					"5": 3, "6": 2, "7": 1, "8": 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
					"e": 4, "f": 5, "g": 6, "h": 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def __init__(self, startSQ, endSQ, board):
		self.startRow = startSQ[0]
		self.startCol = startSQ[1]
		self.endRow = endSQ[0]
		self.endCol = endSQ[1]
		self.movedPiece = board[self.startRow][self.startCol]
		self.capturedPiece = board[self.endRow][self.endCol]
		self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
		print(self.moveId)

	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveId == other.moveId
		return False

	def get_chess_notation(self): # prototype
		return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

	def get_rank_file(self, row, col):
		return self.colsToFiles[col] + self.rowsToRanks[row]


						


class Pawn(object):
	"""docstring for Pawn"""
	def __init__(self, position, board, whiteToMove):
		self.row = position[2]
		self.col = position[1]
		self.moved = False
		self.whiteToMove = whiteToMove
		self.board = board
		self.moves = []

	def generate_possible_moves(self):
		"""
		Logic for all the pawn moves
		"""
		if self.whiteToMove:
			if self.board[self.row - 1][self.col] == "--": # on square move
				self.moves.append(Move((self.row, self.col), (self.row - 1, self.col), self.board))

				if self.board[self.row - 2][self.col] == "--" and self.row == "6": # two square move
					self.moves.append(Move((self.row, self.col), (self.row - 2, self.col), self.board))

		return self.moves


		