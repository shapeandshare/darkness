MONGODB_LOCAL="macos-aarch64-7.0.14"
SESSION_ID=$(screen -ls | grep darkness-mongodb | awk '{print $1}')
echo
if [ -n "$SESSION_ID" ]; then
  echo "detected running mongodb session ($SESSION_ID), skipping startup ..."
else
  echo "starting local mongodb session ..."
  mkdir -p infra/local/data
  screen -dmS darkness-mongodb -h 1000 infra/local/mongodb-$MONGODB_LOCAL/bin/mongod --dbpath infra/local/data
fi
