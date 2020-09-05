import numpy as np
import matplotlib.pyplot as plt

# Define constants
# Define leg parameters
coxa_len = 28.75
tibia_len = 68.825
femur_len = 40
z_offset = tibia_len

# Define body parameters (for rotational IK)
X0_LEN = 45.768
Y0_LEN = 26.424
Y1_LEN = 52.848
R1_ORIGIN = np.array( (X0_LEN, Y0_LEN, z_offset) )
R2_ORIGIN = np.array( (0.0, Y1_LEN, z_offset) )
R3_ORIGIN = np.array( (-X0_LEN, Y0_LEN, z_offset) )
L1_ORIGIN = np.array( (X0_LEN, -Y0_LEN, z_offset) )
L2_ORIGIN = np.array( (0.0, -Y1_LEN, z_offset) )
L3_ORIGIN = np.array( (-X0_LEN, -Y0_LEN, z_offset) )
leg_origins = np.array( (R1_ORIGIN, R2_ORIGIN, R3_ORIGIN, L3_ORIGIN, L2_ORIGIN, L1_ORIGIN) )

def to_rads(num):
    return num*np.pi/180

def to_degs(num):
    return num/np.pi*180

def pythagoras(nums):
    return np.sqrt(np.sum(np.power(nums, 2), axis=-1))

# Forward kinematics check - make this into a function
# Forward kinematics check - make this into a function
def plot_legs(angle):
    leg_base = np.array([0, 0, z_offset], dtype='float32') # xyz
    coxa_end = np.array([0, 0, z_offset], dtype='float32')
    femur_end = np.array([0, 0, 0], dtype='float32')
    tibia_end = np.array([0, 0, 0], dtype='float32')

    # Input desired angles here
    print("\nDesired angles:", ["%0.4f" %i for i in angle])
    angles = angle
    coxa_angle = angles[0] - 90
    femur_angle = angles[1] - 90
    tibia_angle = angles[2]

    theta = tibia_angle + femur_angle - 90

    femur_vert = femur_len * np.cos( to_rads(femur_angle) )
    tibia_vert = tibia_len * np.sin( to_rads(theta) )

    femur_hor = femur_len * np.cos( to_rads(coxa_angle) )
    tibia_hor = tibia_len * np.cos( to_rads(coxa_angle) )

    # # Debug parameters
    # print(z_offset)
    # # Debug desired angles
    # print("%0.4f, %0.4f, %0.4f, %0.4f" %(coxa_angle, femur_angle, tibia_angle, theta))
    # # debug tibia params
    # print("%0.4f, %0.4f" %(femur_vert, tibia_vert))

    # calc coxa end-points
    coxa_end[0] = coxa_len * np.sin( to_rads(coxa_angle) )
    coxa_end[1] = coxa_len * np.cos( to_rads(coxa_angle) )

    # calc femur end-points
    femur_end[0] = coxa_end[0] + femur_vert * np.sin( to_rads(coxa_angle) )
    femur_end[1] = coxa_end[1] + femur_vert * np.cos( to_rads(coxa_angle) )
    femur_end[2] = coxa_end[2] + femur_hor * np.sin( to_rads(femur_angle) )

    # calc tibia end-points
    tibia_end[0] = femur_end[0] + tibia_vert * np.sin( to_rads(coxa_angle) )
    tibia_end[1] = femur_end[1] + tibia_vert * np.cos( to_rads(coxa_angle) )
    tibia_end[2] = femur_end[2] + tibia_hor * np.cos( to_rads( theta-180 ) )

    # sanity check: if all legs are the same length
    print("Coxa length:", pythagoras(coxa_end-leg_base))
    print("Femur length:", pythagoras(femur_end-coxa_end))
    print("Tibia length:", pythagoras(tibia_end-femur_end))

    leg_base_annotate = ["%0.4f" %i for i in leg_base]
    coxa_end_annotate = ["%0.4f" %i for i in coxa_end]
    femur_end_annotate = ["%0.4f" %i for i in femur_end]
    tibia_end_annotate = ["%0.4f" %i for i in tibia_end]

    print("Leg_base:", leg_base_annotate)
    print("coxa_end:", coxa_end_annotate)
    print("femur_end:", femur_end_annotate)
    print("tibia_end:", tibia_end_annotate)
    print("theta: %0.4f" %theta)

    coords_x = (leg_base[0], coxa_end[0], femur_end[0], tibia_end[0])
    coords_y = (leg_base[1], coxa_end[1], femur_end[1], tibia_end[1])
    coords_z = (leg_base[2], coxa_end[2], femur_end[2], tibia_end[2])

    
    leg_annotations = (leg_base_annotate, coxa_end_annotate, femur_end_annotate, tibia_end_annotate)

    # TODO print end coords onto visualization;
    # Plot both views
    fig, axs = plt.subplots(1,2)
    fig.suptitle("Leg IK simulation")
    axs[0].set_title("Top View")
    axs[0].set_xlabel("y")
    axs[0].set_xlabel("x")
    axs[0].plot(coords_y, coords_x, 'x-', linewidth=5)
    # axs[0].plot( (leg_base[1], coxa_end[1]), (leg_base[0], coxa_end[0]), 'x-', linewidth=5, label="Coxa")
    # axs[0].plot( (coxa_end[1], femur_end[1]), (coxa_end[0], femur_end[0]), 'x-', linewidth=5, label="Femur")
    # axs[0].plot( (femur_end[1], tibia_end[1]), (femur_end[0], tibia_end[0]), 'x-', linewidth=5, label="Tibia")
    for i, txt in enumerate(leg_annotations):
        axs[0].annotate(txt, (coords_y[i], coords_x[i]))
    axs[0].set_ylim(-45, 45)
    axs[0].set_xlim(0, 90)
    axs[0].grid()

    axs[1].set_title("Side view")
    axs[1].set_xlabel("y")  
    axs[1].set_xlabel("x")
    axs[1].plot(coords_y, coords_z, 'x-', linewidth=5)
    # axs[1].plot( (leg_base[1], coxa_end[1]), (leg_base[2], coxa_end[2]), 'x-', linewidth=5, label="Coxa")
    # axs[1].plot( (coxa_end[1], femur_end[1]), (coxa_end[2], femur_end[2]), 'x-', linewidth=5, label="Femur")
    # axs[1].plot( (femur_end[1], tibia_end[1]), (femur_end[2], tibia_end[2]), 'x-', linewidth=5, label="Tibia")
    for i, txt in enumerate(leg_annotations):
        axs[1].annotate(txt, (coords_y[i], coords_z[i]))
    axs[1].set_ylim(-30, 90)
    axs[1].set_xlim(0, 120)
    axs[1].grid()

    plt.tight_layout()
    plt.show()

    return [leg_base, coxa_end, femur_end, tibia_end, theta]

