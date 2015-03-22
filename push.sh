#!/usr/bin/sh
# presuming keys given through env vars. See
# http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-environment

aws s3 sync --acl=public-read --storage-class=REDUCED_REDUNDANCY public/ s3://anemone.dodgson.org

