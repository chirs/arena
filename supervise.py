
import sys
from plumbing.supervisor import supervise

if __name__ == '__main__':
    _, host, port = sys.argv
    supervise(host, int(port))

