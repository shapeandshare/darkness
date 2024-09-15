for session_id in $(screen -ls | grep -i darkness- | awk '{print $1}'); do
  echo "terminating $session_id"
  screen -XS $session_id kill
done
