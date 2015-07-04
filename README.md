# pyccuweather [![Coverage Status](https://coveralls.io/repos/chrisvoncsefalvay/pyccuweather/badge.svg)](https://coveralls.io/r/chrisvoncsefalvay/pyccuweather) [![Build Status](https://travis-ci.org/chrisvoncsefalvay/pyccuweather.svg?branch=master)](https://travis-ci.org/chrisvoncsefalvay/pyccuweather)

The Python wrapper to Accuweather services

# Install

Install via pip:

    pip install pyccuweather
    

# Usage

## Authentication

When you create a `Connection` object, Pyccuweather will look for an Accuweather API key in a particular sequence. 
First, it will look for an explicitly provided API key. If none is provided, it will look for anenvironment variable 
called `ACCUWEATHER_APIKEY`. 


### Env authentication

You can set your system up for authentication by saving the API key in your system's environment variables. Open a 
terminal and enter

    export ACCUWEATHER_APIKEY=<your API key>

substituting the example string with your actual API key. Pyccuweather will use this API key if it is not provided with
an explicit API key.

### Explicit authentication

When creating a `Connection` object, you can provide an API key:

    from pyccuweather.connector import Connection
    conn = Connection(API_KEY="<your API key>")
    
This will be used preferentially to the environment key.

## Location resolution

[To be written]

## Querying

[To be written]

## Roadmap

[To be written]

# License

Pyccuweather is licenced under the [MIT License](https://github.com/chrisvoncsefalvay/pyccuweather/blob/master/LICENSE.txt).

# Credits

Pyccuweather was developed by [Chris von Csefalvay](http://www.chrisvoncsefalvay.com) at [RB plc](http://www.rb.com) 
with the generous support of [Accuweather](http://www.accuweather.com).
