using UnityEngine;
using System;
using UnityEngine.UI;

//---------------------Dr Liang------------------------------
//Welcome to the brains of our operation, our algorithm,
//it works by finding the amount of lunar cycles that have occured since 1900
//it should be accurate for many years after 1900, but will degrade over a very long time as the amount of decimals we have will induce an error, can easily be fixed by having a more accurate constant
//firstly, it calcuates the amount of days since jan 5th 0001 lines 
//then, it finds the mod of our lunar cycle constant, effectively finding the current lunar cycle for the given date lines
//it repeats this until it finds a date that is in the right lunar cycle (3rd quarter), this is the tangaroa period, and the start of matariki lines
//after this, it finds the NZ holiday day, which is the closest friday to the start of the tangaroa lines
//you are welcome to de-comment the Debug.Logs to see the inner workings on unity

public class algorithm : MonoBehaviour
{   


    //runner of everything
    public string theYear;
    public GameObject inputField;
    public GameObject textDisplay;


    public void StoreYear()
    {
        theYear = inputField.GetComponent<Text>().text;
        textDisplay.GetComponent<TMPro.TextMeshProUGUI>().text = ("Answer: " + MatarikiDay(Convert.ToInt32(theYear))).Substring(0, 17);
    }

    //function returns the correct matarki day, and is the housing for the smaller algorithms
    public static DateTime MatarikiDay(int year)
    {
        //Functions takes the year as input and returns the date
        //return FirstFriday(MoonPhase(year)); //fix
        //29.53058770576 lunar cycle constant
        //22.14794077932 last quarter start
        //19 + 1 june onwards
        //Jan. 24, Wed 11:32 AM 1900 was a 3rd quarter start
        //jan 5th 12am was 3rd quarter start with moon age 9.92
        DateTime Date = new DateTime();
        for (int i = 20; i < 30; i++){ //check all days in june after the 19th
			//Debug.Log(new DateTime(year, 6, i).Date);
            if (IsCorrectMoonPhase(new DateTime(year, 6, i))){ //if in the right moon phase
                Date = new DateTime(year, 6, i);
                Date = FirstFriday(Date); //find closest friday
                break;
            }
        }

        if (Date.Month != 6){
            for (int i = 1; i < 31; i++){ //check all days in july
				//Debug.Log(new DateTime(year, 6, i).Date);
                if (IsCorrectMoonPhase(new DateTime(year, 7, i))){//if in the right moon phase
                    Date = new DateTime(year, 7, i);
                    Date = FirstFriday(Date); //find closest friday
                    break;
                }
            }
        }
        return Date; 
    }

    //grabs the first day of the CORRECT last quarter moon phase
    static bool IsCorrectMoonPhase(DateTime Date)
    {
        //find number of days since Jan. 24, Wed 11:32 AM 1900 (was a 3rd quarter start)
        //jan 5th 12am was 3rd quarter start with moon age 9.92
        double days = 0;
        days += (Date.Year) * 365.2422;
        if ( DateTime.IsLeapYear(Date.Year)){
            days += 31 + 29 + 31 + 30 + 31; // jan feb mar apr may
            if (Date.Month == 6){ //if month is june
                days += Date.Day;
            } else { //if month is july
                days += Date.Day + 30;
            }
        }
        else {
            days += 31 + 28 + 31 + 30 + 31; // jan feb mar apr may
            if (Date.Month == 6){ //if month is june
                days += Date.Day;
            } else { //if month is july
                days += Date.Day + 30;
            }
        }
        days -= 9.53735307356;// correction
        days -= 5; // subtract 5 for jan 5
        //now have the number of days since 1900

        //find the mod of the value to see if we are in correct moonphase
        double currentPhase = days % 29.53058770576;
        if (currentPhase >= 0f && currentPhase <= 7.38264692644f) { //are we in right moon phase
            return true;
        }
        else {
            return false;
        }
    }

    //finds closest friday to the Tangaroa Lunar Period
    static DateTime FirstFriday(DateTime Date)
    {
        int counterPlus = 0; //counters to keep track of how far the friday is from start of tangaroa period
        int counterMinus = 0;

        DateTime TempDatePlus = Date;
		DateTime TempDateMinus = Date;
        //counting forward
        while ((int) TempDatePlus.DayOfWeek != 5){ //if friday
            TempDatePlus = TempDatePlus.AddDays(1); //increment day
            //Debug.Log(TempDateMinus.Date);
            counterPlus += 1;
        }
		
		//Debug.Log(counterPlus);
		
        //counting Backward
        while ((int) TempDateMinus.DayOfWeek != 5){ //if friday
            TempDateMinus = TempDateMinus.AddDays(-1); //decrement day
			//Debug.Log(TempDateMinus.Date);
            counterMinus += 1;
        }
		
		//Debug.Log(counterMinus);
		
		//final result, see if forward or back is larger
        if (counterMinus > counterPlus){ //is back larger?
            return TempDatePlus; //return holiday date
        } 
        else {
            return TempDateMinus; //return holiday date
        }     
    }
}