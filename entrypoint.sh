#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python main.py
        ;;
    test)
        echo "Test"
        exec pytest
        ;;
    start)
        echo "Running Start"
        exec gunicorn -c gunicorn.py arcgis_proxy.app:app
        ;;
    *)
        exec "$@"
esac
