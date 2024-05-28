# app_delivery_philadelphia
Optimize hospital logistics with our delivery app. Automate item transportation, relieving staff burden. Timely, essential deliveries for patient care.


## what the fleet sends
python3 __main__.py --floor1 "minigary.101" --floor2 "minigary.101" --location1 "[381, 655, 1.57, 'point1']" --location2 "[260, 609, -0.98, 'point2']" --target_x "92" --target_y "123" --target_angle "191" --target_name "room806" --task_id "ccc35b24-059e-48ce-ae8f-6d86013d57dc"

## run without fleet
rayasdk run --floor1 "minigary.101" --floor2 "minigary.101" --location1 "[381, 655, 1.57, 'point1']" --location2 "[260, 609, 0.98, 'point2']"
