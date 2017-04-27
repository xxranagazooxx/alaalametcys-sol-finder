.SILENT:
nothing:
	echo "nothing specified. exiting..."
	exit

backupdb:
	mkdir -p ./backups/
	cp ./main.db ./backups/main.db."`date +\"%s\"`"

venv:
	if [ ! -d "./env" ]; then \
		virtualenv env --system-site-packages ;\
		source env/bin/activate; \
	else\
		echo "env exists. omitting...";\
	fi;

