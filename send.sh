#!/bin/bash

# =========================
# Automated Mail Sender
# =========================

FROM_NAME="Amazon Hunter Original"
FROM_EMAIL="noreply@amazon.com"
SUBJECT="Hunter Original: The last pair of boots you'll ever buy"

HTML_FILE="offer.html"
LIST="all.txt"

# Send email to each recipient
while IFS= read -r TO || [[ -n "$TO" ]]; do

(
echo "From: $FROM_NAME <$FROM_EMAIL>"
echo "To: $TO"
echo "Subject: $SUBJECT"
echo "MIME-Version: 1.0"
echo "Content-Type: text/html; charset=UTF-8"
echo
cat "$HTML_FILE"
) | /usr/sbin/sendmail -t

echo "$(date '+%Y-%m-%d %H:%M:%S') - Sent to $TO"

done < "$LIST"
