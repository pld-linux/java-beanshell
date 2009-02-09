#!/bin/sh

# set JAVA_HOME from jpackage-utils if available
if [ ! -f /usr/share/java-utils/java-functions ]; then
	echo >&2 "Java not found."
	exit 1
fi

. /usr/share/java-utils/java-functions
set_javacmd

exec $JAVACMD -jar $(find-jar bsh)
