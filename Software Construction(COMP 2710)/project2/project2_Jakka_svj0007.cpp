/* Sujay Jakka
*  Svj0007
*  project2_Jakka_svj0007.cpp
*  Compiled using g++
*  geeksforgeeks.org for the syntax of defining constants
*  Used Dr. Li's hints
*/
#include <iostream>
#include <stdlib.h>
#include <assert.h>
#include <ctime>
using namespace std;


/*
* Input: A_alive indicates Aaron is alive true for alive, false for dead
* B_alive indicates Bob is alive
* C_alive indicates Charlie is alive
* Return: true if at least two are alive otherwise return false
*/
bool at_least_two_alive(bool A_alive, bool B_alive, bool C_alive);



/*
* Call by reference
* Strategy 1: Everyone shoots to kill the highest accuracy player alive
* Input: B_alive indicates Bob is alive or dead
* C_alive indicates Aaron is alive or dead
* Return: Change B_alive into false if Bob is killed
* Change C_alive into false if Charlie is killed
*/
void Aaron_shoots1(bool& B_alive, bool& C_alive);



/*
* Call by reference
* Input: A_alive indicates Aaron is alive or dead
* C_alive indicates Charlie is alive or dead
* Return: Change A_alive into false if Aaron is killed
* Change C_alive into false if Charlie is killed
*/
void Bob_shoots(bool& A_alive, bool& C_alive);



/*
* Call by reference
* Input: A_alive indicates Aaron is alive or dead
* B_alive indicates Bob is alive or dead
* Return: Change A_alive into false if Aaron is killed
* Change B_alive into false if Bob is killed
*/
void Charlie_shoots(bool& A_alive, bool& B_alive);



/*
* Call by reference
* Strategy 2: Aaron intentionally misses if both are alive
* Input: B_alive indicates Bob is alive or dead
* C_alive indicates Aaron is alive or dead
* Return: Change B_alive into false if Bob is killed
* Change C_alive into false if Charlie is killed
*/
void Aaron_shoots2(bool& B_alive, bool& C_alive);


//Simple method to implement pause function in linux
void Press_any_key(void);


//TEST PROTOTYPES

void test_at_least_two_alive(void);
void test_Aaron_shoots1(void);
void test_Bob_shoots(void);
void test_Charlie_shoots(void);
void test_Aaron_shoots2(void);


//VARIABLES

//CONSTANTS

const int TOTAL_RUNS = 10000;
const double aaronProb = (1.0/3.0) * 100.0;
const double bobProb = (1.0/2.0) * 100.0;
const double charlieProb = 1.0 * 100.0;

int main()
{
    //Initializes Random number generator's seed and calls test functions
    cout << "*** Welcome to Sujay's Duel Simulator ***\n";
    srand(time(0));
    test_at_least_two_alive();
    Press_any_key();
    test_Aaron_shoots1();
    Press_any_key();
    test_Bob_shoots();
    Press_any_key();
    test_Charlie_shoots();
    Press_any_key();
    test_Aaron_shoots2();
    Press_any_key();

    //Starts strategy 1 and runs 10,000 times

    int aaronWins1 = 0;
    int bobWins = 0;
    int charlieWins = 0;

    cout << "Ready to test strategy 1 (run 10000 times):\n";
    Press_any_key();

    //Loop for runs
    for (int i = 0; i < TOTAL_RUNS; i++ )
    {
        //Initializing boolean variables before run
        bool aaronAlive = true;
        bool bobAlive = true;
        bool charlieAlive = true;

        //While loop for each duel, checks if at least two people are alive, if not then there is a winner and loop will be exited
        while (at_least_two_alive(aaronAlive, bobAlive, charlieAlive))
        {
            if (aaronAlive)
            {
                Aaron_shoots1(bobAlive, charlieAlive);
            }

            if (bobAlive)
            {
                Bob_shoots(aaronAlive, charlieAlive);
            }

            if (charlieAlive)
            {
                Charlie_shoots(aaronAlive, bobAlive);
            }
        }

        //Whoever is still alive is the winner and their win count will be incremented by one

        if (aaronAlive)
        {
            aaronWins1++;
        }

        if (bobAlive)
        {
            bobWins++;
        }

        if (charlieAlive)
        {
            charlieWins++;
        }


    }
    cout << "Aaron won " << aaronWins1 << "/10000 duels or " << static_cast<double>(aaronWins1) / TOTAL_RUNS * 100 << "%\n"
    << "Bob won " << bobWins << "/10000 duels or " << static_cast<double>(bobWins) / TOTAL_RUNS * 100 << "%\n"
    << "Charlie won " << charlieWins << "/10000 duels or " << static_cast<double>(charlieWins) / TOTAL_RUNS * 100 << "%\n"
    << endl;

    //Reinitializes variables and starts strategy 2 to run 10,000 times

    int aaronWins2 = 0;
    bobWins = 0;
    charlieWins = 0;

    cout << "Ready to test strategy 2 (run 10000 times):\n";
    Press_any_key();

    //Loop for runs
    for (int i = 0; i < TOTAL_RUNS; i++ )
    {

        //Initializing boolean variables before run
        bool aaronAlive = true;
        bool bobAlive = true;
        bool charlieAlive = true;

        //While loop for each duel, checks if at least two people are alive, if not then there is a winner and loop will be exited
        while (at_least_two_alive(aaronAlive, bobAlive, charlieAlive))
        {
            if (aaronAlive)
            {
                Aaron_shoots2(bobAlive, charlieAlive);
            }
            if (bobAlive)
            {
                Bob_shoots(aaronAlive, charlieAlive);
            }
            if (charlieAlive)
            {
                Charlie_shoots(aaronAlive, bobAlive);
            }
        }

        //Whoever is still alive is the winner and their win count will be incremented by one

        if (aaronAlive)
        {
            aaronWins2++;
        }
        if (bobAlive)
        {
            bobWins++;
        }
        if (charlieAlive)
        {
            charlieWins++;
        }
    }
    cout << "Aaron won " << aaronWins2 << "/10000 duels or " << static_cast<double>(aaronWins2) /
    TOTAL_RUNS * 100 << "%\n"
    << "Bob won " << bobWins << "/10000 duels or " << static_cast<double>(bobWins) / TOTAL_RUNS
    * 100 << "%\n"
    << "Charlie won " << charlieWins << "/10000 duels or " << static_cast<double>(charlieWins) /
    TOTAL_RUNS * 100 << "%\n"
    << endl;

    //Prints a statement depending on which of Aaron's strategies are better

    if (aaronWins1 > aaronWins2)
    {
        cout << "Strategy 1 is better than strategy 2.\n";
    }

    else
    {
        cout << "Strategy 2 is better than strategy 1.\n";
    }

    return 0;
}


