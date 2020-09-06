import numpy as np
import warnings
# Robot coordinate class
# TODO include subclasses that correspond to individual legs.

# Helper functions
def to_rads(self, num):
    return num*np.pi/180
def to_degs(self, num):
    return num/np.pi*180
def pythagoras(self, nums):
    return np.sqrt(np.sum(np.power(nums, 2), axis=1))

class hexapod:
    # As always, leg order is (R123,L321) and coords are (x,y,z)
    # DO NOT WRITE TO THESE DIRECLTY - getter/setter
    _leg_end_loc = np.zeros((6,3)) # Local coordinates of leg tips
    _leg_ori_loc = np.zeros((6,3)) # local coordinates of leg origins (local to each leg)
    _leg_end_abs = np.zeros((6,3)) # absolute coordinates
    _leg_ori_abs = np.zeros((6,3))
    _leg_angle = np.zeros(6) # Each leg's coxa angle (gamma)
    _body_z = 68.825 # Body origin (0,0,z)
    _roll = 0.0
    _pitch = 0.0

    # body parameters
    X0_LEN = 45.768
    Y0_LEN = 26.424
    Y1_LEN = 52.848
    OFFSET_ROLL = np.array((Y0_LEN, Y1_LEN, Y0_LEN, -Y0_LEN, -Y1_LEN, -Y0_LEN)) # Roll modifies Z based on y-coord
    OFFSET_PITCH = np.array((X0_LEN, 0.0, -X0_LEN, -X0_LEN, 0.0, X0_LEN)) # Pitch modifies Z based on x-coord
    OFFSET_ANGLE = np.array((30, 90, 150, 210, 270, 330), dtype='float32') # Modify angle offset for each
    
    def __init__(self, leg_end_loc=None, leg_ori_loc=None, leg_end_abs=None, 
                leg_angle=np.array((90.0, 90.0, 90.0, 90.0, 90.0, 90.0)), body_z=68.825, roll=0.0, pitch=0.0):

        self._leg_angle = leg_angle # initialise these constants
        self._body_z = body_z
        self._roll = roll
        self._pitch = pitch

        # Set leg origins based on roll and pitch settings
        self._leg_ori_loc[:, 2] = self._body_z + self.OFFSET_ROLL*np.sin(self.to_rads(self._roll)) + self.OFFSET_PITCH*np.sin(self.to_rads(self._pitch))
        self._leg_ori_abs[:, 0] = self.OFFSET_PITCH*np.cos(self.to_rads(self._pitch))
        self._leg_ori_abs[:, 1] = self.OFFSET_ROLL*np.cos(self.to_rads(self._roll))

        if leg_end_loc is None: 
            if leg_end_abs is None:
                print("Specify local or absolute coordinates for leg tips!")
            else:
                # print("Setting leg tips absolutely")
                self.set_leg_end_abs(leg_end_abs)
        elif leg_end_abs is not None:
            print("Only local or absolute coordinates for leg tips should be given!")
        
        else:
            # print("Setting leg tips locally")
            self.set_leg_end_loc(leg_end_loc)

    # Helper functions
    def to_rads(self, num):
        return num*np.pi/180
    def to_degs(self, num):
        return num/np.pi*180
    def pythagoras(self, nums):
        return np.sqrt(np.sum(np.power(nums, 2), axis=1))

    # Sets local value for leg tip, and changes other relevant values
    def set_leg_end_loc(self, newval):
        self._leg_end_loc = newval
        self._leg_end_abs[:, 2] = self._leg_end_loc[:, 2] # Z is absolute
        leg_len = self.pythagoras(self._leg_end_loc[:, 0:2])
        phi = 180-self.OFFSET_ANGLE-self._leg_angle
        self._leg_end_abs[:, 0] = self._leg_ori_abs[:, 0] + leg_len*np.sin(self.to_rads(phi))
        self._leg_end_abs[:, 1] = self._leg_ori_abs[:, 1] + leg_len*np.cos(self.to_rads(phi))

    # Sets absolute value for leg tip, and changes other relevant values
    # Overwrites angle as well
    def set_leg_end_abs(self, newval):
        self._leg_end_abs = newval
        self._leg_end_loc[:, 2] = self._leg_end_abs[:, 2] # Z is absolute
        delta_xy = self._leg_end_abs[:, 0:2] - self._leg_ori_abs[:, 0:2]
        leg_len = self.pythagoras(delta_xy)
        self._leg_angle = self.to_degs( np.arctan2(delta_xy[1], delta_xy[0]) ) - self.OFFSET_ANGLE
        self._leg_end_loc[:, 0] = leg_len[:, 0] * np.sin(self.to_rads(self._leg_angle))
        self._leg_end_loc[:, 1] = leg_len[:, 1] * np.cos(self.to_rads(self._leg_angle))

    # Sets value for leg angle - changes absolute leg positions(x,y) as well
    def set_leg_angle(self, newval):
        self._leg_angle = newval
        leg_len = self.pythagoras(self._leg_end_loc[:, 0:2])
        phi = 180-self.OFFSET_ANGLE-self._leg_angle
        self._leg_end_abs[:, 0] = self._leg_ori_abs[:, 0] + leg_len*np.sin(self.to_rads(phi))
        self._leg_end_abs[:, 1] = self._leg_ori_abs[:, 1] + leg_len*np.cos(self.to_rads(phi))

    # Rolls the body. Body absolute and relative coordinates change.
    def body_roll(self, roll):
        self._roll = roll
        self._leg_ori_loc[:, 2] = self._body_z + self.OFFSET_ROLL*np.sin(self.to_rads(self._roll))
        self._leg_ori_abs[:, 2] = self._leg_ori_loc[:, 2]
        self._leg_ori_abs[:, 1] = self.OFFSET_ROLL*np.cos(self.to_rads(self._roll))

    # Pitches the body. Body absolute and relative coordinates change.
    def body_pitch(self, pitch):
        self._pitch = pitch
        self._leg_ori_loc[:, 2] = self._body_z + self.OFFSET_PITCH*np.sin(self.to_rads(self._pitch))
        self._leg_ori_abs[:, 2] = self._leg_ori_loc[:, 2]
        self._leg_ori_abs[:, 0] = self.OFFSET_PITCH*np.cos(self.to_rads(self._pitch))

    # Rotates the body. Body absolute and relative coordinates change, but leg does not.
    def body_rotate(self, theta):
        distances = self.pythagoras( self._leg_ori_abs[:, 0:2] )
        angles = self.to_degs(np.arctan2( self._leg_ori_abs[:, 1], self._leg_ori_abs[:, 0]))+theta

        self._leg_ori_abs[:, 0] = distances * np.cos( self.to_rads( angles ) )
        self._leg_ori_abs[:, 1] = distances * np.sin( self.to_rads( angles ) )

    def body_translate_x(self, x):
        self._leg_ori_abs[:, 0] += x
        self._leg_ori_loc[:, 0] += x

    def body_translate_y(self, y):
        self._leg_ori_abs[:, 1] += y
        self._leg_ori_loc[:, 1] += y

    def body_translate_z(self, z):
        self._body_z = z
        self.body_pitch(self._pitch) # Updates z-height, then for the other stuff.
        self.body_roll(self._roll)

    # Recenters origin coordinates back to (0,0) - after successfully moving?
    def body_recenter(self):
        self._leg_ori_abs[:,0:2] = 0.0
        self._leg_ori_loc[:,0] = self.OFFSET_PITCH
        self._leg_ori_loc[:,1] = self.OFFSET_ROLL
        self.body_pitch(self._pitch) # Updates z-height, then for the other stuff.
        self.body_roll(self._roll)
    
    def get_leg_end_loc(self):
        return self._leg_end_loc
    def get_leg_end_abs(self):
        return self._leg_end_abs
    def get_leg_ori_loc(self):
        return self._leg_ori_loc
    def get_leg_ori_abs(self):
        return self._leg_ori_abs
    def get_leg_angle(self):
        return self._leg_angle
    def get_body_z(self):
        return self._body_z

    def print_state(self): # Sanity check
        np.set_printoptions(precision=3, suppress=True) # print prettier
        print("Local leg endpoints:\n", self._leg_end_loc)
        print("Abs leg endpoints:\n", self._leg_end_abs)
        print("Local leg origin:\n", self._leg_ori_loc)
        print("Abs leg origin:\n", self._leg_ori_abs)
        print("Leg Angles:\n", self._leg_angle)
        print("Body Z-height:", self._body_z)
        print("Body roll:", self._roll)
        print("Body pitch:", self._pitch)

