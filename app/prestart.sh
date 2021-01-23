#!/bin/bash
set -e

echo "Let the DB start.."
sleep 2;

echo "Run migrations"
flask db upgrade

if [ -f "first.run" ]; then
        echo "Fill db with initial data"
        python fill_db.py
        rm -f first.run
fi
