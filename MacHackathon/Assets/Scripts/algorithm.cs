using UnityEngine;
using System;

public class algorithm : MonoBehaviour
{   
    public int testYear = 2022;

    public void Start(){
        DateTime FinalAns = MatarikiDay(testYear);
		Debug.Log(FinalAns.Date);
    }


    public static DateTime MatarikiDay(int year)
    {
        //Functions takes the year as input and returns the date
        //return FirstFriday(MoonPhase(year)); //fix
        //29.53058770576 lunar cycle constant
        //22.14794077932 last quarter start
        //19 june onwards
        //Jan. 24, Wed 11:32 AM 1900 was a 3rd quarter start
        DateTime Date = new DateTime();
        for (int i = 19; i < 31; i++){ //check all days in june after the 19th
            if (IsCorrectMoonPhase(new DateTime(year, 5, i))){
                Date = new DateTime(year, 5, i);
                Date = FirstFriday(Date);
                break;
            }
        }

        if (Date.Month != 5){
            for (int i = 1; i < 32; i++){ //check all days in july
                if (IsCorrectMoonPhase(new DateTime(year, 5, i))){
                    Date = new DateTime(year, 6, i);
                    Date = FirstFriday(Date);
                    break;
                }
            }
        }

        return Date;
    }

    //grabs the first day of the CORRECT second quarter moon phase
    static bool IsCorrectMoonPhase(DateTime Date)
    {
        //find number of days since Jan. 24, Wed 11:32 AM 1900 was a 3rd quarter start
        double days = 0;
        days += (Date.Year - 1900) * 365.2422;
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
        days -= 24;
        //now have the number of days since 1900

        //find the mod of the value to see if we are in correct moonphase
        double currentPhase = days % 29.53058770576;
        if (currentPhase >= 0f && currentPhase <= 7.38264692644f) {
            return true;
        }
        else {
            return false;
        }
    }

    //finds closest friday to the Tangaroa Lunar Period
    static DateTime FirstFriday(DateTime Date)
    {
        int counterPlus = 0;
        //int counterMinus = 0;

        DateTime TempDatePlus = Date;
        //counting forward
        while ((int) TempDatePlus.DayOfWeek != 4){
            TempDatePlus = new DateTime(TempDatePlus.Year, TempDatePlus.Month, TempDatePlus.Day + 1);
            counterPlus += 1;
            Debug.Log(counterPlus);
        }
        //Debug.Log("now minus");
        //DateTime TempDateMinus = Date;
        ////counting backward
        //while ((int) TempDateMinus.DayOfWeek != 4){
        //    TempDatePlus = new DateTime(TempDatePlus.Year, TempDatePlus.Month, TempDatePlus.Day - 1);
        //    counterMinus += 1;
        //    Debug.Log(counterMinus);
        //}
//
        //if (counterMinus > counterPlus){
            return TempDatePlus;
        //} 
        //else {
        //    return TempDateMinus;
        //}     
    }
}