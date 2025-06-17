import sys
import os

sys.path.append(os.path.abspath("src"))
from Trantorien import Trantorien

def main():
  if len(sys.argv) != 7:
    print("Usage: ./main.py -p PORT -n TEAM -h HOST")
    exit(84)

  port = int(sys.argv[2])
  team = sys.argv[4]
  host = sys.argv[6]

  bot = Trantorien(host, port, team)
  bot.connect()

  print("Looking:", bot.look())
  print("Forward:", bot.forward())
  print("Right:", bot.right())
  print("Forward:", bot.forward())
  print("Forward:", bot.forward())

  bot.close()

if __name__ == "__main__":
  main()