#!/bin/bash
file_list=$(find "$(realpath /traffic)" -maxdepth 1 -type f | paste -sd, -)