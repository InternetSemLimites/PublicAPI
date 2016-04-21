#!/bin/bash -x

FILE="README.md"
if [ "$1" == "shame" ]; then
	FILE="HALL_OF_SHAME.md"
fi

# Update itself
cd /home/automacao/InternetSemLimites/api/ && (
	git reset --hard HEAD; git clean -f -d; git pull origin HEAD
)

# Check for doc updates
cd /home/automacao/InternetSemLimites/doc/ && (
	# Hard reset to avoid committing invalid files
	git reset --hard HEAD; git clean -f -d; git pull origin HEAD

	URL="https://internetsemlimites.herokuapp.com/markdown/$FILE"

	# Validate remote path http status
        STATUS=`curl --write-out %{http_code} --insecure --connect-timeout 5 --silent --output /dev/null $URL`
        if [ "$STATUS" != "200" ]; then
                echo "invalid http status"
                exit 0
        fi

	# Get remote data to tmp file
	wget $URL -O $FILE.tmp

	# Validate if tmp file size is greater than 1KB
        SIZE=`du -k "README.md.tmp" | cut -f 1`
        if [ $SIZE -lt 1 ]; then
                rm -f $FILE.tmp
		echo invalid file size
		exit 0
	fi

	# Get MD5 sum and replace file if necessary
        MD5A=`md5sum $FILE |awk '{print $1}'`
        MD5B=`md5sum $FILE.tmp |awk '{print $1}'`

	if [ "$MD5A" != "$MD5B" ]; then
		mv -f $FILE.tmp $FILE
		git pull origin master
                git add . && (git commit -a -m "auto-update $FILE"; git push origin master)
	fi

	# Delete tmp files
	rm $FILE.tmp
)
