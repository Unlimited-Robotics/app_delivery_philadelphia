## PYRAYA SKILLS
POSIBLES_IDS_CART = ['4']

SETUP_ARG_ATTACH_SKILL = {
}

EXECUTION_ARG_ATTACH_SKILL = {
    'tag_size': 0.12,
    'target_tags': POSIBLES_IDS_CART,
    'reverse': True,
    'target_distance': 0.55,
}

SETUP_ARG_DETACH_SKILL = {
    
}

EXECUTION_ARG_DETACH_SKILL = {
    
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
