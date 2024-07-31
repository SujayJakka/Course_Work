//Sujay Jakka
//Svj0007
//project1_Jakka_svj0007.cpp
//Compiled using g++
//w3schools.com for comment lines
//w3schools.com for creating functions
//w3schools.com for loops
//w3schools.com for else if statements
//programiz.com for Logical and
//w3schools.com for how to code user input
//cplusplus.com for including variable values in cout statement
//w3schools.com for setting boolean variables

#include <iostream>
using namespace std;

//function for setting up table

void printTable()
{
    cout << "*****************************************************************\n"
         << "\tAmortization Table\n"
         << "*****************************************************************\n"
         << "Month\tBalance\t\tPayment\tRate\tInterest Principal\n";
}

//function to calculate the amount of time to pay off loan

void timeToPayLoan(float loanAmount, float interest, float monthlyPayment)
{
    //initializing variables for function
    int months = 0;
    float balance = loanAmount;
    float currentMonthlyPayment = monthlyPayment;
    float principal = 0;
    float interestRatePerMonth = (interest / 100) / 12;
    float interestForMonth = 0;
    float totalInterestPaid = 0;

    //sets numeric output to two decimal places

    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);

    //prints the astericks, table name, and column names of the table

    printTable();

    //prints the first row of the column where month is 0

    cout << months << "\t$" << loanAmount;
    cout << "\t" << "N/A\tN/A\tN/A\t N/A\n";


    while(balance > 0)
    {

        interestForMonth = interestRatePerMonth * balance;

        //checks to see if the monthly payment is larger than the balance
        //if it is it will set the monthly payment for the last month to be the sum of the interest for the month and the principal
        if (currentMonthlyPayment > balance)
        {
            principal = balance;
            currentMonthlyPayment = interestForMonth + principal;
            balance = 0;
        }

        else
        {
            principal = currentMonthlyPayment - interestForMonth;
            balance -= principal;
        }

        totalInterestPaid += interestForMonth;

        months += 1;

        //prints the values for the table

        cout << months << "\t$";

        //adds an extra indent if the value is less than 1000
        if(balance < 1000)
        {
            cout << balance << "\t\t$";
        }

        else
        {
            cout << balance << "\t$";
        }

        cout <<  currentMonthlyPayment << "\t";
        cout << interestRatePerMonth * 100 << "\t$";
        cout << interestForMonth << "\t $";
        cout << principal << "\n";
    }

    //prints the amount of months it took to pay off the loan and also the total interest paid

    cout << "****************************************************************\n";
    cout << "\nIt takes " << months << " months to pay off "
         << "the loan.\n"
         << "Total interest paid is: $" << totalInterestPaid;
    cout << endl << endl;

}



int main()
{
    //creating input variables
    float loanAmount;
    float interest;
    float monthlyPayment;
    bool validInput = false;


    while(validInput != true)
    {
        //asking and retrieving input
        cout << "Loan Amount: ";
        cin >> loanAmount;
        cout << "Interest Rate (% per year): ";
        cin >> interest;
        cout << "Monthly Payments: ";
        cin >> monthlyPayment;
        cout << endl;

        //calculates interest rate for first month
        float interestForMonth = ((interest / 12) / 100) * loanAmount;

        //prints error message if the loan amount or monthly payment is not positive, or if the interest rate is negative
        if((loanAmount <= 0) || (interest < 0) || (monthlyPayment <= 0))
        {
            cout << "Error invalid input, loan amount and/or monthly payment is not positive, and/or interest rate is negative." << endl << endl;
        }

        //prints error message if the monthly payment is not larger than the monthly interest
        else if(interestForMonth >= monthlyPayment)
        {
            cout << "Error invalid input, monthly payment is not larger than monthly interest." << endl << endl;
        }

        else
        {

            //sets boolean variable to true to exit loop
            validInput = true;

            //calls function to calculate the amount of time to pay off loan
            timeToPayLoan(loanAmount, interest, monthlyPayment);
        }
    }

    return 0;

}
