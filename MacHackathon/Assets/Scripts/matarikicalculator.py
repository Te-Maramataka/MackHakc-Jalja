from astroquery.jplhorizons import Horizons
import sys
import astropy 
import datetime # unfortunately only handles AD
import arrow

def calculate(year, denomination):
    moon_data = Horizons(id='301', location='geo', epochs={'start':f'{denomination} {year}-06-17','stop':f'{denomination} {year}-07-19','step':'1d'}).ephemerides()
    # 1. expanded to 6-17 because inclusive of transition day #2. dates before that are buffer days (7 more because ensures week cycle never issue)
    # 301 is the id of the moon, geo refers to from earth and epochs are the start stop step for days with data we want to take from, and are variable. Epheremides prints the astronomical data
    
    buffer_moon_data = Horizons(id='301', location='geo', epochs={'start':f'{denomination} {year}-06-10','stop':f'{denomination} {year}-06-17','step':'1d'}).ephemerides()
    prev = float(moon_data['alpha'][0]) # alpha refers to the STO angle, [0] is first angle value. The angle will be a float.
    candidates = []
    tangaroa = False # method may not be optimal (random booleans)
    
    for day in range(1,32): # run through all dates which could possibly be matariki (July 19th limit) 
        next_one = float(moon_data['alpha'][day+1]) 
        current = float(moon_data['alpha'][day]) 
        
        if next_one >= 90 and current < 90: # if the numbers begin to ascend, meaning they are waning (since local maxima is new moon), and are above 90 (since 90 is quarter moon)
            tangaroa = True # the tangaroa period begins
        if tangaroa == True: # begin taking candidate matariki values
            if prev <= current: # if ascending
                candidates.append(day)
            else: 
                break # moon is starting to reappear, tangaroa period is finished
        prev = current # iterate through angles
    candidates = candidates[0:min(len(candidates),4)] #period is smaller and first 4 days for some reason, use https://www.mbie.govt.nz/assets/maSpring%20Equinoxtariki-dates-2022-to-2052-matariki-advisory-group.pdf. Min in case not 4 candidates in list


    # random notes:
    # day after local maxima value is not included as moon is technically the start of the morning, (days are in a cycle) 
    # has to begin after 19 June. Entire period has to begin after 19th June  


    for c in candidates: 
        current = moon_data['datetime_str'][c] # datetime_str is the date info for each day
        # IN CASE BC IS GIVEN AS A PARAMETER, 'b' WILL BE THE FIRST VALUE, SO THIS IS THE CASE FOR BC
        
        if current[0] == 'b': 
            pass
        else: 
            curr_month = ""
            if current[5:8] == "Jun": # break up string to figure out month, curr_month is set to a number since those are the parameters taken
                curr_month = 6 
            else:
                curr_month = 7 
            pass # take day from string
            curr_day = int(current[9:11])
            curr_weekday = datetime.datetime(year, curr_month, curr_day).weekday() # weekday() returns 0-6 for monday to sunday
            
            if c == candidates[0]: # if first candidate 
                first_weekday = curr_weekday

            if curr_weekday == 4: 
                formatted_msg = current[5:8] + " " + str(curr_day) 
                return formatted_msg
            
    # calculation is off by one error
    # in case matariki is not in candidates, it is outside of the tangaroa period so we need to find it 
    # this value is less than 5 
    
    # same as previous issue but uses the min and needs absolute value, meaning it is a weekend
    if first_weekday == 5 or first_weekday == 6:
        if first_weekday < 4:
            diff = first_weekday - 5 - 6
        else:
            diff = first_weekday - 4
        '''
        moon_data = buffer_moon_data.extend(moon_data)
        moon_datetime = moon_data['datetime_str']
        buffer_moon_datetime = buffer_moon_data['datetime_str']
        moon_datetime = buffer_moon_datetime.extend(moon_datetime)
        '''
        if candidates[0]-diff < 0: 
            current = buffer_moon_data['datetime_str'][-diff] # lines 82-84 questionable 
        else: 
            current = moon_data['datetime_str'][candidates[0]-diff]

    else: 
        if curr_weekday < 4:
            diff = 4 - curr_weekday
        else:
            diff = 5 + 6 - curr_weekday # because datetime is questionable 
        current = moon_data['datetime_str'][candidates[-1]+diff] 

    # interpretation, tangaroa lunar period 
    if current[0] == 'b':
        pass # finish it off after code below, same as above
    else: 
        curr_month = ""
        if current[5:8] == "Jun":
            curr_month = 6 
        else:
            curr_month = 7
        curr_day = int(current[9:11])
        # Use API search to make compatible with BC, reroute to Josh after done
        curr_weekday = datetime.datetime(year, curr_month, curr_day).weekday()
        formatted_msg = current[5:8] + " " + str(curr_day)
        return formatted_msg 
    return "Error occured" # turn this into AD


