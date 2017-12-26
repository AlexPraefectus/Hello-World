A = {0, -1, 10, 43, 55, 31}
B = {-1, -3, -7, 55, 42, 1, 58}
C = {42, 0, -7, 43}
U = {i for i in range(-7, 59)}


class Variant10:
    """methods make step by step calculations of given expression\n
    result of each step can be obtained by calling initializing object\n
    with appropriate sets and calling method of needed step
    """
    def __init__(self, A_set, B_set, C_set, universal_set):
        self.A = A_set
        self.B = B_set
        self.C = C_set
        self.universal_set = universal_set
        self.result_D = set()
        self.result_X = set()
        self.res_1_d = set()
        self.res_2_d = set()
        self.res_3_d = set()
        self.res_4_d = set()
        self.D_impossible_to_calculate_flag = False

    def step_1_d(self):
        try:
            if not self.res_1_d:
                self.res_1_d = self.A.intersection(self.B)
                return self.res_1_d
            else:
                return self.res_1_d
        except TypeError:
            self.D_impossible_to_calculate_flag = True

    def step_2_d(self):
        try:
            if not self.res_2_d:
                self.res_2_d = self.A.intersection(self.universal_set - self.C)
                return self.res_2_d
            else:
                return self.res_2_d
        except TypeError:
            self.D_impossible_to_calculate_flag = True

    def step_3_d(self):
        try:
            if not self.res_3_d:
                self.res_3_d = (self.universal_set - self.A).intersection(self.B)
                return self.res_3_d
            else:
                return self.res_3_d
        except TypeError:
            self.D_impossible_to_calculate_flag = True

    def step_4_d(self):
        try:
            if not self.res_4_d:
                if not self.res_3_d or not self.res_2_d:
                    self.step_3_d()
                    self.step_2_d()
                self.res_4_d = self.res_3_d.union(self.res_2_d)
                return self.res_4_d
            else:
                return self.res_4_d
        except TypeError:
            self.D_impossible_to_calculate_flag = True

    def step_5_d_final(self):
        try:
            if not self.result_D:
                if not self.res_4_d or not self.res_1_d:
                    self.step_1_d()
                    self.step_4_d()
                self.result_D = self.res_1_d.union(self.res_4_d)
                return self.result_D
            else:
                return self.result_D
        except TypeError:
            self.D_impossible_to_calculate_flag = True


test = Variant10(A, B, C, U)
test.step_1_d()
test.step_2_d()
test.step_3_d()
test.step_4_d()
test.step_5_d_final()
print(test.step_5_d_final())
pass


