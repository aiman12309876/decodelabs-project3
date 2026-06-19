import random
import math
import time
import heapq
from datetime import datetime

class OccupancyGrid:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.start = (1, 1)
        self.goal = (18, 18)
        self.robot_pos = self.start
        self.obstacles = []
        self.generate_maze()

    def generate_maze(self):
        for i in range(self.height):
            for j in range(self.width):
                if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1:
                    self.grid[i][j] = 1
                elif random.random() < 0.15:
                    if (i, j) != self.start and (i, j) != self.goal:
                        self.grid[i][j] = 1
                        self.obstacles.append((i, j))

    def is_walkable(self, pos):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == 0
        return False

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
        return [n for n in neighbors if self.is_walkable(n)]

    def update_robot_position(self, pos):
        if self.is_walkable(pos):
            self.robot_pos = pos
            return True
        return False

def a_star(grid, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next_pos in grid.get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(goal, next_pos)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    return reconstruct_path(came_from, start, goal)

def heuristic(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path

class AutonomousRobot:
    def __init__(self):
        self.grid = OccupancyGrid()
        self.path = []
        self.current_target_index = 0
        self.moving = False
        self.obstacle_avoidance_distance = 2

    def plan_path(self):
        print("🔄 Planning path from start to goal...")
        self.path = a_star(self.grid, self.grid.start, self.grid.goal)
        if self.path:
            print(f"✅ Path found! {len(self.path)} steps")
            self.current_target_index = 0
            self.moving = True
            return True
        else:
            print("❌ No path found!")
            return False

    def move_robot(self):
        if not self.moving or self.current_target_index >= len(self.path):
            return False

        target = self.path[self.current_target_index]
        current = self.grid.robot_pos

        if self.detect_obstacle(target):
            print("⚠️ Obstacle detected! Rerouting...")
            self.avoid_obstacle()
            return False

        if self.grid.update_robot_position(target):
            self.current_target_index += 1
            print(f"📍 Moved to {target}")
            return True
        return False

    def detect_obstacle(self, target):
        for obs in self.grid.obstacles:
            dist = math.sqrt((target[0] - obs[0])**2 + (target[1] - obs[1])**2)
            if dist < self.obstacle_avoidance_distance:
                return True
        return False

    def avoid_obstacle(self):
        current = self.grid.robot_pos
        possible_moves = self.grid.get_neighbors(current)

        for move in possible_moves:
            if move not in self.path and self.grid.is_walkable(move):
                self.grid.update_robot_position(move)
                print(f"🔄 Rerouted to {move}")
                self.path = a_star(self.grid, move, self.grid.goal)
                if self.path:
                    self.current_target_index = 0
                    return True

        print("❌ No escape route found!")
        self.moving = False
        return False

    def display_grid(self):
        print("\n" + "=" * 60)
        print("   OCCUPANCY GRID")
        print("=" * 60)

        for y in range(self.grid.height):
            row = ""
            for x in range(self.grid.width):
                if (x, y) == self.grid.robot_pos:
                    row += "🤖 "
                elif (x, y) == self.grid.goal:
                    row += "🏁 "
                elif (x, y) in self.path:
                    row += "• "
                elif self.grid.grid[y][x] == 1:
                    row += "█ "
                else:
                    row += ". "
            print(row)

        print("=" * 60)
        print(f"🤖 Robot Position: {self.grid.robot_pos}")
        print(f"🏁 Goal Position: {self.grid.goal}")
        print(f"📊 Path Steps: {len(self.path) if self.path else 0}")
        print(f"🚧 Obstacles: {len(self.grid.obstacles)}")
        print("=" * 60)

    def run(self):
        print("\n" + "=" * 60)
        print("   AUTONOMOUS MOBILE ROBOT (AMR) NAVIGATION")
        print("=" * 60)

        self.display_grid()

        if not self.plan_path():
            print("⚠️ No viable path found. Exiting.")
            return

        print("\n🔄 Starting navigation...\n")

        for step in range(30):
            if not self.moving:
                print("✅ Navigation complete!")
                break

            self.move_robot()
            self.display_grid()
            time.sleep(0.5)

            if self.grid.robot_pos == self.grid.goal:
                print("🎯 Robot has reached the goal!")
                break

        print("\n" + "=" * 60)
        print("   NAVIGATION COMPLETE")
        print("=" * 60)

def main():
    robot = AutonomousRobot()
    robot.run()

if __name__ == "__main__":
    main()