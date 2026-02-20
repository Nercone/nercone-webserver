sudo /usr/bin/systemctl stop nercone-webserver
/usr/bin/git pull
/home/nercone/.local/bin/uv tool uninstall nercone-webserver --no-cache || true
/home/nercone/.local/bin/uv tool install . --upgrade --no-cache
sudo /usr/bin/systemctl start nercone-webserver
