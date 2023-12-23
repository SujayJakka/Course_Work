/* Sujay Jakka
*  Svj0007
*  project3_Jakka_svj0007.cpp
*  Compiled using g++
*  Used Dr. Li's Sample Code from Project 3 Directions
*  Used Dr. Li's Lecture 4 slides
*/


#include <fstream>
#include <iostream>
#include <cstdlib>
using namespace std;


//Global Variables

const int MAX_SIZE = 100;
int outputArray[MAX_SIZE * 2];


//Function that reads the numeric data in a file and puts it into an integer array
//Returns input array size

int readFile(int inputArray[], ifstream& inStream)
{
    //Variable to keep track of input array size
    int index = 0;

    //Copies all the integers from the file into inputArray
    inStream >> inputArray[index];
    while (! inStream.eof())
    {
        index++;
        inStream >> inputArray[index];
    }

    return index;
}

//Function that inputs the integers from iArray1 and iArray2 into the global variable outputArray
//Function then sorts the integers in outputArray in ascending order
//Function then returns outputArraySize

int mergeInputArrays(int iArray1[], int iArray2[], int iArray1_size, int iArray2_size)
{
    //Variable to keep track of output array size
    int outputArrayIndex = 0;

    //Copies the integers from iArray1 to outputArray
    for(int i = 0; i < iArray1_size; i++)
    {
        outputArray[outputArrayIndex] = iArray1[i];
        outputArrayIndex++;
    }

    //Copies the integers from iArray2 to outputArray
    for(int i = 0; i < iArray2_size; i++)
    {
        outputArray[outputArrayIndex] = iArray2[i];
        outputArrayIndex++;
    }

    //Sorts the integers in outputArray
    for(int i = 0; i < outputArrayIndex - 1; i++)
    {
        for(int j = i + 1; j < outputArrayIndex; j++)
        {
            if(outputArray[i] > outputArray[j])
            {
                int temp = outputArray[i];
                outputArray[i] = outputArray[j];
                outputArray[j] = temp;
            }
        }
    }

    return outputArrayIndex;

}

//Function that writes the integers in the global variable outputArray
//into an output file specified by the user

void writeFile(int outputArraySize, string outputFileName)
{
    //Declares outstream variable
    ofstream outStream;

    //Opens the outstream to the file
    outStream.open(outputFileName.c_str());

    //Checks if the file specified by the user can be opened
    //If file cannot be opened the program will be terminated
    if(outStream.fail())
    {
        cout << "Output file opening failed." << endl;
        exit(1);
    }

    //Writes the contents in outputArray into the file
    for(int i = 0; i < outputArraySize; i++)
    {
        outStream << outputArray[i] << endl;
    }

    //Closes the outstream to the file
    outStream.close();
}

int main()
{
    //Main method variables declaration
    ifstream inStream;
    int iArray1[MAX_SIZE];
    int iArray2[MAX_SIZE];
    int iArray1_size, iArray2_size, outputArraySize;
    string fileName1, fileName2, outputFileName;

    cout << "*** Welcome to Sujay's sorting program ***" << endl;

    //Gets the first input file name from user and opens the instream to this file

    cout << "Enter the first input file name: ";
    cin >> fileName1;

    inStream.open((char*)fileName1.c_str());

    //Checks if the file specified by the user can be opened
    //If file cannot be opened the program will be terminated

    if (inStream.fail())
    {
        cout << "Input file opening failed." << endl;
        exit(1);
    }

    //Calls readFile function to read the integer data in the file and to input that data into iArray1

    iArray1_size = readFile(iArray1, inStream);

    //Closes the instream to the file

    inStream.close();

    //Outputs the size of iArray1 and integers in the array

    cout << "The list of " << iArray1_size << " numbers in file " << fileName1 << " is:" << endl;

    for(int i = 0; i < iArray1_size; i++)
    {
        cout << iArray1[i] << endl;
    }

    cout << endl;

    //Gets the second input file name from user and opens the instream to this file

    cout << "Enter the second input file name: ";
    cin >> fileName2;

    inStream.open((char*)fileName2.c_str());

    //Checks if the file specified by the user can be opened
    //If file cannot be opened the program will be terminated

    if (inStream.fail())
    {
        cout << "Input file opening failed." << endl;
        exit(1);
    }

    //Calls readFile function to read the integer data in the file and to input that data into iArray2

    iArray2_size = readFile(iArray2, inStream);

    //Closes the instream to the file

    inStream.close();

    //Outputs the size of iArray2 and integers in the array

    cout << "The list of " << iArray2_size << " numbers in file " << fileName2 << " is:" << endl;

    for(int i = 0; i < iArray2_size; i++)
    {
        cout << iArray2[i] << endl;
    }

    cout << endl;

    //Calls mergeInputArrays to input the integers in both arrays into outputArray
    //The function also sorts the integers in outputArray once it is inputed
    //Returns the size of outputArray

    outputArraySize = mergeInputArrays(iArray1, iArray2, iArray1_size, iArray2_size);

    //Outputs the size of outputArray and also the integers in the array

    cout << "The sorted list of " << outputArraySize << " numbers is:";

    for(int i = 0; i < outputArraySize; i++)
    {
        cout << " " << outputArray[i];
    }

    cout << endl;

    //Asks user for output file name to write the data in outputArray to

    cout << "Enter the output file name: ";
    cin >> outputFileName;

    //Calls writeFile function to write the data in outputArray to the file specified by user

    writeFile(outputArraySize, outputFileName);

    //Displays the output file name and a closing message

    cout << "*** Please check the new file - " << outputFileName << " ***" << endl;
    cout << "*** Goodbye. ***" << endl;

    return 0;

}



