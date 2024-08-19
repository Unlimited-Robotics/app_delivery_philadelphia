from raya.enumerations import FLEET_UPDATE_STATUS

FLEET_CALL_MESSAGE = {
    'message': 'Hello i`m Gary, please pick up the package.'
}

# FLEET STATUS
FLEET_STATUS_GOING_TO_CART_POINT  = 'On my way to cart point.'
FLEET_STATUS_ATTACHED_TO_CART = 'Gary just attached to the cart'
FLEET_STATUS_NAVIGATING_TO_ELEV = 'On my way to elevator to floor [floor]'
FLEET_STATUS_NAVIGATING_TO_CARE_UNIT = 'On my way to care unit [care_unit]'
FLEET_STATUS_ARRIVED_TO_CARE_UNIT = 'Gary arrived to [care_unit]'

FLEET_PARKING_CART = 'Leaving the delivery cart in the warehouse, Waiting for package confirmation.'
FLEET_UI_RESPONSE = 'The delivery status was [delivery_status], signed by: [user_name]'

FLEET_CART_RELEASED = 'Gary detached from the cart'
FLEET_ON_MY_WAY_TO_HOME = 'On my way to the home'
FLEET_APP_FINISH = 'Application finished'

FLEET_WAIT_FOR_PACKAGE_CONFIRMATION = 'Waiting for package confirmation.'
FLEET_PACKAGE_CONFIRM_USING_UI = 'The package was confirm using the options using the ui oprtions.'

FLEET_GOING_TO_WAREHOUSE = 'Gary is returning to the warehouse'
FLEET_ROBOT_ATTACHING_TO_CART = 'The robot is attaching to the cart.'
FLEET_ROBOT_DETACHING_TO_CART = 'The robot is detaching to the cart.'