def plot_body(body_coords, origin_coords=leg_origins):

    coords_x = np.append( body_coords[:, 0], body_coords[0,0] )
    coords_y = np.append( body_coords[:, 1], body_coords[0,1] )
    coords_z = np.append( body_coords[:, 2], body_coords[0,2] )

    coords_x_origin = np.append( origin_coords[:, 0], origin_coords[0,0] )
    coords_y_origin = np.append( origin_coords[:, 1], origin_coords[0,1] )
    coords_z_origin = np.append( origin_coords[:, 2], origin_coords[0,2] )

    leg_labels = ['R1', 'R2', 'R3', 'L3', 'L2', 'L1', '' ]
    leg_labels_o = ['o_R1', 'o_R2', 'o_R3', 'o_L3', 'o_L2', 'o_L1', '' ]

    fig, axs = plt.subplots(1,3, figsize=(15,5))
    fig.suptitle("Body IK simulation")

    axs[0].set_title("Front view")
    axs[0].set_xlabel("y")  
    axs[0].set_ylabel("z")
    axs[0].plot(coords_y_origin, coords_z_origin, 'x-', linewidth=5)
    axs[0].plot(coords_y, coords_z, 'x-', linewidth=5)
    for i, txt in enumerate(leg_labels):
        axs[0].annotate(txt, (coords_y[i], coords_z[i]))
    for i, txt in enumerate(leg_labels_o):
        axs[0].annotate(txt, (coords_y_origin[i], coords_z_origin[i]+5))
    axs[0].set_xlim(-60, 60)
    axs[0].set_ylim(0, 120)
    axs[0].grid()

    axs[1].set_title("Side View")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("z")
    axs[1].plot(coords_x_origin, coords_z_origin, 'x-', linewidth=5)
    axs[1].plot(coords_x, coords_z, 'x-', linewidth=5)
    for i, txt in enumerate(leg_labels):
        axs[1].annotate(txt, (coords_x[i], coords_z[i]))
    for i, txt in enumerate(leg_labels_o):
        axs[1].annotate(txt, (coords_x_origin[i], coords_z_origin[i]+5))
    axs[1].set_xlim(-60, 60)
    axs[1].set_ylim(0, 120)
    axs[1].grid()

    axs[2].set_title("Top View")
    axs[2].set_ylabel("x")
    axs[2].set_xlabel("y")
    axs[2].plot(coords_y_origin, coords_x_origin, 'x-', linewidth=5)
    axs[2].plot(coords_y, coords_x, 'x-', linewidth=5)
    for i, txt in enumerate(leg_labels):
        axs[2].annotate(txt, (coords_y[i], coords_x[i]))
    for i, txt in enumerate(leg_labels_o):
        axs[2].annotate(txt, (coords_y_origin[i], coords_x_origin[i]-2))
    axs[2].set_xlim(-60, 60)
    axs[2].set_ylim(-60, 60)
    axs[2].grid()

    plt.tight_layout()
    plt.show()

def plot_everything(leg_tips, leg_origins):
    # sanity check
    if leg_tips.shape != (6,3) or leg_origins.shape != (6,3):
        print("Check dimensions please. Leg tips:", leg_tips.shape, "Leg origins:", leg_origins.shape)
        return 0

    legs = np.empty((6, 3, 2))
    legs[:,:,0] = leg_tips
    legs[:,:,1] = leg_origins

    coords_x_body = np.append( leg_origins[:, 0], leg_origins[0,0] )
    coords_y_body = np.append( leg_origins[:, 1], leg_origins[0,1] )
    # coords_z_body = np.append( leg_origins[:, 2], leg_origins[0,2] )

    leg_labels = ['R1', 'R2', 'R3', 'L3', 'L2', 'L1', '' ]

    plt.figure(figsize=(9,8))
    plt.title("Whole Hexapod IK simulation | Top View")
    plt.ylabel("x")
    plt.xlabel("y")
    plt.plot(coords_y_body, coords_x_body, linewidth=5, label="body")
    for i, txt in enumerate(leg_labels):
        plt.annotate(txt, (coords_y_body[i], coords_x_body[i]))
    for x in range(legs.shape[0]):
        plt.plot(legs[x,1,:], legs[x,0,:], linewidth=5, label="leg %d" %(x+1))
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()
    