//Implementation of functions. Look above for documentation of them.


//Function that checks if at least two of the people are alive
bool at_least_two_alive(bool A_alive, bool B_alive, bool C_alive)
{
    if((A_alive == true && B_alive == true) || (A_alive == true && C_alive == true) || (B_alive == true && C_alive == true))
    {
        return true;
    }

    else
    {
        return false;
    }
}

//Function that tests the at_least_two_alive function
void test_at_least_two_alive(void)
{
    cout << "Unit Testing 1: Function - at_least_two_alive()\n";
    cout << "\tCase 1: Aaron alive, Bob alive, Charlie alive\n";
    assert(true == at_least_two_alive(true, true, true));
    cout << "\tCase passed ...\n";

    cout << "\tCase 2: Aaron dead, Bob alive, Charlie alive\n";
    assert(true == at_least_two_alive(false, true, true));
    cout << "\tCase passed ...\n";

    cout << "\tCase 3: Aaron alive, Bob dead, Charlie alive\n";
    assert(true == at_least_two_alive(true, false, true));
    cout << "\tCase passed ...\n";

    cout << "\tCase 4: Aaron alive, Bob alive, Charlie dead\n";
    assert(true == at_least_two_alive(true, true, false));
    cout << "\tCase passed ...\n";

    cout << "\tCase 5: Aaron dead, Bob dead, Charlie alive\n";
    assert(false == at_least_two_alive(false, false, true));
    cout << "\tCase passed ...\n";

    cout << "\tCase 6: Aaron dead, Bob alive, Charlie dead\n";
    assert(false == at_least_two_alive(false, true, false));
    cout << "\tCase passed ...\n";

    cout << "\tCase 7: Aaron alive, Bob dead, Charlie dead\n";
    assert(false == at_least_two_alive(true, false, false));
    cout << "\tCase passed ...\n";

    cout << "\tCase 8: Aaron dead, Bob dead, Charlie dead\n";
    assert(false == at_least_two_alive(false, false, false));
    cout << "\tCase passed ...\n";

}


//Function for Aaron's first shooting strategy
void Aaron_shoots1(bool& B_alive, bool& C_alive)
{
    int shootResult = rand() % 100;
    if(shootResult <= aaronProb)
    {
        if (C_alive)
        {
            C_alive = false;
        }
        else
        {
            B_alive = false;
        }
    }
}


