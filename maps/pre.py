"""
Pre-process a syllabus (class schedule) file. 

"""
#import arrow   # Dates and times
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

#base = arrow.now()   # Default, replaced if file has 'begin: ...'
#start_date = arrow.get(2017,9,25,0,0)   #this is the beginning date of the term, used to calculate week

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    lat = []
    lon = []
    
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            log.debug("Skipping")
            continue
        parts = line.split(',')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            lat.append (float(parts[0]))
            lon.append (float(parts[1]))
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                             "Split into |{}|".format("|".join(parts)))
    cooked = [lat,lon]

    return cooked


def main():
    f = open("data/poi.txt")
    parsed = process(f)
    print(parsed)


if __name__ == "__main__":
    main()
