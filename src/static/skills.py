## PYRAYA SKILLS
POSIBLES_IDS_CART = ['20', '13']

SETUP_ARG_ATTACH_SKILL = {
}

EXECUTION_ARG_ATTACH_SKILL = {
    'leds_interactions': False,
    'reverse_beeping_alert': False,
}

# Old ones (when the attach and approach were in the same skill)
# EXECUTION_ARG_ATTACH_SKILL = {
#     'tag_size': 0.12,
#     'target_tags': POSIBLES_IDS_CART,
#     'reverse': True,
#     'target_distance': 0.55,
# }

EXECUTION_ARG_APPROACH_SKILL = {
    'skill':'approach_to_tag',
    'family':'36h11',
    'tag_size':0.12,
    'sources':['back'],
    'target_tags':POSIBLES_IDS_CART,
    'target_distance':0.40,
    'wait_target_time':4.0,
    'reverse':True,
    'max_x_error':           0.02, 
    'max_y_error':           0.02,
    'low_angular_velocity':  0.10,
    'low_linear_velocity':   0.20,
    'high_linear_velocity':  0.30,
    'min_approach_distance': 0.50,
    'approach_to_center':    False,
}

SETUP_ARG_DETACH_SKILL = {
    
}

EXECUTION_ARG_DETACH_SKILL = {
    'move_fowards': True,
}

## GARY SKILLS
SKILL_EXIT_ELEVATOR = 'exit_elevator'
ARGS_EXIT_ELEVATOR = {
    'skill': SKILL_EXIT_ELEVATOR,
    'target_floor': '', # Set in the FSM
    'move_distance': 3.6,
    'tag_source': 'front_ip',
    'tag_family': '36h11',
    'tag_size': 0.14
}