//Function that tests Aaron's first shooting strategy
void test_Aaron_shoots1(void)
{
    cout << "Unit Testing 2: Function Aaron_shoots1(Bob_alive, Charlie_alive)\n";

    bool bob_a = true;
    bool charlie_a = true;
    cout << "\tCase 1: Bob alive, Charlie alive\n"
         << "\t\tAaron is shooting at Charlie\n";
    Aaron_shoots1(bob_a, charlie_a);
    assert(true == bob_a);


    bob_a = false;
    charlie_a = true;
    cout << "\tCase 2: Bob dead, Charlie alive\n"
         << "\t\tAaron is shooting at Charlie\n";
    Aaron_shoots1(bob_a, charlie_a);
    assert(false == bob_a);

    bob_a = true;
    charlie_a = false;
    cout << "\tCase 3: Bob alive, Charlie dead\n"
         << "\t\tAaron is shooting at Bob\n";
    Aaron_shoots1(bob_a, charlie_a);
    assert(false == charlie_a);

}


//Function for Bob's shooting
void Bob_shoots(bool& A_alive, bool& C_alive)
{
    int shootResult = rand() % 100;
    if(shootResult <= bobProb)
    {
        if (C_alive)
        {
            C_alive = false;
        }
        else
        {
            A_alive = false;
        }
    }
}


//Function that tests Bob's shooting
void test_Bob_shoots(void)
{

    cout << "Unit Testing 3: Function Bob_shoots(Aaron_alive, Charlie_alive)\n";

    bool aaron_a = true;
    bool charlie_a = true;
    cout << "\tCase 1: Aaron alive, Charlie alive\n"
         << "\t\tBob is shooting at Charlie\n";
    Aaron_shoots1(aaron_a, charlie_a);
    assert(true == aaron_a);


    aaron_a = false;
    charlie_a = true;
    cout << "\tCase 2: Aaron dead, Charlie alive\n"
         << "\t\tBob is shooting at Charlie\n";
    Aaron_shoots1(aaron_a, charlie_a);
    assert(false == aaron_a);


    aaron_a = true;
    charlie_a = false;
    cout << "\tCase 3: Aaron alive, Charlie dead\n"
         << "\t\tBob is shooting at Aaron\n";
    Aaron_shoots1(aaron_a, charlie_a);
    assert(false == charlie_a);

}


//Function for Charlie's shooting
void Charlie_shoots(bool& A_alive, bool& B_alive)
{
    int shootResult = rand() % 100;
    if(shootResult <= charlieProb)
    {
        if (B_alive)
        {
            B_alive = false;
        }
        else
        {
            A_alive = false;
        }
    }
}


//Function that tests Charlie's shooting
void test_Charlie_shoots(void)
{
    cout << "Unit Testing 4: Function Charlie_shoots(Aaron_alive, Bob_alive)\n";

    bool aaron_a = true;
    bool bob_a = true;
    cout << "\tCase 1: Aaron alive, Bob alive\n"
         << "\t\tCharlie is shooting at Bob\n";
    Aaron_shoots1(aaron_a, bob_a);
    assert(true == aaron_a);


    aaron_a = false;
    bob_a = true;
    cout << "\tCase 2: Aaron dead, Bob alive\n"
         << "\t\tCharlie is shooting at Bob\n";
    Aaron_shoots1(aaron_a, bob_a);
    assert(false == aaron_a);


    aaron_a = true;
    bob_a = false;
    cout << "\tCase 3: Aaron alive, Bob dead\n"
         << "\t\tCharlie is shooting at Aaron\n";
    Aaron_shoots1(aaron_a, bob_a);
    assert(false == bob_a);

}


//Function for Aaron's second shooting strategy
void Aaron_shoots2(bool& B_alive, bool& C_alive)
{
    int shootResult = rand() % 100;

    if(!(B_alive && C_alive))
    {
        if(B_alive && (shootResult <= aaronProb))
        {
            B_alive = false;
        }

        if(C_alive && (shootResult <= aaronProb))
        {
            C_alive = false;
        }
    }
}


//Function that tests Aaron's second shooting strategy
void test_Aaron_shoots2(void)
{
    cout << "Unit Testing 5: Function Aaron_shoots2(Bob_alive, Charlie_alive)\n";

    bool bob_a = true;
    bool charlie_a = true;
    cout << "\tCase 1: Bob alive, Charlie alive\n"
         << "\t\tAaron intentionally misses his first shot\n";
    Aaron_shoots2(bob_a, charlie_a);
    assert(true == charlie_a);
    cout << "\t\tBoth Bob and Charlie are alive.\n";


    bob_a = false;
    charlie_a = true;
    cout << "\tCase 2: Bob dead, Charlie alive\n"
         << "\t\tAaron is shooting at Charlie\n";
    Aaron_shoots2(bob_a, charlie_a);
    assert(false == bob_a);

    bob_a = true;
    charlie_a = false;
    cout << "\tCase 3: Bob alive, Charlie dead\n"
         << "\t\tAaron is shooting at Bob\n";
    Aaron_shoots2(bob_a, charlie_a);
    assert(false == charlie_a);
}


//Temporarily stops runtime process until user presses a key
void Press_any_key(void)
{
    cout << "Press any key to continue..." << endl;
    cin.get();
}
