from astroquery.jplhorizons import Horizons
import sys
import astropy 
import datetime # cringe can only handle ad, loss
import arrow

def calculate(year, denomination):
    # 301 is the id of the moon, geo refers to from earth and epochs are the start stop step for days which data we want to take from, and are variable. Epheremides print the astronomical data
    moon_data = Horizons(id='301', location='geo', epochs={'start':f'{denomination} {year}-06-18','stop':f'{denomination} {year}-07-19','step':'1d'}).ephemerides()
    # alpha refers to the STO angle, long story short, [0] is first angle value. The angle will be a float
    prev = float(moon_data['alpha'][0]) 
    candidates = []
    tangaroa = False # Method might be bad, don't like random booleans
    for i in range(1,32): # run through all dates which could possibly be matariki (July 19th limit)
        current = float(moon_data['alpha'][i]) 
        # if the numbers have started to be ascending, which means they are waning (since local maxima is new moon), and are above 90 (since 90 is quarter moon)
        if current > 90 and prev <= current: 
            tangaroa = True # the tangaroa period begins
        if tangaroa == True: # begin taking candidate matariki values
            if prev <= current: # if ascending
                candidates.append(i) 
            else: 
                break # moon is starting to reappear, tangaroa period is finished
        prev = current # to track if it is ascending
    candidates = candidates[0:4] #period is smaller for some reason, first 4 days for some reason someone else can figure out https://www.mbie.govt.nz/assets/maSpring%20Equinoxtariki-dates-2022-to-2052-matariki-advisory-group.pdf
    for i in candidates: 
        current = moon_data['datetime_str'][i] # datetime_str is the date info for each day
        # IN CASE BC IS GIVEN AS A PARAMETER, 'b' WILL BE THE FIRST VALUE, SO THIS IS THE CASE FOR BC
        if current[0] == 'b': 
            pass # yet to complete
        else: 
            curr_month = ""
            # break up string to figure out month, curr_month is set to a number since those are the parameters taken
            if current[5:8] == "Jun": 
                curr_month = 6 
            else:
                curr_month = 7 
            # take day from string
            curr_day = int(current[9:11]) 
            curr_weekday = datetime.datetime(year, curr_month, curr_day).weekday()
            if i == candidates[0]: # if first candidate 
                first_weekday = curr_weekday
            # weekday() returns 0-6 for monday to sunday
            if curr_weekday == 4: 
                formatted_message = current[5:8] + " " + str(curr_day) 
                return formatted_message 
    # in case not in candidates, it is outside of the tangaroa period so we need to find it 
    # less than 5 
    # annoying same as previous but uses the min and needs absolute value 
    # 
    if curr_weekday < 4:
        plus_diff = 4 - curr_weekday
    # then it is greater than 5 
    else:
        plus_diff = 5 + 6 - curr_weekday # because datetime is stupid 
    if first_weekday < 4:
        minus_diff = - 5 - 6 + first_weekday 
    # then it is greater than 5 
    else:
        minus_diff = first_weekday- 4

    if minus_diff <= plus_diff: # why is it less or equal, when does it state that it is broken broken 
        current = moon_data['datetime_str'][max(candidates[0]-minus_diff, 0)] # stupid 
    else: 
        current = moon_data['datetime_str'][candidates[-1]+plus_diff] # stupid 

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
        # how to make compatible with BC. Ok this is api search, someone else can do this and then reroute to me 
        curr_weekday = datetime.datetime(year, curr_month, curr_day).weekday()
        formatted_message = current[5:8] + " " + str(curr_day)
        return formatted_message 
    return "how"

# if there are less than 3 arguments, since the name of the file is counted as an argument and we need two arguments for year and denomination
if len(sys.argv) < 3:
    print("Usage: matarikicalculator.py year AD/BC")
# if year doesn't consist of numbers (invalid input)
elif sys.argv[1].isnumeric() == False: 
    print("Year has to be a positive number") 
elif sys.argv[2] != "AD" and sys.argv[2] != "BC": 
    print("Third argument is not AD or BC")
else:
    year = int(sys.argv[1]) # since we know it is numeric
    denomination = sys.argv[2] 
    # calculate function processes code needed for task 
    print(f"Matariki will occur on {calculate(year, denomination)} for the year {year} {denomination}")# obviously not done 

# Actual psuedocode/to do (thursday requires fully admin briefing): 
# give some psuedocode 
# No ephemeris for target "Moon" after A.D. 9999-DEC-30
# No ephemeris for target "Moon" prior to B.C. 9999-MAR-15 # going bogos 
# AD Horizons Error: Cannot interpret date
# closest friday not friday after if not in period
# make outside of tangaroa period code actually work 
# holy even more niche --> day where less than previous, but peaks in the middle  like 160 PEAK 161 <-- actually the mega math, which ones do you have to check to be certain this isn't occuring. Since i can't solve this imma stop everything 
# surface debug 
# finish fill out the test cases since you would know 
# finish give some psuedocode 


# Stuff that needs to be finished for 1st draft of algorithm: 
# chuck the main code into main, make it work with system parameters, and place that before the calculate function (looks cleaner)
# Figure out library for BC (line 30 requires, datetime can't handle BC), apparently https://docs.astropy.org/en/stable/time/index.html is it
# Explain the math needed for the bonus point (at the bottom of the factors, if we don't assume June 19th start) (if don't know how to do might have to use matplotlib)
# Figure out how to use the API for the bonus point and use it.
# Debug code when first draft is finished (in case missed some)


# Briefing on other project specific alternations to be made (introduce): 
# calling from C# someone else figure out: https://www.youtube.com/watch?v=g1VWGdHRkHs&ab_channel=AllTech
# interface debugging from C# end instead of from python's command line, might brick up, rather have a c# error message 


# TEST CASES to show that you are actually correct (documentation) 
# 2024 as 4 concatenation 
# 2028 before tangaroa period 
# 2033 after tangaroa period 
# 9999999999999999 AD Horizons Error: Cannot interpret date
# 99999 AD No ephemeris for target "Moon" after A.D. 9999-DEC-30
# 9999999999 AD No ephemeris for target "Moon" prior to B.C. 9999-MAR-15 WHAT??? 

#sources (add onto these): https://www.mbie.govt.nz/assets/matariki-dates-2022-to-2052-matariki-advisory-group.pdf

#Extra jobs (IGNORE)
#use get request api as last resort --> might need to learn for engineering science comp 
