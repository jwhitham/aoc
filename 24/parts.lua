
BLACK = 1
WHITE = nil

function set_internal(grid, y, x, value)
    if grid.cells[y] == nil then
        grid.cells[y] = {}
    end
    grid.cells[y][x] = value
end

function get_internal(grid, y, x)
    if grid.cells[y] == nil then
        return WHITE
    end
    return grid.cells[y][x]
end

function set_black(grid, y, x)
    set_internal(grid, y, x, BLACK)
end

function set_white(grid, y, x)
    set_internal(grid, y, x, WHITE)
end

function is_black(grid, y, x)
    return get_internal(grid, y, x) == BLACK
end

function count_black_tiles(grid)
    local count = 0
    for y, row in pairs(grid.cells) do
        for x, tile in pairs(row) do
            if tile == BLACK then
                count = count + 1
            end
        end
    end
    return count
end

function mark_adjacent(new_grid, y, x)
    current = get_internal(new_grid, y, x)
    if current == WHITE then
        -- adjacent to one black tile
        set_internal(new_grid, y, x, 1)
    else
        -- adjacent to one more black tile
        set_internal(new_grid, y, x, current + 1)
    end
end

function count_adjacent_black(new_grid, y, x)
    if is_black(new_grid, y, x) then
        return 1
    else
        return 0
    end
end

function new_day(old_grid)
    local new_grid = create_grid()

    for y, row in pairs(old_grid.cells) do
        for x, tile in pairs(row) do
            if tile == BLACK then
                -- black tile here: all adjacent hex tiles
                -- are marked with a number representing
                -- the number of adjacent black tiles
                mark_adjacent(new_grid, y - 2, x - 1)
                mark_adjacent(new_grid, y - 2, x + 1)
                mark_adjacent(new_grid, y, x + 2)
                mark_adjacent(new_grid, y + 2, x + 1)
                mark_adjacent(new_grid, y + 2, x - 1)
                mark_adjacent(new_grid, y, x - 2)
            end
        end
    end

    for y, row in pairs(new_grid.cells) do
        for x, count in pairs(row) do
            if is_black(old_grid, y, x) then
                -- count adjacent black tiles
                if count == 0 or count > 2 then
                    set_white(new_grid, y, x)
                else
                    set_black(new_grid, y, x)
                end
            else
                -- count adjacent black tiles
                if count == 2 then
                    set_black(new_grid, y, x)
                else
                    set_white(new_grid, y, x)
                end
            end
        end
    end
      
    return new_grid
end

function create_grid()
    local grid = {}
    grid.set_black = set_black
    grid.set_white = set_white
    grid.is_black = is_black
    grid.count_black_tiles = count_black_tiles
    grid.new_day = new_day
    grid.cells = {}
    return grid
end

function get_initial_state(filename)
    local grid = create_grid()

    for line in io.lines(filename) do
        local x = 0
        local y = 0
        local dx = 2
        local dy = 0
        for i = 1, line:len() do
            local op = line:sub(i, i)

            if op == "n" then
                dy = -2
                dx = 1
            elseif op == "s" then
                dy = 2
                dx = 1
            elseif op == "w" then
                x = x - dx
                y = y + dy
                dx = 2
                dy = 0
            elseif op == "e" then
                x = x + dx
                y = y + dy
                dx = 2
                dy = 0
            else
                print("unknown op " + op)
                return -1
            end
        end
        if grid:is_black(y, x) then
            grid:set_white(y, x)
        else
            grid:set_black(y, x)
        end
    end
    return grid
end

function part1(filename) 
    return get_initial_state(filename):count_black_tiles()
end

function part2(filename)
    local grid = get_initial_state(filename)
    for day = 1, 100 do
        grid = grid:new_day()
    end
    return grid:count_black_tiles()
end

if (part1("example_input") == 10) then
    print("Part 1 result", part1("input"))
    if (part2("example_input") == 2208) then
        print("Part 2 result", part2("input"))
    else
        print("Part 2 test error")
    end
else
    print("Part 1 test error")
end


