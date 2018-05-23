# StravaRouteAppender
Auto fetches new routes from your Strava profile and appends them to an existing map displaying your previous routes in GeoJSON format.

Strava data fetching uses a slightly modified version of https://github.com/ryanbaumann/Strava-Stream-to-CSV 

GeoJSON simplification is done using the simplify.py library from https://github.com/omarestrella/simplify.py


# Usage

To use, first create a Strava app in your Strava dashboard. Grab your client ID, your secret key, and your access token and put them in a file named `secret.txt`, with a comma separating each one. 

You will need to modify the os.chdir calls at the beginning of each script - this is because `cron` has a different working directory than when I was testing, so it would place files in the wrong folders. There may be other path specific issues in the scripts that you'll need to fix.


