from datetime import datetime

def extract_list(list_string):
    return list_string.strip("[]").replace("'", "").split(", ")

def formatDate(dateString):
    if "." in dateString:
        return datetime.strftime(datetime.strptime(dateString, "%d. %B %Y"), "%Y-%m-%d")
    # elif "-" in dateString:
    #     return datetime.strftime(datetime.strptime(dateString, "%Y-%m-%d"), "%d. %B %Y")
# 
    else:
        return dateString