# Class for legs and joints
class leg_joint:
    # "Public" variables
    curr_angle = 90
    _servo_num = 0
    _offset = 0 # can be tuned for non-idealites in hardware setup
    _limit = 30 # Limit to motion, servo cannot pass this value
    _start_angle = curr_angle
    _angle_max = curr_angle + _offset + _limit
    _angle_min = curr_angle + _offset - _limit
    
    # _servo_driver = None # empty variable for now

    def __init__(self, servo_num, start_angle=90, limit=30, offset=0):
        # Initialises servo values. Here, start angle refers to the neutral position of the servo.
        self._servo_num = servo_num
        self._offset = offset
        self._limit = limit
        self._start_angle = start_angle + self._offset
        self._angle_max = self._start_angle + self._limit
        self._angle_min = self._start_angle - self._limit

        # self._servo_driver = kit.servo[servo_num]

    def writeLimit(self, limit):
        # Updates the limits of the object.
        self._limit = limit
        self._angle_max = self._start_angle + self._offset + self._limit
        self._angle_min = self._start_angle + self._offset - self._limit
        
        return self._angle_max, self._angle_min

    def writeAngle(self, angle):
        try_angle = angle + self._offset
        if try_angle > self._angle_max:
            self.curr_angle = self._angle_max
            warnings.warn("%s: Exceeded +ve limit" %self.__class__.__name__)
        elif try_angle < self._angle_min:
            self.curr_angle = self._angle_min
            warnings.warn("%s: Exceeded -ve limit" %self.__class__.__name__)
        else:
            self.curr_angle = try_angle

        # self._servo_driver.angle = self.curr_angle # Write servo angle here.

        return self.curr_angle

    # Prints info to debug stuff with on to console
    def debug_print(self):
        print("For servo", self.__class__.__name__)
        print("Current Angle:", self.curr_angle, "Offset:", self._offset)
        print("+ve limit:", self._angle_max, "-ve limit:", self._angle_min)
    
    # returns a list of important info
    def debug_return(self):
        info = [self.curr_angle, self._offset, self._angle_max, self._angle_min]
        return info

