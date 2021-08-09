# -*- coding: utf-8 -*-
import csv
from queue import PriorityQueue
from io import open
import os

#file path.
FILE_PATH = os.getcwd() + "/data/cities.csv"

#store the cities and their neighboring cities in a dictionary.
cities = {}

#Prints the "cities" dictionary.
def PrintCities(cities):
    for city in cities:
        print(city, cities[city].neighbors)

#This exception is thrown when a desired city is not found in the dictionary.
class CityNotFoundError(Exception):
    def __init__(self, city):
        pass

#Each city in our graph is represented as a Node.
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}


# Implement this function to read data into an appropriate data structure.
# As an additional feature, you can choose to print the graph by passing True or False.
def build_graph(path, printMap):
    with open(FILE_PATH,"r", encoding="UTF-8") as file:
        reader = csv.reader(file)
        #Evade reading first line because it contains information about the columns.
        next(reader)

        #Extract all the cities and put them into the dictionary named "cities".
        for line in reader:
            #Assign each line to a variable for better readability.
            city1 = line[0].lower()
            city2 = line[1].lower()
            weight = line[2]

            #Add cities to the dictionary if they don't already exist
            if city1 not in cities:
                cities[city1] = Node(city1)
            if city2 not in cities:
                cities[city2] = Node(city2)
            
            #Add the weight(distance) of each edge between the cities.
            cities[city1].neighbors[city2] = int(weight)
            cities[city2].neighbors[city1] = int(weight)

    #If printMap is true, print the graph to the console.
    if printMap:
        PrintCities(cities)

   
# Implement this function to perform uniform cost search on the graph.
def uniform_cost_search(graph, start, end):
    #Check if cities exist in the cities dictionary before doing anything. If not, throw our custom exception.
    if start not in cities:
        raise CityNotFoundError(start)
    if end not in cities:
        raise CityNotFoundError(end)

    #Set data structure named visited in order to store the nodes we have visited in the graph.
    visited = set()
    #PriorityQueue data structure is an essential part of the UCS.
    queue = PriorityQueue()
    #Insert the starting city into queue with cost of 0.
    queue.put((0, start, [start]))

    #Iterate the queue until you reach the target city.
    while queue:
        #Retrieve the elements on top of the queue.
        cost, current, route = queue.get()

        #If our current node is not visited, execute code block given below.
        if current not in visited:
            visited.add(current)

            #If the node we are at is the target city, print the route and the cost of this path and exit the function.
            if current == end:
                print("From city "+start+" to "+end+",the shortest route is: ")
                print(" -> ".join(route))
                print("With cost of", cost, "unit distance.\n")
                return

            #Retrieve the neighbors of the current node.
            neighbors = cities[current].neighbors
            #Iterate through every city in neighbors of current node.
            for city in neighbors: 
                #If the neighbor city is not visited:
                if city not in visited:
                    #For better semantics, cumulative cost is calculated in another variable called total_cost.
                    total_cost = cost + neighbors[city]
                    #Insert the unvisited neighbor city of the current node into our PriorityQueue.
                    queue.put((total_cost, cities[city].name, route + [cities[city].name]))


# Implement main to call functions with appropriate try-except blocks
if __name__ == "__main__":
    #Read the file and initialize the graph, later print it.
    build_graph(FILE_PATH, True)

    #Test cities.
    while True:
        try:
            print("Please write exit to terminate the program.\n") 
            departure = input("Please enter the city of departure:").strip().replace(" ", "").lower()
            
            if departure == 'exit':
                print("Bye!")
                break
            
            arrival = input("Please enter the city of arrival:").strip().replace(" ", "").lower()

            if arrival == 'exit':
                print("Bye!")
                break

            uniform_cost_search(cities, departure, arrival)
      
        except CityNotFoundError as cne:
            print("City named", cne.args[0], "couldn't be found.")