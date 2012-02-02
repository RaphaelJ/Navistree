<VirtualHost *:80>
	ServerName {server_name}
	DocumentRoot {document_root}
	ServerAdmin {server_admin}
	SuexecUserGroup {user} {user_group}
	RailsEnv development
	<Directory {document_root}>
		# allow .htaccess
		AllowOverride all
		# don't search for implicits extensions
		Options -MultiViews
		Options Indexes FollowSymLinks
		Order allow,deny
		Allow from all
	</Directory>
</VirtualHost>
