from ..types import Game_Object, Vector2, Entity
from .. import settings as s
from .. import sprites
from .. import sounds
from .. import level
from ..extras import accelerate


class Coin(Game_Object):
    def __init__(self, rect):
        super(Coin, self).__init__(rect)
        self.animation = self.Animation(self.pos.y)
        self.deployed = False
        self.collected = False

    def update(self):
        self.animation.anim()
        self.pos.y = self.animation.new_y
        if self.animation.bounce_iteration > 23:
            self.collected = True

        self.check_for_destroy()

    def check_for_destroy(self):
        if self.collected:
            level.coins.remove(self)

    def draw(self):
        view_pos = s.camera.to_view_space(self.pos)
        s.screen.blit(sprites.tile_set, (view_pos.x, view_pos.y), self.animation.current_sprite)

    class Animation():
        def __init__(self, start_height):
            self.current_sprite = sprites.COIN[0]

            self.start_height = start_height
            self.new_y = start_height
            self.anim_timer = s.INITIAL_TIMER_VALUE
            self.anim_frame = 0
            self.bounce_iteration = 0

        def anim(self):
            # Spin
            self.current_sprite = sprites.COIN[self.anim_frame % 4]
            self.anim_timer += s.var_time
            if self.anim_timer > 3 * s.var_time:
                self.anim_frame += 1
                self.anim_timer = 0
            self.bounce_iteration += 0.6

            self.new_y = self.start_height - self.anim_function(self.bounce_iteration)

        def anim_function(self, bounce_iteration):
            # For bounce
            return -(bounce_iteration - 12) ** 2 + 144


class Super_Mushroom(Entity):
    def __init__(self, rect, vel):
        super(Super_Mushroom, self).__init__(vel, rect)

        self.deployed = False
        self.collected = False

        self.animation = self.Animation(self.pos.y)

    def draw(self):
        view_pos = s.camera.to_view_space(self.pos)
        s.screen.blit(sprites.tile_set, (view_pos.x, view_pos.y), sprites.SUPER_MUSHROOM)

    def update(self):
        if self.animation.has_animated:
            accelerate(self, 0, s.GRAVITY)
            self.move()
        else:
            self.animation.deploy_anim()
            self.pos.y = self.animation.new_y

        self.check_for_destroy()

    def check_for_destroy(self):
        if self.collected:
            sounds.power_up.play()
            s.total_score += s.MUSHROOM_SCORE
            level.super_mushrooms.remove(self)

    def move(self):
        if self.vel.x != 0:
            self.move_single_axis(self.vel.x, 0)
        if self.vel.y != 0:
            self.move_single_axis(0, self.vel.y)

    def move_single_axis(self, dx, dy):
        # Collision check
        self.pos.x += dx * s.var_time
        self.pos.y += dy * s.var_time
        other_collider = self.rect.check_collisions(level.static_colliders + level.dynamic_colliders)

        if other_collider is None:
            return
        if dx > 0:
            self.pos.x = other_collider.pos.x - self.rect.w
            self.vel.x = -self.vel.x
        elif dx < 0:
            self.pos.x = other_collider.pos.x + other_collider.rect.w
            self.vel.x = -self.vel.x
        elif dy > 0:
            self.pos.y = other_collider.pos.y - self.rect.h
            self.vel.y = 0
        
    class Animation():
        def __init__(self, start_height):
            self.new_y = start_height
            self.anim_iteration = 0
            self.has_animated = False

        def deploy_anim(self):
            # Mushroom coming out from brick
            if self.anim_iteration == 48:
                self.has_animated = True
            if not self.has_animated:
                self.new_y -= 1
                self.anim_iteration += 1 
