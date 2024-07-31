//Compiled using g++ compiler

//Test Data

//Trial 1 Inputs in order  - 155, y, 200, n, 50, y, 120, y, 75, n, 4
//Result - 456326325

//Trial 2 Inputs in order - 45, n, 85, y, 20, y, 70, n, 50, y, 5
//Result - 698526906

//Trial 3 Inputs in order - 200, y, 315, y, 270, n, 133, y, 194, y, 3
//Result - 99137080

#include <iostream>

using namespace std;

int main()
{
    unsigned long long totalCombinations = 0;
    int totalUsersToChooseFrom = 0;
    int usersThatLikeInterest = 0;
    string likesInterest = "";
    int amountOfBumps = 0;
    unsigned long long nOverNMinusK = 1;
    long kFactorial = 1;

    cout << "Bump! is an app that allows you to make meaningful connections from unexpected encounters by setting you up with existing and mutual "
            "friends to talk to each week. Bump! functions as a social media platform that allows you to earn tokens each month by interacting "
            "with your friends. Throughout the month, these tokens can be used to add other users based on specified interests." << endl << endl;

    cout << "This program will simulate one's Bumps for the week by only taking the user's interests into account not their mutual friends, existing friends, or "
            "location like the actual platform. A user is set up with two Bumps per week on the actual platform but for the sake of this project the "
            "user can select 2-6 Bumps." << endl << endl;

    cout << "The user can select one or multiple interests." << endl << endl;



    cout << "Please enter below the amount of users that ONLY selected Sports as their interest." << endl;
    cin >> usersThatLikeInterest;
    cout << "Do you like Sports? (y/n)" << endl;
    cin >> likesInterest;
    cout << endl;
    if(likesInterest.compare("y") == 0)
    {
        totalUsersToChooseFrom += usersThatLikeInterest;
    }
    usersThatLikeInterest = 0;
    likesInterest = "";


    cout << "Please enter below the amount of users that ONLY selected Music as their interest." << endl;
    cin >> usersThatLikeInterest;
    cout << "Do you like Music? (y/n)" << endl;
    cin >> likesInterest;
    cout << endl;
    if(likesInterest.compare("y") == 0)
    {
        totalUsersToChooseFrom += usersThatLikeInterest;
    }
    usersThatLikeInterest = 0;
    likesInterest = "";


    cout << "Please enter below the amount of users that ONLY selected Reading as their interest." << endl;
    cin >> usersThatLikeInterest;
    cout << "Do you like Reading? (y/n)" << endl;
    cin >> likesInterest;
    cout << endl;
    if(likesInterest.compare("y") == 0)
    {
        totalUsersToChooseFrom += usersThatLikeInterest;
    }
    usersThatLikeInterest = 0;
    likesInterest = "";


    cout << "Please enter below the amount of users that ONLY selected Movies & Tv as their interest." << endl;
    cin >> usersThatLikeInterest;
    cout << "Do you like Movies & Tv? (y/n)" << endl;
    cin >> likesInterest;
    cout << endl;
    if(likesInterest.compare("y") == 0)
    {
        totalUsersToChooseFrom += usersThatLikeInterest;
    }
    usersThatLikeInterest = 0;
    likesInterest = "";


    cout << "Please enter below the amount of users that ONLY selected Cooking as their interest." << endl;
    cin >> usersThatLikeInterest;
    cout << "Do you like Cooking? (y/n)" << endl;
    cin >> likesInterest;
    cout << endl;
    if(likesInterest.compare("y") == 0)
    {
        totalUsersToChooseFrom += usersThatLikeInterest;
    }
    usersThatLikeInterest = 0;
    likesInterest = "";


    cout << "Please enter below the amount of Bumps you want for the week. You can select between 2-6 Bumps inclusive." << endl;
    cin >> amountOfBumps;
    cout << endl;

    for(int i = totalUsersToChooseFrom; i > (totalUsersToChooseFrom - amountOfBumps) ; i--)
    {
        nOverNMinusK *= i;
    }

    for(int i = 1; i <= amountOfBumps; i++)
    {
        kFactorial *= i;
    }

    totalCombinations = nOverNMinusK / kFactorial;

    cout << "The total amount of combinations for your Bumps for the week is " << totalCombinations << " combinations!" << endl;
}
