if [ -d infra/local/venv ]; then
  echo "python runtime environment present, skipping setup ..."
else
  echo "setting up python runtime environment ..."
  python3 -m venv infra/local/venv
  source infra/local/venv/bin/activate
  pip install --upgrade pip
  pip install -r infra/local/requirements.server.txt
  deactivate
fi
