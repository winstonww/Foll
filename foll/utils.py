from foll.models import FoodRating, Food, Party

def find_average_rating(food_id):
	rated_food = Food.objects.get(id = food_id)
	ratings_for_food = FoodRating.objects.all().filter(food = rated_food)
	rating_sum = 0
	counter = 0
	for food_rating in ratings_for_food:
		counter += 1
		rating_sum += food_rating.rating
	if counter == 0:
		return 0
	avg_rating = rating_sum / counter;
	return avg_rating


class TopFood():

	def __init__(self):
		self.rating_array = []
		self.price_array = []
		self.food_id_array = []


		self.rating_array.append(0) #first element is 0
		self.price_array.append(0)
		self.food_id_array.append(0)


	def top_rated_food_under_price_constraints(self, party_id):
		

		# this function returns a list of best food under the price constraint
		best_food = []
		party_of_interest = Party.objects.get(id = party_id)
		party_price_constraint = party_of_interest.max_budget
		all_food_in_party = Food.objects.all().filter(belong_to_party = party_of_interest)

		# Implementation of Knapsack problem
		n = len(all_food_in_party)
		p = party_price_constraint

		# memo[n][p]
		self.memo = [[-1 for x in range(p+1)] for y in range(n+1)]

		for food in all_food_in_party:
			self.food_id_array.append(food.id)
			self.rating_array.append(food.avg_rating)
			self.price_array.append(round(food.price))
		
		max_value = self.MaxValue(n,p)
		# return max_value

		#now let's trace the path ddown from max_value to zero
		while (n > 0):

				
			if self.price_array[n] > p:
				n -= 1

			else:
				child_1 = self.memo[n-1][p]
				child_2 = self.memo[n-1][p - self.price_array[n] ]  + self.rating_array[n]
				if (self.memo[n][p] == child_1):
					n -= 1

				elif (self.memo[n][p] == child_2):
					best_food.append(self.food_id_array[n])
					p -= self.price_array[n]
					n -= 1

				else:
					n -= 1
					
	

		return best_food




	def MaxValue(self, n, p): 
		# nth item with p dollars left

		if (n == 0):
			self.memo[n][p] = 0
			return 0
		# if (p < 0):
		# 	self.memo[n][p] = 0
		# 	return 0
		if(self.memo[n][p] != -1):
			return self.memo[n][p]

		if(self.price_array[n] > p):
			self.memo[n][p] =  self.MaxValue(n-1, p)
			return self.memo[n][p]

		self.memo[n][p] = max(self.rating_array[n] + self.MaxValue(n-1, p-self.price_array[n]), self.MaxValue(n-1, p) )
		return self.memo[n][p]
	
	

# possible errors
# forgot to memoize
# decrement at not the right time
# did not check memoize index

# Google Map API key
# AIzaSyCLVUE5kSGFo3Hx_pmMS2vnVGLdt0ihBfU