MONGODB_VERSION="macos-arm64-7.0.14"
MONGODB_LOCAL="macos-aarch64-7.0.14"

# https://www.mongodb.com/try/download/community
if [ -f infra/local/mongodb-$MONGODB_VERSION.tgz ]; then
  echo "infra/local/mongodb-$MONGODB_VERSION.tgz exists, skipping download ..."
else
  echo "downloading to infra/local/mongodb-$MONGODB_VERSION.tgz  ..."
  curl https://fastdl.mongodb.org/osx/mongodb-$MONGODB_VERSION.tgz -o infra/local/mongodb-$MONGODB_VERSION.tgz
fi

if [ -d infra/local/mongodb-$MONGODB_LOCAL ]; then
  echo "infra/local/mongodb-$MONGODB_LOCAL exists, skipping unarchiving ..."
else
  echo "expanding to infra/local/mongodb-$MONGODB_LOCAL  ..."
  tar xfvz infra/local/mongodb-$MONGODB_VERSION.tgz -C infra/local
fi
