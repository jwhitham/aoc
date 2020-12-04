#!/bin/bash

rm -f tmp.db
sqlite3 tmp.db < part1.sql
rm -f tmp.db
sqlite3 tmp.db < part2.sql

