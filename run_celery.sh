#!/bin/sh

sleep 10

celery -A crypto_api worker -l info