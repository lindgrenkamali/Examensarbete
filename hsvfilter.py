class HSVFilter:
    def __init__(self, h_min, s_min, v_min, h_max, s_max, v_max, s_add, s_sub, v_add, v_sub):
        self.H_Min = h_min
        self.S_Min = s_min
        self.V_Min = v_min
        self.H_Max = h_max
        self.S_Max = s_max
        self.V_Max = v_max
        self.S_Add = s_add
        self.S_Sub = s_sub
        self.V_Add = v_add
        self.V_Sub = v_sub