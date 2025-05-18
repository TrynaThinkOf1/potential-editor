if [ "$1" = "-man" ]; then
  op=$(python3 ~/mini/python/manual.py "$2")
  echo "$op"
else
  python3 ~/mini/python/main.py $1
fi