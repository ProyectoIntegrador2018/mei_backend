import numpy as np

# axis = 0 => hacia abajo
# axis = 1 => hacia la derecha
class ISM:
	def __init__(self, variables):
		self.variables = variables
		self.reachability_matrix = np.array([[1, 0], [0, 1]])
		self.levels = dict()
		self.variable_level = dict()
		for i in range(variables):
			self.variable_level[i] = -1

	def askQuestion(self, i, j):
		print("%d influences %d? (y/n)" % (i + 1, j + 1))
		ans = input()
		if ans == "y":
			return 1
		else:
			return 0

	def contextual_relationships(self):
		self.reachability_matrix[0][1] = self.askQuestion(0, 1)
		self.reachability_matrix[1][0] = self.askQuestion(1, 0)

		# Keep adding variables
		while len(self.reachability_matrix) < self.variables:

			# Variables to answer (length of vector x + length of vector y)
			elementsToFill = 2 * len(self.reachability_matrix)
			answered = 0

			m = self.reachability_matrix
			zeros = np.zeros((len(m), len(m)))
			negatedTranspose = np.transpose(m) == 0
			phi = np.concatenate((np.concatenate((m, zeros), axis = 1), np.concatenate((negatedTranspose, m), axis = 1)), axis = 0)

			# Add a column and row with [0 ... len(m)] to keep track of where each variable is in the original phi matrix as it gets smaller
			indices = [np.arange(2 * len(m))]
			phi = np.concatenate((indices, phi), axis = 0)
			phi = np.concatenate((np.transpose([np.insert(indices, 0, -1)]), phi), axis = 1)

			# Add new variable (last column and last row)
			self.reachability_matrix = np.concatenate((self.reachability_matrix, np.zeros((len(self.reachability_matrix), 1))), axis = 1)
			self.reachability_matrix = np.concatenate((self.reachability_matrix, np.zeros((1, len(self.reachability_matrix[0])))), axis = 0)
			self.reachability_matrix[-1, -1] = 1

			# Ask or infer all the needed questions
			while answered < elementsToFill:
				# Row sum
				u = np.sum(phi[1:, :], axis = 1) - phi[1:, 0]

				# Column sum
				v = np.sum(phi[:,1:], axis = 0) - phi[0,1:]
				uv = np.array([u, v])

				# Minimum of each pair (u, v)
				mins = np.min(uv, axis=0)

				# Indices of the maximum values in mins
				maxMins = np.argwhere(mins == np.max(mins)).flatten()
				
				# Break tie with sum of pairs (u, v) if more than one element in previous step
				if len(maxMins) > 1:
					sums = np.sum(uv, axis = 0)

					# Max value in sums
					index = np.argmax(sums)
				else:
					# Index of max element in mins
					index = np.argmax(mins)

				(i, j) = (-1, -1)
				ans = -1

				# Top half of the phi matrix consists of x (these get negated)
				if phi[index + 1, 0] < len(m): # Add 1 to the index because the first row has the indices defined in line 37
					(i, j) = (phi[index + 1, 0], len(m))
					ans = self.askQuestion(i, j) == 0
				# Lower half of the phi matrix consists of y
				else:
					(i, j) = (len(m), phi[0, index + 1] - len(m)) # Add 1 to the index because the first column has the indices defined in line 37
					ans = self.askQuestion(i, j)

				# Vector in which questions can be inferred
				indicesToFill = np.array([])

				# Lists of tuples with 4 elements
				#	0 -> index of row/column in phi to delete
				#	1 -> index of row/column in the original phi matrix (to get the position in the reachability matrix to infer)
				#	2 -> row in the reachability matrix to infer
				#	3 -> column in the reachability matrix to infer
				questionsToInfer = []

				# Search in column if the answer to the question with best opportunity inference is 0
				if ans == 0:
					indicesToFill = phi[:, index + 1] # Add 1 to the index because the first column has the indices defined in line 37
				# Search in row if the answer to the question with best opportunity inference is 1
				else:
					indicesToFill = phi[index + 1, :] # Add 1 to the index because the first row has the indices defined in line 37

				# Look for 1s in the row or column
				for i in np.arange(1, len(indicesToFill)):
					if indicesToFill[i] == 1:
						answered = answered + 1
						# Top half of phi consists of x (these get negated)
						if phi[i, 0] < len(m):
							questionsToInfer.append((int(i), int(phi[i, 0]), int(phi[i, 0]), int(len(m)))) # (index (to check if its x or y), i (row to fill in reachability matrix), j (column to fill in reachability matrix))
						# Lower half of phi consists of y
						else:
							questionsToInfer.append((int(i), int(phi[i, 0]), int(len(m)), int(phi[0, i] - len(m)))) # (index (to check if its x or y), i (row to fill in reachability matrix), j (column to fill in reachability matrix))

				# Rows/columns to delete
				delete = []
				for question in questionsToInfer:
					# Collect rows/columns to delete after inferring the needed questions
					delete.append(question[0])

					# Top half of phi consists of x (these get negated)
					if question[1] < len(m):
						self.reachability_matrix[question[2], question[3]] = (ans == 0)
					# Lower half of phi consists of y
					else:
						self.reachability_matrix[question[2], question[3]] = ans

				# Delete the rows and columns of x's or y's that have been ansered/inferred
				phi = np.delete(phi, delete, axis = 0)
				phi = np.delete(phi, delete, axis = 1)

	def reachabilityAntecedentSets(self, variable, exclude):
		reachability_set = set()
		antecedent_set = set()
		for i in range(self.variables):
			if self.reachability_matrix[variable][i] == 1:
				reachability_set.add(i)

			if self.reachability_matrix[i][variable] == 1:
				antecedent_set.add(i)

		return (reachability_set - exclude, antecedent_set - exclude)

	def finished(self):
		for key, value in self.variable_level.items():
			if value == -1:
				return False

		return True

	def fill_reachability_matrix(self):
		for variable in range(self.variables):
			visited = [False for j in range(self.variables)]
			stack = []
			stack.append(variable)
			while len(stack) > 0:
				current_variable = stack.pop()
				visited[current_variable] = True
				for other_variable in range(self.variables):
					if visited[other_variable] == False and self.reachability_matrix[current_variable][other_variable] == 1:
						self.reachability_matrix[variable][other_variable] = 1
						stack.append(other_variable)

	def structural_model(self):
		to_exclude = set()
		level = 1
		while not self.finished():
			variables_to_exclude = set()
			for variable in range(self.variables):
				if variable not in to_exclude:
					(reachability_set, antecedent_set) = self.reachabilityAntecedentSets(variable, to_exclude)
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

		print(self.levels)

def main():
	ism = ISM(int(input("Number of variables: ")))
	ism.contextual_relationships()
	ism.structural_model()

if __name__ == '__main__':
	main()