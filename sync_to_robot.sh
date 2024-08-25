#!/bin/bash

rsync -av --delete --exclude='__pycache__/' --exclude='.git' ./ $1:/opt/raya_os/data/apps/delivery_cart
