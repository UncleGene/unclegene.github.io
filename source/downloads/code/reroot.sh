launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
/usr/local/opt/mysql/bin/mysqld_safe --skip-grant-tables --skip-networking & 
mysql -e "UPDATE mysql.user SET Password=PASSWORD('new password') WHERE User='root'; FLUSH PRIVILEGES;"
/usr/local/bin/mysql.server stop
launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
