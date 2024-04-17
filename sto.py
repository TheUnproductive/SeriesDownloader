import libs.loaders as loaders
import argparse

def main(link: str, episode: int = 1):
    if "s.to" not in link:
        print("Invalid link")
        return
    
    else:
        loaders.sto(link, episode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", action="store", dest="link", type=str, required=True)
    args = parser.parse_args()

    link = args.link
    main(link)