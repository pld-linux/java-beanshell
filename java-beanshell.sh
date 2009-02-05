#!/bin/sh

if [ "$JAVA_HOME" ]; then
  JAVA=$JAVA_HOME/bin/java
else
  if [ -x /usr/bin/gij ]; then
    JAVA=/usr/bin/gij
  else
    if [ -x /usr/bin/java ]; then
      JAVA=/usr/bin/java
    else
      echo "Java not found." >&2
      exit 1
    fi
  fi
fi

$JAVA -jar $(find-jar bsh)
