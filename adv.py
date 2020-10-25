from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# These will handle backward traversal 
opposite_direction = { 's': 'n', 'n': 's', 'e': 'w', 'w': 'e' }
reverse_path = [None]

# Visited dict to store our visited rooms
visited = {}


# while we haven't searched through all rooms
while len(visited) < len(room_graph) - 1:

    # if the current room ID has not been visited yet
    if player.current_room.id not in visited:
        # set the current ID to visited and get exits 
        visited[player.current_room.id] = player.current_room.get_exits()

    # while the length of the visited current room's ID == 0
    while len(visited[player.current_room.id]) == 0:
        # set previous path to the reverse path list and pop it
        previous_path = reverse_path.pop()
        # append the previous path to the traversal_path list
        traversal_path.append(previous_path)
        # move to the previous path
        player.travel(previous_path)
    
    next_direction = visited[player.current_room.id].pop()
    traversal_path.append(next_direction)
    reverse_path.append(opposite_direction[next_direction])
    player.travel(next_direction)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
