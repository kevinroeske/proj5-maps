"""
Pre-process a syllabus (class schedule) file. 

"""
import arrow   # Dates and times
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

base = arrow.now()   # Default, replaced if file has 'begin: ...'
start_date = arrow.get(2017,9,25,0,0)   #this is the beginning date of the term, used to calculate week

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None

    days_passed = 0                                                         #I went through the arrow doccumentation, and it wasn't clear
    current_date = arrow.now()                                              #whether the span_range() method returned anything like an integer
    for days in arrow.Arrow.span_range('day', start_date, current_date):    #value, but I did see that i could iterate over it and
        days_passed += 1                                                    #use an accumulator, then it's simple math to get the week number
    current_week = int(days_passed / 7) + 1
    entry = {}
    cooked = []
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            log.debug("Skipping")
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                             "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                base = arrow.get(content, "MM/DD/YYYY")
                # print("Base date {}".format(base.isoformat()))
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = {}
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content
            if int(content) == current_week:
                entry['is_current_week'] = "true"           #here we look at the current week and see if it's the one we are packaging,
            else:                                           #and set a flag accordingly in a field we add to the return object
                entry['is_current_week'] = "false"
        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked


def main():
    f = open("data/poi.txt")
    parsed = process(f)
    print(parsed)


if __name__ == "__main__":
    main()
