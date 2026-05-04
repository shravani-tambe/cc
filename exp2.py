import heapq
import math

# Colors (ANSI)
RESET = "\033[0m"
RED = "\033[41m"
GREEN = "\033[42m"
YELLOW = "\033[43m"
BLUE = "\033[44m"
MAGENTA = "\033[45m"
CYAN = "\033[46m"
GREY = "\033[100m"
PATHSTEP = "\033[105m"
TENTATIVE = "\033[47m"

class Node:
    def __init__(self, x, y, g, h):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def is_valid(x, y, n, m, maze):
    return 0 <= x < n and 0 <= y < m and maze[x][y] == 0


def print_legend():
    print("\nLegend:")
    print(f"{GREEN}  {RESET} Start  {RED}  {RESET} Goal  {BLUE}  {RESET} Current  "
          f"{PATHSTEP}  {RESET} Path  {YELLOW}  {RESET} Open  "
          f"{TENTATIVE}  {RESET} Tentative Closed  {CYAN}  {RESET} Permanent Closed  "
          f"{GREY}  {RESET} Block\n")


def print_grid(maze, perm_closed, tent_closed, open_map, parent, current, start, goal):
    n, m = len(maze), len(maze[0])
    curr_path = [[False]*m for _ in range(n)]

    temp = current
    while temp != (-1, -1):
        x, y = temp
        curr_path[x][y] = True
        temp = parent[x][y]

    for i in range(n):
        print("+" + "--+"*m)
        for j in range(m):
            print("|", end="")
            if (i, j) == start:
                print(GREEN + "  " + RESET, end="")
            elif (i, j) == goal:
                print(RED + "  " + RESET, end="")
            elif (i, j) == current:
                print(BLUE + "  " + RESET, end="")
            elif curr_path[i][j]:
                print(PATHSTEP + "  " + RESET, end="")
            elif maze[i][j] == 1:
                print(GREY + "  " + RESET, end="")
            elif perm_closed[i][j]:
                print(CYAN + "  " + RESET, end="")
            elif tent_closed[i][j]:
                print(TENTATIVE + "  " + RESET, end="")
            elif open_map[i][j]:
                print(YELLOW + "  " + RESET, end="")
            else:
                print("  ", end="")
        print("|")
    print("+" + "--+"*m)


def print_path(parent, start, goal, maze):
    path = []
    curr = goal

    while curr != (-1, -1):
        path.append(curr)
        curr = parent[curr[0]][curr[1]]

    path.reverse()

    print("\nFinal Path:")
    for p in path:
        print(p, end=" ")
    print("\nPath Length:", len(path) - 1)

    n, m = len(maze), len(maze[0])
    is_path = [[False]*m for _ in range(n)]
    for x, y in path:
        is_path[x][y] = True

    print("\nFinal Grid:")
    for i in range(n):
        print("+" + "--+"*m)
        for j in range(m):
            print("|", end="")
            if (i, j) == start:
                print(GREEN + "  " + RESET, end="")
            elif (i, j) == goal:
                print(RED + "  " + RESET, end="")
            elif is_path[i][j]:
                print(MAGENTA + "  " + RESET, end="")
            elif maze[i][j] == 1:
                print(GREY + "  " + RESET, end="")
            else:
                print("  ", end="")
        print("|")
    print("+" + "--+"*m)


def astar(maze, start, goal):
    n, m = len(maze), len(maze[0])

    open_list = []
    heapq.heappush(open_list, Node(start[0], start[1], 0,
                    heuristic(start[0], start[1], goal[0], goal[1])))

    perm_closed = [[False]*m for _ in range(n)]
    tent_closed = [[False]*m for _ in range(n)]
    open_map = [[False]*m for _ in range(n)]
    g_cost = [[math.inf]*m for _ in range(n)]
    parent = [[(-1, -1)]*m for _ in range(n)]

    g_cost[start[0]][start[1]] = 0
    open_map[start[0]][start[1]] = True

    print_legend()

    while open_list:
        current = heapq.heappop(open_list)
        x, y = current.x, current.y

        if perm_closed[x][y]:
            continue

        perm_closed[x][y] = True
        tent_closed[x][y] = False
        open_map[x][y] = False

        print("\n=====================================")
        print(f"Current Node: ({x},{y}) g={current.g} h={current.h} f={current.f}\n")

        print_grid(maze, perm_closed, tent_closed, open_map, parent, (x, y), start, goal)
        input("Press ENTER to continue...")

        if (x, y) == goal:
            print("\nGoal Reached!")
            print_path(parent, start, goal, maze)
            return

        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny, n, m, maze):
                new_g = g_cost[x][y] + 1
                h = heuristic(nx, ny, goal[0], goal[1])
                f = new_g + h

                print(f"Checking ({nx},{ny}) -> g={new_g}, h={h}, f={f}", end="")

                if new_g < g_cost[nx][ny]:
                    g_cost[nx][ny] = new_g
                    parent[nx][ny] = (x, y)
                    heapq.heappush(open_list, Node(nx, ny, new_g, h))
                    open_map[nx][ny] = True
                    tent_closed[nx][ny] = True
                    print(" -> ADDED")
                else:
                    print(" -> SKIPPED")

    print("\nNo Path Found!")


# -------- MAIN --------
n, m = map(int, input("Enter rows and columns: ").split())

maze = []
print("Enter maze (0 = free, 1 = blocked):")
for _ in range(n):
    maze.append(list(map(int, input().split())))

sx, sy = map(int, input("Enter start (x y): ").split())
gx, gy = map(int, input("Enter goal (x y): ").split())
