import numpy as np

class ISM:
	def __init__(self, variables):
		self.variables_dict = variables
		print(variables)
		self.variables = len(variables)
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
		self.C = self.reachability_matrix
		self.permuted_rm = np.empty(0, dtype=int)
		self.m = None
		self.cycles	= {}
		for i in range(self.variables):
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

		(i, j) = (-1, -1)
		ans = -1

		# Top half of the phi matrix consists of x (these get negated)
		if self.phi[self.index + 1, 0] < len(self.m): # Add 1 to the index because the first row has the indices defined in line 37
			(i, j) = (self.phi[self.index + 1, 0], len(self.m))
		# Lower half of the phi matrix consists of y
		else:
			(i, j) = (len(self.m), self.phi[0, self.index + 1] - len(self.m)) # Add 1 to the index because the first column has the indices defined in line 37

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

	def __permute_reachability_matrix(self):
		# indices = [[variable['ideaID'] for variable in self.variables_dict]]
		indices = [range(1, self.variables + 1)]
		tmpReachabilityMatrix = self.reachability_matrix
		tmpReachabilityMatrix = np.concatenate((indices, tmpReachabilityMatrix), axis = 0)
		tmpReachabilityMatrix = np.concatenate((np.transpose([np.insert(indices, 0, -1)]), tmpReachabilityMatrix), axis = 1)

		self.permuted_rm = [tmpReachabilityMatrix[0]]

		# Arrange rows per level
		for i in range(1, len(self.levels) + 1):
			varsInLevel = self.levels[i]
			varsInLevel = [variable for vars in varsInLevel for variable in vars]
			level = tmpReachabilityMatrix[varsInLevel]
			self.permuted_rm = np.append(self.permuted_rm, level, axis = 0)

		# Arrange columns per level
		tmpReachabilityMatrix = self.permuted_rm
		self.permuted_rm = self.permuted_rm[:, [0]]
		for i in range(1, len(self.levels) + 1):
			varsInLevel = self.levels[i]
			varsInLevel = [variable for vars in varsInLevel for variable in vars]
			level = tmpReachabilityMatrix[:, varsInLevel]
			self.permuted_rm = np.append(self.permuted_rm, level, axis = 1)

	def __add_cycles_helper(self, level, start_end):
		cycles = False
		self.cycles[level] = []
		startIndex, endIndex = start_end[0], start_end[1]
		levelMatrix = self.permuted_rm[startIndex:(endIndex + 1), startIndex:(endIndex + 1)]
		s = set()
		d = {}	# Maps a row to a list of indexes which have the same row
		d_ideaNumber = {}
		rng = range(startIndex, endIndex + 1)
		for i in range(len(levelMatrix)):
			row = levelMatrix[i]
			row_str = ''.join(str(e) for e in row)
			original_index = rng[i]
			idea_number = int(self.permuted_rm[startIndex + i][0])
			if row_str in s:
				d[row_str].append(original_index)
				d_ideaNumber[row_str].append(idea_number)
			else:
				s.add(row_str)
				d[row_str] = [original_index]
				d_ideaNumber[row_str] = [idea_number]

		# Sort keys by value length
		sortedKeys = sorted(d, key=lambda k: len(d[k]))

		sortedIndices = []

		variablesInCycleToDelete = []

		variableCycleIndex = {}

		# Save variables in cycle
		for key in sortedKeys:

			for index in d[key]:
				sortedIndices.append(index)

			if len(d[key]) > 1:
				cycles = True
				self.cycles[level].append(d_ideaNumber[key])

		# Rearrange rows and columns if there's a cycle
		if cycles == True:
			elementsInCycle = []
			for cycle in self.cycles[level]:
				for element in cycle:
					elementsInCycle.append(element)

			tmpRm = np.copy(self.permuted_rm)
			i = 0
			for index in rng:

				# Arrange variable rows and columns that are not in the block diagonal
				self.permuted_rm[index, :rng[0]] = tmpRm[sortedIndices[i], :rng[0]]			# Swap rows from 0..blockStart
				self.permuted_rm[rng[-1]+1:, index] = tmpRm[rng[-1]+1:, sortedIndices[i]]	# Swap columns from blockEnd..end
				self.permuted_rm[0, index] = tmpRm[0, sortedIndices[i]]						# Swap indexes at first row

				if int(tmpRm[0, sortedIndices[i]]) in elementsInCycle:
					variableCycleIndex[int(tmpRm[0, sortedIndices[i]])] = index

				i = i + 1

			# Arrange elements in block
			for i in range(len(rng)):
				for j in range(len(rng)):
					self.permuted_rm[rng[i], rng[j]] = tmpRm[sortedIndices[i], sortedIndices[j]]

		for cycle in self.cycles[level]:
			cycleIndices = []
			for i in range(1, len(cycle)):
				variablesInCycleToDelete.append(variableCycleIndex[cycle[i]])

		return variablesInCycleToDelete

	def __remove_cycles(self):
		levelsStartEnd = {}
		for i in range(1, len(self.levels) + 1):
			if i == 1:
				levelsStartEnd[i] = [1, len(self.levels[i])]
			else:
				levelsStartEnd[i] = [levelsStartEnd[i - 1][1] + 1, levelsStartEnd[i - 1][1] + len(self.levels[i])]

			toDelete = self.__add_cycles_helper(i, levelsStartEnd[i])
			variablesDeleted = len(toDelete)
			levelsStartEnd[i][1] -= variablesDeleted

			self.permuted_rm = np.delete(self.permuted_rm, toDelete, axis = 0)
			self.permuted_rm = np.delete(self.permuted_rm, toDelete, axis = 1)

		return levelsStartEnd

	def __adjust_levels_cycles(self):
		for level in range(1, len(self.levels) + 1):
			cyclesInLevel = self.cycles[level]
			if len(cyclesInLevel) > 0:
				flattened_cycles = [element for cycle in cyclesInLevel for element in cycle]
				new_level = []
				for elements in self.levels[level]:
					for element in elements:
						if element not in flattened_cycles:
							new_level.append([element])

				for cycle in cyclesInLevel:
					new_level.append(cycle)

				self.levels[level] = new_level

	def __get_beta(self, beta, i, levelsStartEnd):
		for level in range(1, len(self.levels) - i + 1):
			blockRows = levelsStartEnd[level + i]
			blockColumns = levelsStartEnd[level]

			blockRowStart, blockRowEnd = blockRows[0], blockRows[1]
			blockColumnStart, blockColumnEnd = blockColumns[0], blockColumns[1]
			beta[(blockRowStart - 1) : blockRowEnd, (blockColumnStart - 1) : blockColumnEnd] = self.permuted_rm[blockRowStart : (blockRowEnd + 1), blockColumnStart : (blockColumnEnd + 1)]

		return beta, i + 1

	def __remove_redundant_relations(self, levelsStartEnd):
		s = self.permuted_rm.shape
		C = self.permuted_rm[1:, 1:]
		beta = np.zeros((s[0] - 1, s[1] - 1))
		betaIndex = 0
		beta, betaIndex = self.__get_beta(beta, betaIndex, levelsStartEnd)

		levels = len(self.levels)

		idempotence = False
		while not idempotence:
			beta_raised = np.copy(beta)
			for i in range(levels - 1):
				beta_raised = np.dot(beta_raised, beta)
				beta_raised = 1.0 * (beta_raised > 0)

			error = np.sum(np.subtract(C, beta_raised))
			idempotence = error == 0
			if not idempotence:
				beta, betaIndex = self.__get_beta(beta, betaIndex, levelsStartEnd)

		self.permuted_rm[1:, 1:] = beta - np.eye(s[0] - 1)

	def __changeIndexToID(self):
		print(self.levels)
		# Level
		for level in self.levels.keys():
			# Variables (lists because they can be cycles)
			varsInLevel = self.levels[level]
			newLevel = []
			print(level, varsInLevel)
			for variables in varsInLevel:
				# Variable
				print(variables)
				newLevel.append([self.variables_dict[variable - 1]['ideaID'] for variable in variables])

			self.levels[level] = newLevel


	def __structural_model(self):
		to_exclude = set()
		level = 1
		print(self.variables_dict)
		while not self.__finished():
			variables_to_exclude = set()
			for variable in range(self.variables):
				variableID = self.variables_dict[variable]['ideaID']
				if variable not in to_exclude:
					(reachability_set, antecedent_set) = self.__reachabilityAntecedentSets(variable, to_exclude)
					intersection = reachability_set & antecedent_set
					if reachability_set == intersection:
						variables_to_exclude.add(variable)
						if level in self.levels:
							self.levels[level].append([variable + 1])
							self.variable_level[variable] = level
						else:
							self.levels[level] = [[variable + 1]]
							self.variable_level[variable] = level

			to_exclude = to_exclude | variables_to_exclude
			level = level + 1

		self.__permute_reachability_matrix()
		levelsStartEnd = self.__remove_cycles()
		self.__remove_redundant_relations(levelsStartEnd)
		self.__adjust_levels_cycles()
		self.__changeIndexToID()
		self.reachability_matrix = self.permuted_rm
