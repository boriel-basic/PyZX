from pygame.locals import *

b4 = 0x10
b3 = 0x08
b2 = 0x04
b1 = 0x02
b0 = 0x01

_B_SPC = 0
_H_ENT = 1
_Y_P = 2
_6_0 = 3
_1_5 = 4
_Q_T = 5
_A_G = 6
_CAPS_V = 7


class Keyboard:
    def __init__(self):
        self.keyboard = [0xff] * 8
        self.joy = [0]

        self.signals = {
            K_1: [_1_5, b0],
            K_2: [_1_5, b1],
            K_3: [_1_5, b2],
            K_4: [_1_5, b3],
            K_5: [_1_5, b4],

            K_6: [_6_0, b4],
            K_7: [_6_0, b3],
            K_8: [_6_0, b2],
            K_9: [_6_0, b1],
            K_0: [_6_0, b0],

            K_q: [_Q_T, b0],
            K_w: [_Q_T, b1],
            K_e: [_Q_T, b2],
            K_r: [_Q_T, b3],
            K_t: [_Q_T, b4],

            K_y: [_Y_P, b4],
            K_u: [_Y_P, b3],
            K_i: [_Y_P, b2],
            K_o: [_Y_P, b1],
            K_p: [_Y_P, b0],

            K_a: [_A_G, b0],
            K_s: [_A_G, b1],
            K_d: [_A_G, b2],
            K_f: [_A_G, b3],
            K_g: [_A_G, b4],

            K_h: [_H_ENT, b4],
            K_j: [_H_ENT, b3],
            K_k: [_H_ENT, b2],
            K_l: [_H_ENT, b1],
            K_RETURN: [_H_ENT, b0],

            K_LCTRL: [_CAPS_V, b0],
            K_z: [_CAPS_V, b1],
            K_x: [_CAPS_V, b2],
            K_c: [_CAPS_V, b3],
            K_v: [_CAPS_V, b4],

            K_b: [_B_SPC, b4],
            K_n: [_B_SPC, b3],
            K_m: [_B_SPC, b2],
            K_RALT: [_B_SPC, b1],
            K_SPACE: [_B_SPC, b0],
        }

    def reset_keyboard(self):
        self.keyboard[_B_SPC] = 0xff
        self.keyboard[_H_ENT] = 0xff
        self.keyboard[_Y_P] = 0xff
        self.keyboard[_6_0] = 0xff
        self.keyboard[_1_5] = 0xff
        self.keyboard[_Q_T] = 0xff
        self.keyboard[_A_G] = 0xff
        self.keyboard[_CAPS_V] = 0xff

        self.joy = [0]

    def do_key(self, down, scan_code, mods):
        caps = (mods & KMOD_CTRL) != 0
        symb = (mods & KMOD_ALT) != 0
        shift = (mods & KMOD_SHIFT) != 0

        if scan_code == K_SPACE:
            caps = shift
        if scan_code == K_RETURN:
            caps = shift
        if scan_code == K_TAB:
            caps = True
            symb = True
        if scan_code == K_BACKSPACE:
            caps = True
            scan_code = K_0

        if scan_code == K_LEFT:
            caps = shift
            scan_code = K_5
        if scan_code == K_DOWN:
            caps = shift
            scan_code = K_6
        if scan_code == K_UP:
            caps = shift
            scan_code = K_7
        if scan_code == K_RIGHT:
            caps = shift
            scan_code = K_8

        # numpad as a kempston
        if scan_code == K_KP8:  # up
            if down:
                self.joy[0] |= 0b00001000
            else:
                self.joy[0] &= 0b11110111
        elif scan_code == K_KP2:  # down
            if down:
                self.joy[0] |= 0b00000100
            else:
                self.joy[0] &= 0b11111011
        elif scan_code == K_KP4:  # left
            if down:
                self.joy[0] |= 0b00000010
            else:
                self.joy[0] &= 0b11111101
        elif scan_code == K_KP6:  # right
            if down:
                self.joy[0] |= 0b00000001
            else:
                self.joy[0] &= 0b11111110
        elif scan_code == K_KP0:  # fire
            if down:
                self.joy[0] |= 0b00010000
            else:
                self.joy[0] &= 0b11101111

        try:
            sig = self.signals[scan_code]

            if down:
                self.keyboard[sig[0]] &= ~sig[1]
            else:
                self.keyboard[sig[0]] |= sig[1]

            if symb & down:
                sig = self.signals[K_RALT]
                self.keyboard[sig[0]] &= ~sig[1]
            else:
                sig = self.signals[K_RALT]
                self.keyboard[sig[0]] |= sig[1]

            if caps & down:
                sig = self.signals[K_LCTRL]
                self.keyboard[sig[0]] &= ~sig[1]
            else:
                sig = self.signals[K_LCTRL]
                self.keyboard[sig[0]] |= sig[1]

        except KeyError:
            pass
