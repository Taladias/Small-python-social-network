from collections import deque #this is used for efficient breadth first search in the graph (O(1) complexity)

import random #we could use faker too if we wanted (from faker import Faker)

import time

class SocialNetwork:
    def __init__(self):
        self.graph = {}
        self.first_names = ["John", "Aliki", "Menelaos", "Emmanouela", "Kiriaki", "Olivia", "George", "Sophia", "William", "Emily"]
        self.last_names = ["Smithers", "Huancan", "Berolm", "Onion", "Papadopoulos", "Mariliou", "Dafnontas", "Garcia", "Rodriguez", "Wilson"]

    def add_member(self, member):
        if member not in self.graph:
            self.graph[member] = {'followers': set(), 'following': set(), 'likes': {}, 'comments': {}}

    def add_interaction(self, from_member, to_member, likes=0, comments=0):
        self.add_member(from_member)
        self.add_member(to_member)
        if to_member not in self.graph[from_member]['following']:
            self.graph[from_member]['following'].add(to_member)
            self.graph[to_member]['followers'].add(from_member)
        self.graph[from_member]['likes'][to_member] = likes
        self.graph[from_member]['comments'][to_member] = comments

    def calculate_engagement_rate(self, member):
        total_likes = sum(self.graph[member]['likes'].values())
        total_comments = sum(self.graph[member]['comments'].values())
        total_engagement = total_likes + total_comments
        followers_count = len(self.graph[member]['followers'])
        if followers_count == 0:
            return 0
        return total_engagement / followers_count

    def calculate_influence(self, member_a, member_b):
        engagement_rate_a = self.calculate_engagement_rate(member_a)
        likes_to_b = self.graph[member_a]['likes'].get(member_b, 0)
        comments_to_b = self.graph[member_a]['comments'].get(member_b, 0)
        if engagement_rate_a == 0:
            return 0
        return (likes_to_b + comments_to_b) / engagement_rate_a

    def calculate_all_engagement_rates(self):
        engagement_rates = {}
        for member in self.graph:
            engagement_rates[member] = self.calculate_engagement_rate(member)
        return engagement_rates

    def shortest_path(self, start_member, end_member):
        if start_member not in self.graph or end_member not in self.graph:
            return None

        visited = set()
        queue = deque([(start_member, [start_member])])

        while queue:
            current_member, path = queue.popleft()
            if current_member == end_member:
                return path
            if current_member not in visited:
                visited.add(current_member)
                for neighbor in self.graph[current_member]['following']:
                    queue.append((neighbor, path + [neighbor]))

        return None

    def path_with_highest_engagement(self, start_member, end_member):
        if start_member not in self.graph or end_member not in self.graph:
            return None

        visited = set()
        max_engagement_path = None
        max_engagement = 0
        queue = deque([(start_member, [start_member], 0)])

        while queue:
            current_member, path, current_engagement = queue.popleft()
            if current_member == end_member and current_engagement > max_engagement:
                max_engagement_path = path
                max_engagement = current_engagement
            if current_member not in visited:
                visited.add(current_member)
                for neighbor in self.graph[current_member]['following']:
                    engagement_to_neighbor = self.calculate_influence(current_member, neighbor)
                    queue.append((neighbor, path + [neighbor], current_engagement + engagement_to_neighbor))

        return max_engagement_path
    
    def generate_random_data(self, num_members, num_interactions):
        # Picks random member names (from a given list above)
        members = [f"{random.choice(self.first_names)} {random.choice(self.last_names)}" for _ in range(num_members)]

        for member in members:
            self.add_member(member)

        # Generates random interactions
        for _ in range(num_interactions):
            from_member = random.choice(members)
            to_member = random.choice(members)
            likes = random.randint(0, 100) #likes given from 0 to 100
            comments = random.randint(0, 50) #comments given from 0 to 50
            self.add_interaction(from_member, to_member, likes, comments)

    def get_members(self):
        return list(self.graph.keys())



social_network = SocialNetwork()

time.sleep(0.5)
print('Welcome to the social network!')

number_of_members = int(input('Please enter how many members you want in the network: '))
number_of_interactions = int(input('Great! Now please enter how many interactions you want to happen inside the social network (It is recommended you enter a number x10 the amount of members): '))

print ("Awesome! The social network is starting...\n")

social_network.generate_random_data(number_of_members, number_of_interactions) #we give how many members and how many interactions we want

while True:
    time.sleep(2)
    action = int(input('Please select an action by typing the number associated with it:\n1. View all engagement rates of the members\n2. Find and display the shortest path between two members\n3. Find and display the path with the highest engagement between two members\n4. Exit the application\n\nType your action here (Please make sure your answer is ONLY a number): '))
    
    if action == 1:
        all_engagement_rates = social_network.calculate_all_engagement_rates()

        for member, rate in all_engagement_rates.items():
            print(f"{member}'s engagement rate: {rate} %\n")
            time.sleep(0.1)
        
    
    elif action == 2:
        members = social_network.get_members()
        print("Members in the network:\n")
        for member in members:
            print(member, '\n')
            time.sleep(0.1)
        
        start_member = input('Type the start member (Full name): ')
        while start_member not in members:
            print("Invalid member name. Please type the full name of a member in the network.\n")
            start_member = input('Type the start member (Full name): ')
        
        end_member = input('Type the end member (Full name): ')
        while end_member not in members:
            print("Invalid member name. Please type the full name of a member in the network.\n")
            end_member = input('Type the end member (Full name): ')

        shortest_path = social_network.shortest_path(start_member, end_member)
        if shortest_path:
            print(f"The shortest path between {start_member} and {end_member} is: {shortest_path}\n")
            print(f"Number of steps: {len(shortest_path) - 1}\n")
        else:
            print(f"No path exists between {start_member} and {end_member}\n")
    
    elif action == 3:
        members = social_network.get_members()
        print("Members in the network:\n")
        for member in members:
            print(member, '\n')
            time.sleep(0.1)
        
        start_member = input('Type the start member (Full name): ')
        while start_member not in members:
            print("Invalid member name. Please type the full name of a member in the network.\n")
            start_member = input('Type the start member (Full name): ')
        
        end_member = input('Type the end member (Full name): ')
        while end_member not in members:
            print("Invalid member name. Please type the full name of a member in the network.\n")
            end_member = input('Type the end member (Full name): ')
        
        highest_engagement_path = social_network.path_with_highest_engagement(start_member, end_member)

        if highest_engagement_path:
            print(f"The path with the highest engagement between {start_member} and {end_member} is: {highest_engagement_path}\n")
        else:
            print(f"No path exists between {start_member} and {end_member}\n")

    elif action == 4:
        break
    
    else:
        print('You had a typo please try again!\n')

    








