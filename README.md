visualizaiton
========================

A template for visualizing realtime data on Google Map
To get this running you need to have a few things:


* Install memcache
http://mac-dev-env.patrickbougie.com/memcached/
* Install venv
* Better to use Firefox for the current version
* Install required python packages
  **>cd repo/root/directory/
  **>source your/directory/venv/bin/activate
  **>pip install -r requirements.txt  



First, start loading historical data by >python -m service.hourly_in_a_week.
Then start the app by >python -m app.
Then connect your browser to http://localhost:5000/static/hourlyinaweek_yield.html and wait for the visualization to appear!

High level architect:
Client (browser) <-- wsgi <-- flask <-- Python functions/memcache

Caveat:
Since the template is for data stream, the handling of client disconnection (browser closed before sockets are properly turned down) is not ready. Mostly likely you may see error: [Errno 32] Broken pipe on the server log. In the next iteration, I will improve it.
