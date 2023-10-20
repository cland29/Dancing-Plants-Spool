import math
import turtle, random

wn = turtle.Screen()
alex = turtle.Turtle()

wn.setworldcoordinates(-100, 0, 100, 200)

wn.tracer(100)
def main():
    #alex.goto(100,100)
    rand_points = generate_rand_Points(400)
    draw_points(rand_points)
    location_point = [(0,0)]
    for i in range(5):
        for n in range(len(location_point)):
            near_point = find_nearest_point_and_eat(location_point[n], rand_points)
            location_point[n] = rand_points.pop(near_point)

    location_point = [location_point[0], location_point[0]]
    for i in range(5):
        for n in range(len(location_point)):
            near_point = find_nearest_point_and_eat(location_point[n], rand_points)
            location_point[n] = rand_points.pop(near_point)

    location_point = [location_point[0], location_point[0], location_point[1], location_point[1]]
    for i in range(5):
        for n in range(len(location_point)):
            near_point = find_nearest_point_and_eat(location_point[n], rand_points)
            location_point[n] = rand_points.pop(near_point)

    location_point = [location_point[0], location_point[0], location_point[1], location_point[1], location_point[2], location_point[2], location_point[3], location_point[3]]
    for i in range(5):
        for n in range(len(location_point)):
            near_point = find_nearest_point_and_eat(location_point[n], rand_points)
            location_point[n] = rand_points.pop(near_point)




def find_nearest_point_and_eat(point, point_list):
    minDist = 300
    ind = -1
    for i in range(len(point_list)):
        compare_point = point_list[i]
        x_dist = compare_point[0] - point[0]
        y_dist = compare_point[1] - point[1]
        dist = math.sqrt(x_dist**2 + y_dist**2)
        if dist < minDist and compare_point[1] >= point[1]:
            minDist = dist
            ind = i
    connect_two_points(point, point_list[ind])
    return ind

def connect_two_points(point_1, point_2):
    alex.penup()
    alex.goto(point_1[0], point_1[1])
    alex.pendown()
    alex.goto(point_2[0], point_2[1])







def generate_rand_Points(count):
    point_list = []
    for i in range(count):
        point_list.append((random.randint(-100, 100), random.randint(0, 200)))
    return point_list
def draw_points(point_list):
    alex.penup()
    for point in point_list:
        alex.goto(point[0], point[1])
        alex.dot()
    alex.pendown()
if __name__ == "__main__":
    main()
    wn.update()
    input()