"""
This file allows the tool to be ran with python -m <...>
"""
import sys
import publisher

if __name__ == '__main__':
    sys.exit(publisher.main(sys.argv))
