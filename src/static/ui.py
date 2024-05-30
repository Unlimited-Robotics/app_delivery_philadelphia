from raya.enumerations import UI_ANIMATION_TYPE

# SCREENS

UI_SCREEN_LOCALIZING = {
        'title':'Starting Application', 
        'subtitle':'Localizing 🕵',
    }

UI_SCREEN_NAV_TO_WAREHOUSE = {
        'title':'Navigating', 
        'subtitle':'Going to warehouse',
    }

UI_SCREEN_ENTERING_TO_WAREHOUSE = {
        'title':'Navigating', 
        'subtitle':'Entering warehouse',
    }

UI_SCREEN_WAIT_FOR_PACKAGE_LOAD = {
        'title':'Waiting for package', 
        'subtitle':'Please load the package and press the chest button to continue',
    }

UI_SCREEN_WAIT_FOR_CART_UNLOAD = {
        'title':'Waiting for Cart Unload', 
        'subtitle':'Please unload the cart and press the chest button to continue',
    }

UI_SCREEN_WAIT_FOR_DOOR_OPEN = {
        'title':'Waiting for door to open', 
        'subtitle':'Please open the door and press the chest button to continue, and step aside',
    }

UI_SCREEN_NAV_TO_WAREHOUSE_EXIT = {
        'title':'Navigating', 
        'subtitle':'Navigating to warehouse exit',
    }

UI_SCREEN_LEAVE_WAREHOUSE = {
        'title':'Navigating', 
        'subtitle':'Leaving warehouse',
    }

UI_SCREEN_NAV_TO_WAREHOUSE_RETURN = {
        'title':'Navigating', 
        'subtitle':'Going back to warehouse',
    }

UI_SCREEN_DELIVERING_ARRIVE = {
        'title':'Delivering', 
        'subtitle':'Delivering complete, please confirm pressing the chest button',
    }

UI_SCREEN_DELIVERING_SUCCESS = {
        'title':'Delivering Success ✅', 
        'subtitle':'The package was delivered successfully',
    }

UI_SCREEN_ALL_PACKAGES_DONE = {
        'title':'Delivering finished', 
        'subtitle':'The app went through all the packages and parked the cart.',
    }

UI_SCREEN_RELEASE_CART = {
        'title':'Releasing Cart', 
        'subtitle':'Please wait while the cart is being released.',
    }

UI_PACKAGE_NOT_DELIVERED = {
        'title':'Package not delivered 🚫', 
        'subtitle':'No confirmation received',
    }

UI_SCREEN_REQUEST_FOR_HELP = {
        'title':'Request for Help',
        'subtitle':'I\'m stuck, contacting the fleet...',
    }

UI_SCREEN_WAIT_FOR_HELP_SELECTOR = {
        'title':'I\'m stuck, please help me, and choose an option',
        'back_button_text': '',
        'max_items_shown': 2,
        'data': [
                {'id': 1, 'name': 'Abort App 🚫'}, 
                {'id': 2, 'name': 'Continue 🚶‍♂️'},
            ]
    }

UI_SCREEN_FAILED = {
        'title':'Failed',
    }
