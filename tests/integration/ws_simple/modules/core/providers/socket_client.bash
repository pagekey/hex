#!/bin/bash

echo "hello world" | socat - UNIX-CONNECT:./user_input.sock