class hex_leg:
    # Similar to body class, use getter-setter fns
    # body class will interact with several leg classes. The leg classes perform IK calculations and handle lower-level actions
    _leg_angles = np.tile(90.0, 3)
    _leg_end = np.zeros(3) # local coordinates for the leg tip/end 
    _leg_ori = np.zeros(3) # local coordinates for leg origin

    _joints = None

    COXA_LEN = 28.75
    FEMUR_LEN = 40.0
    TIBIA_LEN = 68.825

    def __init__(self, leg_end, leg_ori_z, leg_nums, 
                limits=np.array((30.0, 30.0, 30.0)), offsets=np.array((0.0, 0.0, 0.0))):

        self._leg_ori[2] = leg_ori_z
        self._leg_end = leg_end

        coxa_joint = leg_joint(servo_num=leg_nums[0], limit=limits[0], offset=offsets[0])
        femur_joint = leg_joint(servo_num=leg_nums[1], limit=limits[1], offset=offsets[1])
        tibia_joint = leg_joint(servo_num=leg_nums[2], limit=limits[2], offset=offsets[2])
        self._joints = (coxa_joint, femur_joint, tibia_joint)
    
    # Leg tip moves, leg origin does not
    def swing(self, leg_end):
        self._leg_end = leg_end

        coxa_angle_ik = np.arctan2(leg_end[0], leg_end[1]) # 'gamma' in notes

        coxa_len_ik = self.COXA_LEN * np.cos( coxa_angle_ik ) # Takes side view of this thing.
        femur_len_ik = self.FEMUR_LEN * np.cos( coxa_angle_ik )
        tibia_len_ik = self.TIBIA_LEN * np.cos( coxa_angle_ik )

        y_offset_ik = leg_end[1] - coxa_len_ik
        z_offset_ik = self.TIBIA_LEN - leg_end[2]
        l_len = np.sqrt( np.power(z_offset_ik,2) + np.power(y_offset_ik,2) )

        print("z_offset_ik: %0.4f | y_offset_ik: %0.4f | l_len: %0.4f" %(z_offset_ik, y_offset_ik, l_len) )

        femur_angle_ik1 = np.arccos( z_offset_ik / l_len )
        femur_angle_ik2 = np.arccos( (femur_len_ik**2 + l_len**2 - tibia_len_ik**2) / (2*femur_len_ik*l_len) )
        femur_angle_ik = femur_angle_ik1 + femur_angle_ik2
        tibia_angle_ik = np.arccos( (femur_len_ik**2 - l_len**2 + tibia_len_ik**2) / (2*femur_len_ik*tibia_len_ik) )

        self._leg_angles = np.array( (to_degs(coxa_angle_ik)+90, to_degs(femur_angle_ik), to_degs(tibia_angle_ik)) )

        return self._leg_angles

    # Leg origin moves. Update leg end; after all, leg end is RELATIVE to leg origin (always 0,0,Z)
    def stance(self, leg_ori):
        diff = leg_ori - self._leg_ori
        self._leg_end += diff

        return self.swing(self._leg_end)

    # Sets leg angles arbitrarily and use FK to update leg end coordinates
    # assume swing: that leg origin z-height is const (modify tip z-height)
    # else stance: that leg tip z-height is const (modify origin z-height)
    def set_leg_angles(self, angles, assume_swing=True):
        alpha = angles[1]
        beta = angles[2]

        femur_yx = self.FEMUR_LEN*np.cos(to_rads(alpha-90))
        tibia_yx = self.TIBIA_LEN*np.sin(to_rads(alpha+beta-180)) # respective lengths viewed from top (y-x plane)

        femur_yz = self.FEMUR_LEN*np.sin(to_rads(alpha-90))
        tibia_yz = self.TIBIA_LEN*np.cos(to_rads(alpha+beta-180)) # respective lengths viewed from side (y-z plane)

        tip_x = (self.COXA_LEN + femur_yx + tibia_yx) * np.sin(to_rads(angles[0]-90))
        tip_y = (self.COXA_LEN + femur_yx + tibia_yx) * np.cos(to_rads(angles[0]-90))

        if assume_swing:
            tip_z = self._leg_ori[2] + femur_yz + tibia_yz
            self._leg_end[2] = tip_z
        else:
            tip_z = self._leg_end[2] - femur_yz - tibia_yz
            self._leg_ori[2] = tip_z

        self._leg_end[0:2] = (tip_x, tip_y)

    def get_leg_ori(self):
        return self._leg_ori
    def get_leg_end(self):
        return self._leg_end
    def get_leg_angles(self):
        return self._leg_angles