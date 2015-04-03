#!/bin/sh
# Note: You need some env vars to make this work.
aws s3 sync --acl=public-read --delete --storage-class=REDUCED_REDUNDANCY public/ s3://anemone.dodgson.org
curl -d "" http://steps.dodgson.org/clear
