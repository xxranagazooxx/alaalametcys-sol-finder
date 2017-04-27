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
		sleep 2;\
		source env/bin/activate && pip install -r requirements.txt; \
	else\
		echo "env exists. omitting...";\
	fi;

