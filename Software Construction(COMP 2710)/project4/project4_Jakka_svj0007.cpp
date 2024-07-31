/* Sujay Jakka
*  Svj0007
*  project4_Jakka_svj0007.cpp
*  Compiled using g++
*  Used Dr. Li's instructions for Project 4
*  Used Dr. Li's Hints for Project 4
*  Used Geeksforgeeks.org to understand getline() function from Dr.Li's Hints for Project 4
*  Used Tutorialspoint.com for the cin.ignore() function
*/

//Libary imports.
#include <iostream>
#include <assert.h>
using namespace std;


//Structure for creating a linked list that holds a trivia question,answer and point amount.
struct triva_node
{
    string question;
    string answer;
    int points;
    triva_node *next;
};

//Structure for keeping track of the linked list quiz.
//Keeps track of the first node(first question), last node(last question), and the total number of nodes(total questions).
//Prevents looping through linked list everytime.
struct triviaQuiz
{
    triva_node *head, *tail;
    int numOfQuestions;
};

//Initializes the quiz to have these three questions inputted into the linked list.
//Sets first question as the head and the last question as the tail to the triviaQuiz object, exam.
void initializeTriviaQuiz(triviaQuiz &exam)
{

    triva_node *firstQuestion = new triva_node;
    firstQuestion->question = "How long was the shortest war on record?";
    firstQuestion->answer = "38";
    firstQuestion->points = 100;
    exam.head = firstQuestion;
    exam.numOfQuestions++;


    triva_node *secondQuestion = new triva_node;
    firstQuestion->next = secondQuestion;
    secondQuestion->question = "What was Bank of America’s original name? (Hint: Bank of Italy or Bank of Germany)";
    secondQuestion->answer = "Bank of Italy";
    secondQuestion->points = 50;
    exam.numOfQuestions++;

    triva_node *thirdQuestion = new triva_node;
    secondQuestion->next = thirdQuestion;
    thirdQuestion->question = "What is the best-selling video game of all time? (Hint: Call of Duty or Wii Sports)";
    thirdQuestion->answer = "Wii Sports";
    thirdQuestion->points = 20;
    exam.tail = thirdQuestion;
    exam.numOfQuestions++;
}

//Function that allows user to create a question.
//Question is added to the end of the linked list.
//Sets the new question as the tail to the triviaQuiz object, exam.
void addQuestions(triviaQuiz &exam)
{
    triva_node *newQuestion = new triva_node;

    cout << "Enter a question: ";
    getline(cin, newQuestion->question);

    cout << "Enter an answer: ";
    getline(cin, newQuestion->answer);

    cout << "Enter award points: ";
    cin >> newQuestion->points;

    exam.tail->next = newQuestion;
    exam.tail = newQuestion;

    exam.numOfQuestions++;

}


//Checks for an invalid value for the number of questions to ask.
//Asks the user trivia questions and starts the game.
//Keeps track of the total points the user earned.
int askQuestions(triviaQuiz exam, int numQuestionsToAsk, int &score)
{
    score = 0;
    triva_node *currentTriviaQuestion = exam.head;
    string userAnswer = "";

    if (numQuestionsToAsk < 1)
    {
        cout << "Warning - the number of trivia to be asked must equal to or be larger than 1." << endl;
        return 1;
    }

    else if (numQuestionsToAsk > exam.numOfQuestions)
    {
        cout << "Warning - There is only " << exam.numOfQuestions << " trivia in the list." << endl;
        return 1;
    }

    else
    {
        for (int x = 0; x < numQuestionsToAsk; x++)
        {
            cout << "\nQuestion: " << currentTriviaQuestion->question << endl;
            cout << "Answer: ";
            getline(cin, userAnswer);

            if (userAnswer.compare(currentTriviaQuestion->answer) == 0) //correct_answer
            {
                cout << "Your answer is correct. You receive " << currentTriviaQuestion->points << " points." << endl;
                score += currentTriviaQuestion->points;
            }

            else
            {
                cout << "Your answer is wrong. The correct answer is: " << currentTriviaQuestion->answer << endl;
            }

            cout << "Your total points: " << score << endl;
            currentTriviaQuestion = currentTriviaQuestion->next;
        }

        cout << endl;
    }

    return 0;
}


//Test cases to check whether the methods work.
void Unit_Test()
{
    triviaQuiz exam;
    exam.numOfQuestions = 0;
    initializeTriviaQuiz(exam);
    int score;

    cout << "***This is a debugging version ***" << endl;
    cout << "Unit Test Case 1: Ask no question. The program should give a warning message." << endl;
    assert(askQuestions(exam, 0, score) == 1);
    cout << "Case 1 Passed" << endl << endl;

    cout << "Unit Test Case 2.1: Ask 1 question in the linked list. The tester enters an incorrect answer.";
    assert(askQuestions(exam, 1, score) == 0);
    cout << "Case 2.1 passed" << endl << endl;

    cout << "Unit Test Case 2.2: Ask 1 question in the linked list. The tester enters a correct answer.";
    assert(askQuestions(exam, 1, score) == 0);
    assert(score == 100);
    cout << "Case 2.2 passed" << endl << endl;

    cout << "Unit Test Case 3: Ask all the questions of the last trivia in the linked list.";
    assert(askQuestions(exam, 3, score) == 0);
    cout << "Case 3 passed" << endl << endl;

    cout << "Unit Test Case 4: Ask 5 questions in the linked list." << endl;
    assert(askQuestions(exam, 5, score) == 1);
    cout << "Case 4 passed" << endl << endl;

    cout << "*** End of the Debugging Version ***" << endl;
}

//Creates two versions, one version is debugging version and the other version is the production version.
//Commented out UNIT_TESTING(Debugging Version)

//#define UNIT_TESTING
#define TRIVIA_QUIZ
int main()
{
    //Debugging Version
    #ifdef UNIT_TESTING

    Unit_Test();
    return 0;

    #endif

    //Production Version
    //Creates a new trivia game.
    //Sets up three original questions.
    //Sets up loop for user to input his or her own questions.
    //Quiz questions are stored in linked list.

    #ifdef TRIVIA_QUIZ

    triviaQuiz exam;
    exam.numOfQuestions = 0;
    initializeTriviaQuiz(exam);
    int score;
    cout << "*** Welcome to Sujay's trivia quiz game ***\n";

    string addQuestionResponse = "";
    addQuestions(exam);
    cout << "Continue? (Yes/No): ";
    getline(cin.ignore(), addQuestionResponse);

    while(addQuestionResponse == "Yes")
    {
        addQuestions(exam);
        cout << "Continue? (Yes/No): ";
        getline(cin.ignore(), addQuestionResponse);
    }

    //This is start of Trivia quiz game.
    askQuestions(exam, exam.numOfQuestions, score);
    cout << "\n*** Thank you for playing the trivia quiz game. Goodbye! ***" << endl;

    return 0;
    #endif
}
