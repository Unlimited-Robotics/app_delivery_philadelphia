# Delivery App - Philadelphia

Optimize hospital logistics with our delivery app. Automate item transportation, relieving staff burden. Ensure timely, essential deliveries for patient care.

## Preparing the Robot

* The robot is calibrated.
* Ensure you are using version `integration_20240529` or newer.

## Preparing the Environment

1. Map the environment using the usual methods.

2. Set the following coordinates. We recommend using the `nav_to_click` example to obtain the coordinates, then copy and paste the values into the `src/static/navigation.py` file:

    * `NAV_CART_POINT`: Where the robot will pick up the cart. This location should have the cart tags visible from this position.

    * `NAV_WAREHOUSE_ENTRANCE`: Just in front of the door, OUTSIDE the warehouse, and facing the door.

    * `NAV_WAREHOUSE_EXIT`: Just in front of the door, INSIDE the warehouse, and facing the door.

    * `NAV_HOME_POSITION_NAME`: Location name saved in the map where the robot will start and finish the app. This point should be close to the docking station.

![alt text](/doc/img/nav_points.png)

3. Create a location and call it `Home`. This value must match `NAV_HOME_POSITION_NAME`. Use the example app `nav_save_current_location` in the latest version of the `integration` branch of the pyRa-Ya examples repository.

    You can execute the app like this:

    ```
    rayasdk run nav_save_current_location/ -m <map_name> -l <location_name>
    ```

4. Set the zone and call it `warehouse`. Use the example app `nav_save_zone` in the latest version of the `integration` branch of the pyRa-Ya examples repository.

    You can execute the app like this:

    ```
    rayasdk run nav_save_zone/ -m <map_name> -z <zone_name>
    ```

    You will see the map, so just click to create a polygon that describes the zone:

    ![alt text](/doc/img/save_zone.png)

    After that, click the X to close the window and wait for the zone to be saved (this can take some time).

    If you need to delete a zone, open the `map.yaml` file inside the map folder and delete it from the list of zones.

## Set Constants

* In the file `src/static/navigation.py`:

    * `NAV_WAREHOUSE_MAP_NAME`: Name of the map.

    * `NAV_CART_POINT`, `NAV_WAREHOUSE_ENTRANCE`, and `NAV_WAREHOUSE_EXIT`: Navigation points.

    * `NAV_WAREHOUSE_ZONE_NAME`: Name of the warehouse zone (`warehouse` by default).

* In the file `src/static/skills.py`:
    
    * `SETUP_ARG_ATTACH_SKILL`: Setup arguments (dict) for the attach-to-cart skill.

    * `EXECUTION_ARG_ATTACH_SKILL`: Execution arguments (dict) for the attach-to-cart skill.

    * `SETUP_ARG_DETACH_SKILL`: Setup arguments (dict) for the detach-from-cart skill.

    * `EXECUTION_ARG_DETACH_SKILL`: Execution arguments (dict) for the detach-from-cart skill.

## Execute App from Terminal

Before executing the app, ensure to run the rayasdk command to download the necessary skills:

```
rayasdk skills install_deps --no-delete
```

Then run:

```
rayasdk run \
    --location1 \"[260, 609, -78.39]\" \
    --location2 \"[381, 655, 1.57]\" 
```

The `--location1` are the coordinates for delivery point 1.

The `--location2` are the coordinates for delivery point 2.

(Maximum 2 points).

## Execute App from Fleet

Synchronize the app, create the locations using the location option in the fleet, add them as parameters to the app task, and execute it.

![alt text](/doc/img/fleet_arguments.png)
