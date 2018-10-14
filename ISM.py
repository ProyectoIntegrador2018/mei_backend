class ISM:
	def __init__(self, variables):
		self.variables = variables
		self.reachability_matrix = [[0 for j in range(variables)] for i in range(variables)]
		self.levels = dict()
		self.variable_level = dict()
		for i in range(variables):
			self.variable_level[i] = -1

	def contextual_relationships(self):
		for i in range(self.variables):
			for j in range(i, self.variables):
				if i == j:
					self.reachability_matrix[i][j] = 1
				else:
					print("v. %d influeces %d?" % (i + 1, j + 1))
					print("a. %d is influenced by %d?" % (i + 1, j + 1))
					print("x. %d influence each other %d?" % (i + 1, j + 1))
					print("o. %d and %d do not influece each other?" % (i + 1, j + 1))
					ans = input()
					if ans == 'v':
						self.reachability_matrix[i][j] = 1
					elif ans == 'a':
						self.reachability_matrix[j][i] = 1
					elif ans == 'x':
						self.reachability_matrix[i][j] = 1
						self.reachability_matrix[j][i] = 1
					elif ans == 'o':
						self.reachability_matrix[i][j] = 0
						self.reachability_matrix[j][i] = 0

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
	ism.fill_reachability_matrix()
	ism.structural_model()

if __name__ == '__main__':
	main()