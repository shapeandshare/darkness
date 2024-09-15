SESSION_ID=$(screen -ls | grep darkness-state | awk '{print $1}')
echo
if [ -n "$SESSION_ID" ]; then
  echo "detected running darkness-state session ($SESSION_ID), skipping startup ..."
else
  echo "starting darkness-state session ..."
  screen -dmS darkness-state -h 1000 infra/local/darkness.sh
fi
