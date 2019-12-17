import pygame


class Keyboard:
    '''
    Represents a Hex Keyboard for the Chip-8 inpupt
    There are 16 keys, 0-F

    Key Mapping is as follows to QWERTY

    1=1 2=2 3=3 4=C
    q=4 w=5 e=6 r=D
    a=7 s=8 d=9 f=E
    z=A x=0 c=B v=F
    '''

    def __init__(self):
        self.key_mappings = {
            0x0: pygame.K_x,
            0x1: pygame.K_1,
            0x2: pygame.K_2,
            0x3: pygame.K_3,
            0x4: pygame.K_q,
            0x5: pygame.K_w,
            0x6: pygame.K_e,
            0x7: pygame.K_a,
            0x8: pygame.K_s,
            0x9: pygame.K_d,
            0xA: pygame.K_z,
            0xB: pygame.K_c,
            0xC: pygame.K_4,
            0xD: pygame.K_r,
            0xE: pygame.K_f,
            0xF: pygame.K_v,
        }

    def is_pressed(self, key_to_check):
        keys_pressed = pygame.key.get_pressed()
        return keys_pressed[self.key_mappings[key_to_check]]

    def get_pressed(self):
        keys_pressed = pygame.key.get_pressed()
        for k in self.key_mappings.keys():
            if keys_pressed[self.key_mappings[k]]:
                return k

        return None
