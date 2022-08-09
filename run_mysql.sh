#!/bin/bash

docker run --name some-mysql --net=host -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7.39 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci