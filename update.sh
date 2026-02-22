sudo /usr/bin/systemctl stop nercone-webserver
/usr/bin/git pull
/root/.local/bin/uv tool uninstall nercone-webserver --no-cache || true
/root/.local/bin/uv tool install . --upgrade --no-cache
sudo /usr/bin/systemctl start nercone-webserver
