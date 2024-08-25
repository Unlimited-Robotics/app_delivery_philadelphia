#!/bin/bash

rsync -av --delete --exclude='__pycache__/' ./ $1:/opt/raya_os/data/apps/delivery_cart
