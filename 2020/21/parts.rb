
require 'set';

class ParsedLine
  def initialize(foods, allergens)
    @foods = Set.new(foods.split())
    @allergens = Set.new(allergens.split())
  end

  def allergens()
    return @allergens
  end

  def foods()
    return @foods
  end
end

def get_parsed_lines(filename)
  parsed_lines = []
  File.open(filename, "r") do |input|
    input.each_line() do |line|
      line.chomp!()
      line.gsub!(")", "")
      line.gsub!(",", "")
      line.squeeze!(" ")
      (foods, allergens) = line.split(" (contains ")
      parsed_lines.push(ParsedLine.new(foods, allergens))
    end
  end
  return parsed_lines
end

def get_all_allergens(parsed_lines)
  all_allergens = Set.new()
  parsed_lines.each() do |p|
    all_allergens = all_allergens.union(p.allergens)
  end
  return all_allergens
end

def get_all_foods(parsed_lines)
  all_foods = Set.new()
  parsed_lines.each() do |p|
    all_foods = all_foods.union(p.foods)
  end
  return all_foods
end

def solver(filename)
  # Collect all input
  parsed_lines = get_parsed_lines(filename)
  all_allergens = get_all_allergens(parsed_lines)
  all_foods = get_all_foods(parsed_lines)

  # Pick an allergen and try to figure out which food it is
  food_to_allergen = Hash.new()
  dangerous = []

  # Each allergen maps to exactly 1 food
  # Each food may contain 0 or 1 allergen
  progress = true
  unsolved = true
  while progress do
    progress = false
    unsolved = false
    all_allergens.to_a().sort.each() do |allergen|

      # For each allergen, look at all lines containing that allergen
      # and get the intersection of all foods appearing: one of these
      # foods must contain the allergen
      could_be = Set.new(all_foods)
      parsed_lines.each() do |p|
        if p.allergens.member?(allergen) then
          could_be = could_be.intersection(p.foods)
        end
      end

      if could_be.size() == 0 then
        raise NameError, "eliminated all possibilities?"
      elsif could_be.size() == 1 then
        # one possibility - this is solved
        food = could_be.to_a()[0]
        parsed_lines.each() do |p|
          p.foods.delete(food)
        end
        all_allergens.delete(allergen)
        food_to_allergen[food] = allergen
        dangerous.push([allergen, food])
        puts(allergen + " is " + food)
        progress = true
      else
        # still not solved
        unsolved = true
      end
    end
  end
  if unsolved then
    raise NameError, "problem is not solved"
  end

  # Count ingredients in original list that don't map to allergens
  part1_result = 0
  parsed_lines.each() do |p|
    p.foods.each() do |food|
      if not food_to_allergen.has_key?(food) then
        part1_result += 1
      end
    end
  end

  # make canonical dangerous ingredient list
  part2_result = []
  dangerous.sort().each() do |allergen, food|
    part2_result.push(food)
  end

  return [part1_result, part2_result.join(",")]
end

def main()
  puts("TESTING")
  results = solver("example_input")
  part1_result = results[0]
  part2_result = results[1]
  if part1_result != 5 then
    raise NameError, "part 1 example input test failed"
  end
  if part2_result != "mxmxvkd,sqjhc,fvjkl" then
    raise NameError, "part 2 example input test failed"
  end
  puts("")
  puts("SOLVING")
  results = solver("input")
  part1_result = results[0]
  part2_result = results[1]
  puts("part 1 result = " + part1_result.to_s())
  puts("part 2 result = " + part2_result)
end

main()

