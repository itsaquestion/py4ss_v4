#!/bin/sh
cp plotly.js _book/book_parts/case_study
rsync -av -e ssh _book/ lee@hk:/var/www/py4ss.net/python 

# # turn off cache = development_mode on 
# curl -X PATCH "https://api.cloudflare.com/client/v4/zones/7e61015d60a07937b261e3314862c7a4/settings/development_mode" \
# -H "Authorization: Bearer $cf_cache_key" \
# -H "Content-Type: application/json" \
# --data '{"value":"on"}' -s -o /dev/null &

# wait