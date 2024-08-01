#!/bin/bash
file_list=$(find "/traffic" -maxdepth 1 -type f | paste -sd, -)