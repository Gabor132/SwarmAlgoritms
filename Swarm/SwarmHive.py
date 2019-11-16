import random
import time
from enum import Enum
import operator
import math
from graphics import *


def normalize(x, y):
    length = math.sqrt((x ** 2) + (y ** 2))
    x = x / length
    y = y / length
    return (x, y)

class Obstacle:

    def __init__(self, width : int = 600, height : int = 400):
        self.x = random.randrange(width)
        self.y = random.randrange(height)
        self.size = random.randrange(20, 100)

    def draw(self, win):
        pt = Point(self.x, self.y)
        cir = Circle(pt, self.size-10)
        cir.setFill('black')
        cir.draw(win)


class BoidType(Enum):
    LEADER = 1
    FOLLOWER = 2

class Boid:

    index = 0

    def __init__(self, width : int=600, height : int=400, speed : int = 10, min_separation : int = 100,
                 boid_type: BoidType = BoidType.FOLLOWER):
        self.index = Boid.index
        Boid.index = Boid.index + 1
        self.x = random.randrange(width)
        self.y = random.randrange(height)
        self.v1 = random.randrange(10,30)
        self.v2 = random.randrange(10,30)
        self.v1_cohesion = 0
        self.v2_cohesion = 0
        self.v1_separation = 0
        self.v2_separation = 0
        self.v1_alignment = 0
        self.v2_alignment = 0
        self.min_separation = min_separation
        self.speed = speed
        self.type = boid_type
        self.nearby_boids = []
        self.target_x = 0
        self.target_y = 0
        self.trail_x = 0
        self.trail_y = 0
        self.win_max_width = width
        self.win_max_height = height
        self.has_leader_nearby = False
        self.ahead_x = self.v1
        self.ahead_y = self.v2
        self.avoid_x = 0
        self.avoid_y = 0
        self.follow_leader_x = 0
        self.follow_leader_y = 0

    def set_type(self, type : BoidType = BoidType.FOLLOWER):
        self.type = type

    def normalize_speed(self):
        v1 = self.v1
        v2 = self.v2
        length = math.sqrt((self.v1**2) + (self.v2 ** 2))
        v1 = self.v1 / length
        v2 = self.v2 / length
        self.v1 = v1
        self.v2 = v2
        return (v1, v2)

    def has_nearby_boids(self):
        has_neighbors = len(self.nearby_boids) > 0
        return has_neighbors

    def cohesion(self):
        avg_x = 0
        avg_y = 0
        if len(self.nearby_boids) == 0:
            self.v1_cohesion = 0
            self.v2_cohesion = 0
            return
        if self.type == BoidType.LEADER:
            return
        contains_leader = False
        for boid in self.nearby_boids:
            avg_x += boid.x
            avg_y += boid.y
        avg_x = avg_x/len(self.nearby_boids)
        avg_y = avg_y/len(self.nearby_boids)
        distance = math.sqrt((self.x - avg_x)**2+(self.y - avg_y)**2)
        avg_x = self.x - avg_x
        avg_y = self.y - avg_y

        if distance > 0:
            length = math.sqrt((avg_x**2) + (avg_y ** 2))
            avg_x = avg_x/length
            avg_y = avg_y/length
            avg_x = avg_x * (distance/100.0)
            avg_y = avg_y * (distance/100.0)
            avg_x = avg_x - self.v1
            avg_y = avg_y - self.v2
            self.v1_cohesion = avg_x
            self.v2_cohesion = avg_y
        else:
            self.v1_cohesion = 0
            self.v2_cohesion = 0

    def separation(self):
        avg_x = 0
        avg_y = 0
        if len(self.nearby_boids) == 0:
            self.v1_separation = 0
            self.v2_separation = 0
            return
        if self.type == BoidType.LEADER:
            return
        nr_really_close_boids = 0
        for boid in self.nearby_boids:
            distance = math.sqrt((self.x - boid.x)**2+(self.y - boid.y)**2)
            if distance <= self.min_separation:
                dif_x = self.x - boid.x
                dif_y = self.y - boid.y
                length = math.sqrt((dif_x**2) + (dif_y ** 2))
                dif_x = dif_x / length
                dif_y = dif_y / length
                dif_x = dif_x / distance
                dif_y = dif_y / distance
                avg_x = avg_x + dif_x
                avg_y = avg_y + dif_y
                nr_really_close_boids += 1
        if nr_really_close_boids > 0:
            self.v1_separation = avg_x / nr_really_close_boids
            self.v2_separation = avg_y / nr_really_close_boids

    def alignment(self):
        avg_x = 0
        avg_y = 0
        if len(self.nearby_boids) == 0:
            self.v1_alignment = 0
            self.v2_alignment = 0
            return
        if self.type == BoidType.LEADER:
            return
        contains_leader = False
        for boid in self.nearby_boids:
            if boid.type == BoidType.LEADER:
                avg_x += boid.v1
                avg_y += boid.v2
        self.v1_alignment = avg_x / len(self.nearby_boids)
        self.v2_alignment = avg_y / len(self.nearby_boids)

    def draw_boid(self, win, debug):
        (v1, v2) = self.normalize_speed()
        pt = Point(self.x, self.y)
        pt2 = Point(self.x+v1*20, self.y+v2*20)
        pt_cohesion = Point(self.x + self.v1_cohesion, self.y + self.v2_cohesion)
        pt_separation = Point(self.x + self.v1_separation, self.y + self.v2_separation)
        pt_alignment = Point(self.x + self.v1_alignment, self.y + self.v2_alignment)
        pt_avoid = Point(self.ahead_x, self.ahead_y)
        dir = Line(pt, pt2)
        dir.setFill('black')
        dir_cohesion = Line(pt, pt_cohesion)
        dir_cohesion.setFill('green')
        dir_separation = Line(pt, pt_separation)
        dir_separation.setFill('black')
        dir_alignment = Line(pt, pt_alignment)
        dir_alignment.setFill('orange')
        dir_avoid = Line(pt, pt_avoid)
        dir_avoid.setFill('pink')
        cir = Circle(pt, 5)
        cir_visible = Circle(pt, 100)
        cir_visible.setOutline('red')
        if self.type == BoidType.LEADER:
            cir.setFill('blue')
        elif self.type == BoidType.FOLLOWER:
            cir.setFill('red')
        if self.has_nearby_boids():
            cir_visible.setOutline('green')
        cir.draw(win)
        dir.draw(win)
        if debug:
            cir_visible.draw(win)
            if self.has_nearby_boids() and self.type != BoidType.LEADER:
                dir_cohesion.draw(win)
                dir_separation.draw(win)
                dir_alignment.draw(win)
            dir_avoid.draw(win)
            if self.type == BoidType.LEADER:
                pt_trail = Point(self.trail_x, self.trail_y)
                cir_trail = Circle(pt_trail, 1)
                cir_trail.setFill('green')
                cir_trail.draw(win)

    def find_nearby_boids(self, boid_list):
        self.nearby_boids.clear()
        self.has_leader_nearby = False
        for possible_neighbor in boid_list:
            if self.index == possible_neighbor.index:
                continue
            if(math.sqrt((self.x - possible_neighbor.x)**2+(self.y - possible_neighbor.y)**2) < 100):
                if possible_neighbor.type == BoidType.LEADER:
                    self.has_leader_nearby = True
                    self.target_x = possible_neighbor.x - possible_neighbor.v1
                    self.target_y = possible_neighbor.y - possible_neighbor.v2
                self.nearby_boids.append(possible_neighbor)

    def setType(self, boid_type: BoidType):
        self.type = boid_type
        if self.type == BoidType.LEADER:
            self.target_x = random.randrange(100, 300)
            self.target_y = random.randrange(100, 300)
        else:
            self.target_x = 0
            self.target_y = 0
            
    def is_in_window_bound(self):
        if self.ahead_x > self.win_max_width and self.v1 > 0:
            self.v1 = -self.v1
            return False
        elif self.ahead_y > self.win_max_height and self.v2 >0:
            self.v2 = -self.v2
            return False
        elif self.ahead_x < 0 and self.v1 < 0:
            self.v1 = -self.v1
            return False
        elif self.ahead_y < 0 and self.v2 < 0:
            self.v2 = -self.v2
            return False
        else:
            return True

    def move(self, time, SEPARATION_WEIGHT : int = 1, ALIGNMENT_WEIGHT : int = 1,  COHESION_WEIGHT : int = 1):
        if self.avoid_x == 0:
            if self.has_nearby_boids() and self.type == BoidType.FOLLOWER:
                self.v1 += self.v1_separation * SEPARATION_WEIGHT + self.v1_alignment * ALIGNMENT_WEIGHT + self.v1_cohesion * COHESION_WEIGHT
                self.v2 += self.v2_separation * SEPARATION_WEIGHT + self.v2_alignment * ALIGNMENT_WEIGHT + self.v2_cohesion * COHESION_WEIGHT
                self.v1 += self.follow_leader_x
                self.v2 += self.follow_leader_y
        self.v1 += self.avoid_x
        self.v2 += self.avoid_y
        (v1, v2) = self.normalize_speed()
        self.x = self.x + v1*time*self.speed
        self.y = self.y + v2*time*self.speed
        self.is_in_window_bound()

    def check_for_obstacles(self, obstacle_list, MAX_LOOK_AHEAD, MAX_AVOID_FORCE):
        (self.ahead_x, self.ahead_y) = normalize(self.v1, self.v2)
        if self.type == BoidType.LEADER:
            MAX_LOOK_AHEAD *= 2
        self.ahead_x *= MAX_LOOK_AHEAD
        self.ahead_y *= MAX_LOOK_AHEAD
        self.ahead_x += self.x
        self.ahead_y += self.y
        ahead_x_2 = self.ahead_x / 2
        ahead_y_2 = self.ahead_y / 2
        min_distance = 600
        most_threatening = None
        for obstacle in obstacle_list:
            distance = math.sqrt((self.ahead_x - obstacle.x)**2 + (self.ahead_y - obstacle.y)**2)
            distance2 = math.sqrt((ahead_x_2 - obstacle.x)**2 + (ahead_y_2 - obstacle.y)**2)
            if distance < obstacle.size or distance2 < obstacle.size:
                distance = math.sqrt((self.x - obstacle.x)**2 + (self.y - obstacle.y)**2)
                if distance < min_distance:
                    most_threatening = obstacle
                    min_distance = distance
        if most_threatening is not None:
            self.avoid_x = self.ahead_x - most_threatening.x
            self.avoid_y = self.ahead_y - most_threatening.y
            (self.avoid_x, self.avoid_y) = normalize(self.avoid_x, self.avoid_y)
            self.avoid_x = self.avoid_x * MAX_AVOID_FORCE
            self.avoid_y = self.avoid_y * MAX_AVOID_FORCE
        else:
            self.avoid_x = 0
            self.avoid_y = 0

    def check_for_colision(self, obstacle_list):
        for obstacle in obstacle_list:
            distance = math.sqrt((self.x - obstacle.x)**2 + (self.y - obstacle.y)**2)
            if distance < obstacle.size:
                x_outside = self.x - obstacle.x
                y_outside = self.y - obstacle.y
                (x_outside, y_outside) = normalize(x_outside, y_outside)
                x_outside *= distance/obstacle.size
                y_outside *= distance/obstacle.size
                self.x = self.x + x_outside
                self.y = self.y + y_outside
                break

    def follow_leader(self, leader, LEADER_BEHIND_DIST):
        if self.type == BoidType.LEADER:
            return
        distance = math.sqrt((self.x - leader.x) ** 2 + (self.y - leader.y) ** 2)
        if distance > 100:
            self.follow_leader_x = 0
            self.follow_leader_y = 0
            return
        target_leader_x = leader.v1 * -1
        target_leader_y = leader.v2 * -1
        (target_leader_x, target_leader_y) = normalize(target_leader_x, target_leader_y)
        target_leader_x *= LEADER_BEHIND_DIST
        target_leader_y *= LEADER_BEHIND_DIST
        target_leader_x = leader.x + target_leader_x
        target_leader_y = leader.y + target_leader_y
        leader.trail_x = target_leader_x
        leader.trail_y = target_leader_y
        self.follow_leader_x = target_leader_x - self.x
        self.follow_leader_y = target_leader_y - self.y



