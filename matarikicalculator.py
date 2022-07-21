from astroquery.jplhorizons import Horizons
import sys
import astropy 
import datetime # cringe can only handle ad, loss
import arrow

#main

# so stupid, governments estimates don't even make sense, literally before tangaroa period (waning) for years such as 2024, is there a gregorian shift?? 
def calculate(year, denomination):
    # how to chuck in datea? 
    moon_data = Horizons(id='301', location='geo', epochs={'start':f'{denomination} {year}-06-18','stop':f'{denomination} {year}-07-19','step':'1d'}).ephemerides() # assuming this is for moon ripped from liang 
    prev = float(moon_data['alpha'][0]) # or is it 1 
    candidates = []
    tangaroa = False # sorry stupid method 
    for i in range(1,32): 
        current = float(moon_data['alpha'][i])    
        if current > 90 and prev <= current: # naive
            tangaroa = True 
        if tangaroa == True: 
            if prev <= current:
                candidates.append(i)
            else: 
                break
        prev = current
    candidates = candidates[0:4] # # period is smaller for some reason, first 4 days for some reason someone else can figure outhttps://www.mbie.govt.nz/assets/maSpring%20Equinoxtariki-dates-2022-to-2052-matariki-advisory-group.pdf
    for i in candidates:
        current = moon_data['datetime_str'][i]
        if current[0] == 'b':
            # finish it off after stuff below 
            pass
        else:
            curr_month = ""
            if current[5:8] == "Jun": # python not inclusive right? 
                curr_month = 6
            else:
                curr_month = 7
            curr_day = int(current[9:11])
            # how to make compatible with BC. Ok fuck off this is api search, someone else can do this and then reroute to me 
            curr_weekday = datetime.datetime(year, curr_month, curr_day).weekday()
            if curr_weekday == 4: # bruh how is 5 sat and 4 fri, because 0 is first 
                # how to format message 
                formatted_message = current[5:8] + " " + str(curr_day) # off by 1 error, how 
                return formatted_message 
    # some paths are fucked, some are alg (off by 1) 
    # in case not in candidates how to get friday after

    # can calculate out next friday 
    # less than 5
    if curr_weekday < 4:
        diff = 4 - curr_weekday
    # then it is greater than 5 
    else:
        diff = 5 + 6 - curr_weekday # because datetime is stupid 
    current = moon_data['datetime_str'][candidates[-1]+diff] # stupid 

    if current[0] == 'b':
        # finish it off after stuff below, same as above 
        pass
    else:
        curr_month = ""
        if current[5:8] == "Jun": # python not inclusive right? 
            curr_month = 6
        else:
            curr_month = 7
        curr_day = int(current[9:11])
        # how to make compatible with BC. Ok fuck off this is api search, someone else can do this and then reroute to me 
        curr_weekday = datetime.datetime(year, curr_month, curr_day).weekday()
        formatted_message = current[5:8] + " " + str(curr_day)
        return formatted_message 

    return "how"

if len(sys.argv) < 3:
    print("Usage: matarikicalculator.py year AD/BC") # relative to nz definate ? 
    
elif sys.argv[1].isnumeric() == False: 
    print("Year has to be a number") # what if you want BC? might be easy accept negative numbers
elif sys.argv[2] != "AD" and sys.argv[2] != "BC": 
    print("Third argument is not AD or BC")
else:
    year = int(sys.argv[1]) # need error prevention
    denomination = sys.argv[2]
    print(f"Matariki will occur on {calculate(year, denomination)} for the year {year} {denomination}")# obviously not done 

# TEST CASES to show that you are actually correct (documentation) 
# 2024 as 4 concatenation 
# 2028 as not within tangaroa period, have to get closest 

#Extra jobs
# do at shafquats: use get request api as last resort --> might need to learn for engineering science comp 

# Actual psuedocode/to do (thursday requires fully admin briefing) (nitty gritty): 
# closest friday not friday after if not in period
# make outside of tangaroa period code actually work 
# holy shit even more niche --> day where less than previous, but peaks in the middle  like 160 PEAK 161 <-- actually the mega math, which ones do you have to check to be certain this isn't occuring. Since i can't solve this imma stop everything 
# surface debug 
# give some psuedocode 
# clean up names of these tasks
# How am i supposed to keep up with two different versions (one which is fully mine, one which isn't)
# finish fill out the test cases since you would know 
# finish give some psuedocode 

# finish this, comments
# Menial Jobs (shitty gritty): 
# Figure out library for BC (and use it i guess) --> basically reveal, do for your own (don't want code polish fucking up my understanding)
# Debug and fix bugs (just make sure to spot how the fixes have been made) --> basically reveal, do for your own (don't want code polish fucking up my understanding)
# Baby math out the bonus point (if nobody else can do it might be matplotlib calling)
# Baby api browsing and using (fucking gay) 
# period is smaller for some reason, first 4 days for some reason someone else can figure outhttps://www.mbie.govt.nz/assets/maSpring%20Equinoxtariki-dates-2022-to-2052-matariki-advisory-group.pdf
#sources lmao https://www.mbie.govt.nz/assets/matariki-dates-2022-to-2052-matariki-advisory-group.pdf

# Briefing on other project specific alternations to be made: 
# calling from C# someone else figure out: https://www.youtube.com/watch?v=g1VWGdHRkHs&ab_channel=AllTech
# interface debugging from C# end instead of from python's command line, might brick up, rather have a c# error message 
