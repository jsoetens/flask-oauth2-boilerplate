#!/usr/bin/env bash

# Flask
export MYAPP_CONFIG='testing'
export FLASK_APP=`pwd`/autoapp.py
export FLASK_DEBUG=True
# Please generate your own random keys (you can use os.urandom(24))
export SECRET_KEY='\xa6TQ5\xc9\xf942\x9cx\x9b\xed\xa4\xc7\x95\xcc\xfd\xb8Q\xa1\x80\x99Z%'
# Separate token for CSRF protection (by default it uses secret key)
export WTF_CSRF_SECRET_KEY='\xc9\xcc\x91{\xd9\x9a\x18\x92\xaa\xb4\x9e\x80\x07\x13\x92-\x1ciH\x86\xecz:['

echo 'Starting myapp'

# Python Virtual Environment using Pipenv
pipenv run flask test_with_coverage

# Python Virtual Environment using virtualenv
# source venv/bin/activate