def SwarmHive(nr_boids, nr_obstacles, win, debug):
    boids_list = []
    obstacles_list = []
    # Creating the boids
    for i in range(nr_boids):
        boid = Boid(win.width, win.height, 50)
        boids_list.append(boid)
    for i in range(nr_obstacles):
        obstacle = Obstacle(win.width, win.height)
        obstacles_list.append(obstacle)
    # Setting up the LEADER
    boids_list[0].set_type(BoidType.LEADER)
    start_time = time.time()
    elapsed_time = time.time() - start_time
    for i in range(10000):
        for boid in boids_list:
            boid.find_nearby_boids(boids_list)
            boid.cohesion()
            boid.separation()
            boid.alignment()
            boid.check_for_obstacles(obstacles_list, 25, 0.3)
            boid.follow_leader(boids_list[0], 20)
            boid.draw_boid(win, debug=debug)
            if boid.follow_leader_x == 0 and boid.type == BoidType.FOLLOWER:
                separation_width = 20
            else:
                separation_width = 1000
            boid.move(elapsed_time, SEPARATION_WEIGHT=separation_width, ALIGNMENT_WEIGHT= 1, COHESION_WEIGHT=-1)
            boid.check_for_colision(obstacle_list=obstacles_list)
        for obstacle in obstacles_list:
            obstacle.draw(win)
        time.sleep(0.01)
        current_time = time.time()
        elapsed_time = current_time-start_time
        start_time = current_time
        win.update()
        win.delete('all')

def main(debug):
    win = GraphWin("Boids, boids, baby", 1000, 600, autoflush=False)
    SwarmHive(30, 10,  win, debug=debug)
    win.getMouse()
    win.close()

main(True)