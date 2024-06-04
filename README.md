# Delivery App - Philadelphia

Optimize hospital logistics with our delivery app. 
Automate item transportation, relieving staff burden. 
Timely, essential deliveries for patient care.

## Preparing the robot

* The robot is calibrated.
* You're using the version `integration_20240529` or newer.

## Preparing the environment

1. Map the environment. Using the usual methods to map.

2. Set the following coordinates:

    * `NAV_CART_POINT`: Where the robot is going to pick the cart.

    * `NAV_WAREHOUSE_ENTRANCE`: Just in front of the door, OUTSIDE the warehouse.

    * `NAV_WAREHOUSE_EXIT`: Just in front of the door, INSIDE the warehouse.

![alt text](/doc/img/nav_points.png)

3. Set the zone and call it `warehouse`. Use the example app `nav_save_zone` in the LAST version of `integration` of the pyRa-Ya examples repository.

    You can execute the app like:

    ```
    rayasdk run nav_save_zone/ -m <map_name> -z <zone_name>
    ```

    You're going to see the map, so just click to create a polygon that describes the zone:

    ![alt text](/doc/img/save_zone.png)

    After that just click the X to close the window and wait for the zone to get saved (it can take some time).

    If you need to delete a zone, open the `map.yaml` file inside the map folder and delete it from the list of zones.

## Set Constants

* File `src/static/navigation.py`:

    * `NAV_WAREHOUSE_MAP_NAME`: Name of the map.

    * `NAV_CART_POINT`, `NAV_WAREHOUSE_ENTRANCE` and `NAV_WAREHOUSE_EXIT`: Navigation points.

    * `NAV_WAREHOUSE_ZONE_NAME`: Name of the wareouse zone (`warehouse` by default).

## Execute app from terminal

Just run:

```
rayasdk run \
    --location1 \"[260, 609, -78.39]\" \
    --location2 \"[381, 655, 1.57]\" 
```

The `--floor1` and `--location1` are the map name and coordinates for delivery point 1.

The `--floor2` and `--location2` are the map name and coordinates for delivery point 2.

(Maximum 2 points).

## Execute app from fleet

Just set the points and add them as parameters to the app task.
