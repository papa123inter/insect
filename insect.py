import pygame
import math

WIDTH, HEIGHT = 1200, 800
SEG_COUNT = 80
SEG_DIST = 8
BODY_WIDTH = 20

class Segment:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0

class Creature:
    def __init__(self):
        self.segments = [Segment(WIDTH/2, HEIGHT/2) for _ in range(SEG_COUNT)]

    def update(self, target_pos):
        head = self.segments[0]
        target = pygame.Vector2(target_pos)
        diff = target - head.pos
        if diff.length() > 2:
            head.angle = math.atan2(diff.y, diff.x)
            head.pos += diff.normalize() * 6.0

        for i in range(1, SEG_COUNT):
            seg = self.segments[i]
            prev = self.segments[i-1]
            d = prev.pos - seg.pos
            seg.angle = math.atan2(d.y, d.x)
            seg.pos = prev.pos - pygame.Vector2(math.cos(seg.angle), math.sin(seg.angle)) * SEG_DIST

    def draw(self, surface):
        for i in range(SEG_COUNT - 1, -1, -1):
            seg = self.segments[i]
            perp = seg.angle + math.pi / 2
            
            width_factor = math.sin((i / SEG_COUNT) * math.pi * 0.9)
            current_width = BODY_WIDTH * width_factor + 5
            
            off_vec = pygame.Vector2(math.cos(perp), math.sin(perp)) * current_width
            p1, p2 = seg.pos + off_vec, seg.pos - off_vec
            
            pygame.draw.line(surface, (200, 200, 200), p1, p2, 1)
            
            if i in [10, 20, 30, 40]:
                for side in [-1, 1]:
                    shoulder = seg.pos + pygame.Vector2(math.cos(perp * side), math.sin(perp * side)) * current_width
                    knee_angle = perp * side + (0.5 * side)
                    knee = shoulder + pygame.Vector2(math.cos(knee_angle), math.sin(knee_angle)) * 30
                    foot = knee + pygame.Vector2(math.cos(knee_angle + 0.3), math.sin(knee_angle + 0.3)) * 15
                    
                    pygame.draw.line(surface, (255, 255, 255), shoulder, knee, 1)
                    pygame.draw.line(surface, (255, 255, 255), knee, foot, 1)
                    for f_angle in [-0.4, 0, 0.4]:
                        finger = foot + pygame.Vector2(math.cos(knee_angle + f_angle), math.sin(knee_angle + f_angle)) * 8
                        pygame.draw.line(surface, (255, 255, 255), foot, finger, 1)

            if i > 0:
                pygame.draw.line(surface, (255, 255, 255), seg.pos, self.segments[i-1].pos, 2)
            
            if i == 0:
                for a in [-0.6, 0.6]:
                    ant_angle = seg.angle + a
                    ant_end = seg.pos + pygame.Vector2(math.cos(ant_angle), math.sin(ant_angle)) * 20
                    pygame.draw.line(surface, (255, 255, 255), seg.pos, ant_end, 1)
                    pygame.draw.circle(surface, (255, 255, 255), (int(ant_end.x), int(ant_end.y)), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    creature = Creature()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
        
        screen.fill((5, 5, 10))
        creature.update(pygame.mouse.get_pos())
        creature.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()