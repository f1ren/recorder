PYTHONPATH=. python3 server.py  &
PYTHONPATH=. python3 main.py cam  &
read -r -p "Wait 1 seconds or press any key to continue immediately" -t 1 -n 1 -s
PYTHONPATH=. python3 main.py mic