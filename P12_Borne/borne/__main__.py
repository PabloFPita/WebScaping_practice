import sys
import spider
import crawler

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 spyder.py YYYYMMDD or python3 spyder.py input_file.txt")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    if input_arg.endswith(".txt"):
        with open(input_arg, "r") as file:
            dates = file.readlines()
            for date in dates:
                date = date.strip()
                spider.run(date)
    else:
        date = input_arg
        spider.run(date)
    
    # crawler.run()