'''
if len(sys.argv) < 3: # if there are less than 3 arguments, since the name of the file is counted as an argument and we need two arguments for year and denomination
    print("Usage: matarikicalculator.py year AD/BC") 
elif sys.argv[1].isnumeric() == False: 
    print("Year has to be a positive number") # if year doesn't consist of numbers (invalid input)
elif sys.argv[2] != "AD" and sys.argv[2] != "BC": 
    print("Third argument is not AD or BC")
else:
    year = int(sys.argv[1]) # since we know it is numeric
    denomination = sys.argv[2] 
    # calculate function processes code needed for task 
'''


years = [year for year in range(2022,2053)]
denomination = "AD"

for year in years: 
    print(f"Matariki will occur on {calculate(year, denomination)} for the year {year} {denomination}")# obviously not done

# use comp1 (current results) comp 2 (previous results) realone (actual correct outputs) to debug, good luck

'''
# Ur guys jobs
    # debug my current code 
    # Figure out library for BC (line 30 requires, datetime can't handle BC), apparently https://docs.astropy.org/en/stable/time/index.html is it
    # debug all possible years i guess...... watch out for error message
    # chuck the main code into main, make it work with system parameters, and place that before the calculate function (looks cleaner)
    # calling from C# someone else figure out: https://www.youtube.com/watch?v=g1VWGdHRkHs&ab_channel=AllTech
    # interface debugging from C# end instead of from python's command line, might brick up, rather have a c# error message 
        # just don't accept numbers greater these bounds here
    # No ephemeris for target "Moon" after A.D. 9999-DEC-30 
    # No ephemeris for target "Moon" prior to B.C. 9999-MAR-15 
    # AD Horizons Error: Cannot interpret date <-- from 999999999999999 way too high 
    # Line 104 return "Error occured" # turn this into an actual error message in unity itself

# + Stuff for hackathon rubric 
    # Readability: Comments + Readable Code 15 
    # Efficiency: Speed + Elegancy 10 
    # Reusability: Resolving into functions 15 
    # Documentation: Comments + Separate page explaining 10 

# Unneccissary to do these, do these if you wish to torture yourself:
    # holy even more niche --> day where less than previous, but peaks in the middle  like 160 PEAK 161 <-- actually the mega math, which ones do you have to check to be certain this isn't occuring. Since i can't solve this imma stop everything 
    # Explain the math needed for the bonus point (at the bottom of the factors, if we don't assume June 19th start) (if don't know how to do might have to use matplotlib)
    # Figure out how to use the API for the bonus point and use it. # yeah if we right we right, who cares
    # wonder if there is a way to not have limitations 

# How to test: 
    # python C:\Users\waste\Documents\GitHub\MackHakc-Jalja\MacHackathon\Assets\Scripts\matarikicalculator.py 2022 AD

# TEST CASES to show that you are actually correct (documentation):
    # Idk all dates given by government work just list some out in the documentation
    # some of them don't work because they also account for if it is a clear sky. 
    # 2036, 2042 
    # 9999999999999999 AD Horizons Error: Cannot interpret date
    # 99999 AD No ephemeris for target "Moon" after A.D. 9999-DEC-30
    # 9999999999 AD No ephemeris for target "Moon" prior to B.C. 9999-MAR-15 WHAT??? 

# IGNORE: 
    # previous issues which don't exist: 
    # define 6am as start of morning. Day after local maxima included. --> idk if it is in the government calculation. Guranteed. Literally can't have maxima be exactly moon its gonna lap over. Nevermind 
    # Take into consideration if it is a clear day or not

# Test case runner: 
    # modcheck

#sources (add onto these): https://www.mbie.govt.nz/assets/matariki-dates-2022-to-2052-matariki-advisory-group.pdf

#Extra jobs (IGNORE)
    #use get request api as last resort --> might need to learn for engineering science comp
'''
