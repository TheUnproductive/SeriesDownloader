import libs.loaders as loaders
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", action="", dest="link", type=str, required=True)
args = parser.parse_args()

link = args.link

def main():
    if "s.to" not in link:
        print("Invalid link")
        return
    
    else:
        loaders.sto(link)

if __name__ == "__main__":
    main()