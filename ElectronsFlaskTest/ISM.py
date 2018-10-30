import numpy as np

class ISM:
	def __init__(self, variables):
		self.variables = variables
		self.reachability_matrix = np.array([[1, 0], [0, 1]])
		self.nextQuestion = [(0, 1), (1, 0)]
		self.levels = dict()
		self.phi = []
		self.answered = 0
		self.elementsToFill = 4
		self.elements = 0
		self.finishedContextualRelationships = False
		self.variable_level = dict()
		self.index = -1
		self.totalAnswered = 0
		self.m = None
		for i in range(variables):
			self.variable_level[i] = -1

	def __restartmatricesAndAddVariable(self):
		# Variables to answer (length of vector x + length of vector y)
		self.elementsToFill = 2 * len(self.reachability_matrix)
		self.answered = 0

		self.m = self.reachability_matrix
		zeros = np.zeros((len(self.m), len(self.m)))
		negatedTranspose = np.transpose(self.m) == 0
		self.phi = np.concatenate((np.concatenate((self.m, zeros), axis = 1), np.concatenate((negatedTranspose, self.m), axis = 1)), axis = 0)

		# Add a column and row with [0 ... len(m)] to keep track of where each variable is in the original phi matrix as it gets smaller
		indices = [np.arange(2 * len(self.m))]
		self.phi = np.concatenate((indices, self.phi), axis = 0)
		self.phi = np.concatenate((np.transpose([np.insert(indices, 0, -1)]), self.phi), axis = 1)

		# Add new variable (last column and last row)
		self.reachability_matrix = np.concatenate((self.reachability_matrix, np.zeros((len(self.reachability_matrix), 1))), axis = 1)
		self.reachability_matrix = np.concatenate((self.reachability_matrix, np.zeros((1, len(self.reachability_matrix[0])))), axis = 0)
		self.reachability_matrix[-1, -1] = 1

	def __addNextQuestion(self):

		# Row sum
		u = np.sum(self.phi[1:, :], axis = 1) - self.phi[1:, 0]

		# Column sum
		v = np.sum(self.phi[:,1:], axis = 0) - self.phi[0,1:]
		uv = np.array([u, v])

		# minimum of each pair (u, v)
		mins = np.min(uv, axis=0)
		#print("mins:", mins)

		# Indices of the maximum values in mins
		maxmins = np.argwhere(mins == np.max(mins)).flatten()
		
		# Break tie with sum of pairs (u, v) if more than one element in previous step
		if len(maxmins) > 1:
			sums = np.sum(uv, axis = 0)
			self.index = 0
			maxSum = -1
			for i in range(len(sums)):
				if sums[i] >= maxSum:
					self.index = i
					maxSum = sums[i]
		else:
			# Index of max element in mins
			self.index = np.argmax(mins)

		#print("Picked index:", self.index)

		(i, j) = (-1, -1)
		ans = -1

		# Top half of the phi matrix consists of x (these get negated)
		if self.phi[self.index + 1, 0] < len(self.m): # Add 1 to the index because the first row has the indices defined in line 37
			#print("Picked x")
			(i, j) = (self.phi[self.index + 1, 0], len(self.m))
		# Lower half of the phi matrix consists of y
		else:
			#print("Picked y")
			(i, j) = (len(self.m), self.phi[0, self.index + 1] - len(self.m)) # Add 1 to the index because the first column has the indices defined in line 37

		#print("Next question: (%d, %d)" % (i, j))
		self.nextQuestion.append((int(i), int(j)))

	def getNextQuestion(self):
		question = self.nextQuestion[0]
		self.nextQuestion = self.nextQuestion[1:]
		return question

	def answerQuestion(self, answer, i, j):
		self.totalAnswered += 1
		self.reachability_matrix[i][j] = answer

		if self.totalAnswered == 2:
			if self.variables > 2:
				self.__restartmatricesAndAddVariable()
				self.__addNextQuestion()
			else:
				self.finishedContextualRelationships = True
				self.__structural_model()

		if self.totalAnswered > 2:
			# Vector in which questions can be inferred
			indicesToFill = np.array([])

			# Lists of tuples with 4 elements
			#	0 -> index of row/column in phi to delete
			#	1 -> index of row/column in the original phi matrix (to get the position in the reachability matrix to infer)
			#	2 -> row in the reachability matrix to infer
			#	3 -> column in the reachability matrix to infer
			questionsToInfer = []

			# Top half of the phi matrix consists of x (these get negated)
			if self.phi[self.index + 1, 0] < len(self.m): # Add 1 to the index because the first row has the indices defined in line 37
				answer = (answer == 0)

			# Search in column if the answer to the question with best opportunity inference is 0
			if answer == 0:
				indicesToFill = self.phi[:, self.index + 1] # Add 1 to the index because the first column has the indices defined in line 37
			# Search in row if the answer to the question with best opportunity inference is 1
			else:
				indicesToFill = self.phi[self.index + 1, :] # Add 1 to the index because the first row has the indices defined in line 37

			# Look for 1s in the row or column
			for i in np.arange(1, len(indicesToFill)):
				if indicesToFill[i] == 1:
					self.answered = self.answered + 1
					# Top half of phi consists of x (these get negated)
					if self.phi[i, 0] < len(self.m):
						questionsToInfer.append((int(i), int(self.phi[i, 0]), int(self.phi[i, 0]), int(len(self.m)))) # (index (to check if its x or y), i (row to fill in reachability matrix), j (column to fill in reachability matrix))
					# Lower half of phi consists of y
					else:
						questionsToInfer.append((int(i), int(self.phi[i, 0]), int(len(self.m)), int(self.phi[0, i] - len(self.m)))) # (index (to check if its x or y), i (row to fill in reachability matrix), j (column to fill in reachability matrix))

			# Rows/columns to delete
			delete = []
			for question in questionsToInfer:
				# Collect rows/columns to delete after inferring the needed questions
				delete.append(question[0])

				# Top half of phi consists of x (these get negated)
				if question[1] < len(self.m):
					self.reachability_matrix[question[2], question[3]] = (answer == 0)
				# Lower half of phi consists of y
				else:
					self.reachability_matrix[question[2], question[3]] = answer

			# Delete the rows and columns of x's or y's that have been ansered/inferred
			self.phi = np.delete(self.phi, delete, axis = 0)
			self.phi = np.delete(self.phi, delete, axis = 1)

			if self.answered >= self.elementsToFill:
				if (len(self.reachability_matrix) == self.variables):
					self.finishedContextualRelationships = True
					self.__structural_model()
				else:
					self.__restartmatricesAndAddVariable()
					self.__addNextQuestion()
			else:
				self.__addNextQuestion()

	def __reachabilityAntecedentSets(self, variable, exclude):
		reachability_set = set()
		antecedent_set = set()
		for i in range(self.variables):
			if self.reachability_matrix[variable][i] == 1:
				reachability_set.add(i)

			if self.reachability_matrix[i][variable] == 1:
				antecedent_set.add(i)

		return (reachability_set - exclude, antecedent_set - exclude)

	def __finished(self):
		for key, value in self.variable_level.items():
			if value == -1:
				return False

		return True

	def __structural_model(self):
		to_exclude = set()
		level = 1
		while not self.__finished():
			variables_to_exclude = set()
			for variable in range(self.variables):
				if variable not in to_exclude:
					(reachability_set, antecedent_set) = self.__reachabilityAntecedentSets(variable, to_exclude)
					intersection = reachability_set & antecedent_set
					if reachability_set == intersection:
						variables_to_exclude.add(variable)
						if level in self.levels:
							self.levels[level].append(variable + 1) # Just to show them as 1-indexed
							self.variable_level[variable] = level
						else:
							self.levels[level] = [variable + 1] # Just to show them as 1-indexed
							self.variable_level[variable] = level

			to_exclude = to_exclude | variables_to_exclude
			level = level + 1
