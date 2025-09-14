# ! /bin/sh

HOST=lisp-trpg.sakura.ne.jp
USERNAME=lisp-trpg
REMOTE="www"
LOCAL="."

FROM="$REMOTE"
TO="$LOCAL"

lftp <<EOF
open -u $USERNAME $HOST
set ssl:check-hostname false
mirror \
--only-newer \
--parallel=2 \
$FROM \
$TO \
exit
EOF
