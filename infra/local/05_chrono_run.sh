SESSION_ID=$(screen -ls | grep darkness-chrono | awk '{print $1}')
echo
if [ -n "$SESSION_ID" ]; then
  echo "detected running darkness-chrono session ($SESSION_ID), skipping startup ..."
else
  echo "starting darkness-chrono session ..."
  screen -dmS darkness-chrono -h 1000 infra/local/chrono.sh
fi
