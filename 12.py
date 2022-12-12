import heapq


def parse_input():
    with open('inputs/12.in', 'r') as f:
        return list(map(list, f.read().splitlines()))


def shortest_path(start, end, grid):
    visited = set()

    q = [(0, start)]
    heapq.heapify(q)

    while q:
        path_len, position = heapq.heappop(q)

        if position == end:
            return path_len

        if position in visited:
            continue

        visited.add(position)

        x, y = position
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and 0 <= ord(grid[x][y]) + 1 >= ord(grid[new_x][new_y]):
                heapq.heappush(q, (path_len + 1, (new_x, new_y)))


grid = parse_input()

start = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 'S'][0]
end = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 'E'][0]

# modify grid start and end letters
grid[start[0]][start[1]] = 'a'
grid[end[0]][end[1]] = 'z'


def first_part(grid):
    return shortest_path(start, end, grid)


def second_part(grid):
    starts = [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 'a']
    return min(filter(lambda x: x, [shortest_path(start, end, grid) for start in starts]))


print(first_part(grid))
print(second_part(grid))
