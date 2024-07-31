import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.FileWriter;
import java.lang.Math;
import java.util.Random;
import java.util.Scanner;


public class ProgrammingAssignment
{

    //Matrix for storing runtime for algorithms and theoretical complexity time
    private static long[][] matrix = new long[19][8];

    //Algorithm1 for finding the Maximum Sum Contiguous Subvector
    private static int Algorithm1(int X[])
    {
        int maxSoFar = 0;

        for(int L = 0; L < X.length; L++)
        {
            for(int U = L; U < X.length; U++)
            {
                int sum = 0;
                for(int I = L; I <= U; I++)
                {
                    sum = sum + X[I];
                }
                //sum now contains the sum of X[L..U]
                maxSoFar = max(maxSoFar, sum);
            }
        }
        return maxSoFar;
    }

    //Algorithm2 for finding the Maximum Sum Contiguous Subvector
    private static int Algorithm2(int X[])
    {
        int maxSoFar = 0;
        for(int L = 0; L < X.length; L++)
        {
            int sum = 0;
            for(int U = L; U < X.length; U++)
            {
                sum = sum + X[U];
                //sum now contains the sum of X[L..U]
                maxSoFar = max(maxSoFar, sum);
            }
        }
        return maxSoFar;
    }

    //Algorithm3 for finding the Maximum Sum Contiguous Subvector
    private static int Algorithm3_MaxSum(int X[], int L, int U)
    {
        //Zero-element vector
        if(L > U)
        {
            return 0;
        }

        //One-element vector
        if(L == U)
        {
            return Math.max(0, X[L]);
        }

        int M = (L + U) / 2;

        int sum = 0;
        int maxToLeft = 0;

        //Find max crossing to left
        for(int I = M; I >= 0; I--)
        {
            sum = sum + X[I];
            maxToLeft = Math.max(maxToLeft, sum);
        }

        sum = 0;
        int maxToRight = 0;

        //Find max crossing to right
        for(int I = M+1; I <= U; I++)
        {
            sum = sum + X[I];
            maxToRight = Math.max(maxToRight, sum);
        }
        int maxCrossing = maxToLeft + maxToRight;

        int maxInA = Algorithm3_MaxSum(X, L, M);
        int maxInB = Algorithm3_MaxSum(X, M+1, U);

        return max(maxCrossing, maxInA, maxInB);

    }

    //Algorithm4 for finding the Maximum Sum Contiguous Subvector
    private static int Algorithm4(int X[])
    {
        int maxSoFar = 0;
        int maxEndingHere = 0;

        for(int I = 0; I < X.length; I++)
        {
            maxEndingHere = max(0, maxEndingHere + X[I]);
            maxSoFar = max(maxSoFar, maxEndingHere);
        }

        return maxSoFar;
    }

    //Method to create an array of random positive and negative integers given a size
    //The integers generated are between the range -2^31 and 2^31
    private static int[] createArray(int size)
    {
        int arr[] = new int[size];

        Random rand = new Random();

        for(int i = 0; i < size; i++)
        {
            arr[i] = rand.nextInt();
        }

        return arr;
    }

    //Method that fills in the runtime and theoretical complexity matrix
    //Method does this by calculating the runtime and also calculating the time complexity given an array size N
    private static void findRunTimeandTimeComplexity(int arr[], int i, int N)
    {
        long startTime, endTime, t1, t2, averageTime = 0;
        double timeComplexity = 0;

        //Finds the runtime, t1, of running Algorithm1 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm1(arr);
        }
        endTime = System.nanoTime();
        t1 = endTime - startTime;

        //Finds the runtime, t2, of running Algorithm1 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm1(arr);
        }
        endTime = System.nanoTime();
        t2 = endTime - startTime;

        //Finds the average time of t1 and t2 and places it in the correction position of matrix
        averageTime = (t1 + t2) / 2;
        matrix[i][0] = averageTime;

        //Calculates the theoretical time complexity of algorithm1 using the size of the array
        timeComplexity = (7/6)*(Math.pow(N,3)) + 8 * (Math.pow(N,2)) + (53 * N / 6) + 4;
        matrix[i][4] = (long) (Math.ceil(timeComplexity));



        //Finds the runtime, t1, of running Algorithm2 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm2(arr);
        }
        endTime = System.nanoTime();
        t1 = endTime - startTime;


        //Finds the runtime, t2, of running Algorithm2 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm2(arr);
        }
        endTime = System.nanoTime();
        t2 = endTime - startTime;

        //Finds the average time of t1 and t2 and places it in the correction position of matrix
        averageTime = (t1 + t2) / 2;
        matrix[i][1] = averageTime;

        //Calculates the theoretical time complexity of algorithm2 using the size of the array
        timeComplexity = (13/2)*(Math.pow(N,2)) + (19*N/2) + 4;
        matrix[i][5] = (long) (Math.ceil(timeComplexity));



        //Finds the runtime, t1, of running Algorithm3 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm3_MaxSum(arr, 0, arr.length-1);
        }
        endTime = System.nanoTime();
        t1 = endTime - startTime;

        //Finds the runtime, t2, of running Algorithm3 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm3_MaxSum(arr, 0, arr.length-1);
        }
        endTime = System.nanoTime();
        t2 = endTime - startTime;

        //Finds the average time of t1 and t2 and places it in the correction position of matrix
        averageTime = (t1 + t2) / 2;
        matrix[i][2] = averageTime;

        //Calculates the theoretical time complexity of algorithm3 using the size of the array
        timeComplexity = Math.ceil(N * (Math.log(N)));
        matrix[i][6] = (long) timeComplexity;



        //Finds the runtime, t1, of running Algorithm4 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm4(arr);
        }
        endTime = System.nanoTime();
        t1 = endTime - startTime;

        //Finds the runtime, t2, of running Algorithm4 500 times
        startTime = System.nanoTime();
        for(int j = 0; j < 500; j++)
        {
            Algorithm4(arr);
        }
        endTime = System.nanoTime();
        t2 = endTime - startTime;

        //Finds the average time of t1 and t2 and places it in the correction position of matrix
        averageTime = (t1 + t2) / 2;
        matrix[i][3] = averageTime;

        //Calculates the theoretical time complexity of algorithm3 using the size of the array
        timeComplexity = Math.ceil((18 * N) + 5);
        matrix[i][7] = (long) timeComplexity;

    }


    //Max function that returns the maximum value of three numbers
    private static int max(int a, int b, int c)
    {
        int max = 0;

        if(a > b)
        {
            max = a;
        }
        else
        {
            max = b;
        }

        if(max > c)
        {
            return max;
        }
        else
        {
            return c;
        }
    }


    //Max function that returns the maximum value of two numbers
    private static int max(int a, int b)
    {

        if(a > b)
        {
            return a;
        }
        else
        {
            return b;
        }
    }


    //Method that writes runtime and time complexity matrix values into output file
    private static void writeOutputFile() throws IOException
    {
        FileWriter writer = new FileWriter("sujayshane_phw_output.txt");

        //Array of file headers
        String[] headers = {"algorithm-1","algorithm-2","algorithm-3","algorithm-4","T1(n)","T2(n)","T3(n)","T4(n)"};

        //Writes headers into output file
        writer.write(headers[0] + ",");
        writer.write(headers[1] + ",");
        writer.write(headers[2] + ",");
        writer.write(headers[3] + ",");
        writer.write(headers[4] + ",");
        writer.write(headers[5] + ",");
        writer.write(headers[6] + ",");
        writer.write(headers[7] + "\n");


        //Writes matrix values into output file
        for (int i = 0; i < 19; i++)
        {
            for (int j = 0; j < 8; j++)
            {
                writer.write(Long.toString(matrix[i][j]));

                //Writes a comma after every matrix value
                if (j < 7)
                {
                    writer.write(",");
                }
            }
            writer.write("\n");
        }

        writer.close();
    }

    public static void main(String[] args) throws FileNotFoundException, IOException
    {

        //Array of size 10 initialized for the values in input file phw_input.txt
        int X[] = new int[10];


        //Scans values in phw_input.txt and places them in array X
        File file = new File("phw_input.txt");
        Scanner sc = new Scanner(file);
        sc.useDelimiter(",");

        for(int i = 0; i < X.length; i++)
        {
            String next = sc.next().trim();
            X[i] = Integer.parseInt(next);
        }


        //Prints out the values returned from each Algorithm, Algorithm takes input X as input
        System.out.print("algorithm-1:" + Algorithm1(X) + ";" + "algorithm-2:" + Algorithm2(X) + ";" +  "algorithm-3:" + Algorithm3_MaxSum(X, 0, X.length - 1) + ";" + "algorithm-4:" + Algorithm4(X));


        //Creates 19 arrays of size 10 - 100
        int arr1[] = createArray(10);
        int arr2[] = createArray(15);
        int arr3[] = createArray(20);
        int arr4[] = createArray(25);
        int arr5[] = createArray(30);
        int arr6[] = createArray(35);
        int arr7[] = createArray(40);
        int arr8[] = createArray(45);
        int arr9[] = createArray(50);
        int arr10[] = createArray(55);
        int arr11[] = createArray(60);
        int arr12[] = createArray(65);
        int arr13[] = createArray(70);
        int arr14[] = createArray(75);
        int arr15[] = createArray(80);
        int arr16[] = createArray(85);
        int arr17[] = createArray(90);
        int arr18[] = createArray(95);
        int arr19[] = createArray(100);


        //Array of arrays to simplify access of each of the 19 arrays
        int[][] arrayOfArrays = {arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8, arr9, arr10, arr11, arr12, arr13, arr14, arr15, arr16, arr17, arr18, arr19};


        //Iterates through each array and calles the findRunTimeandTimeComplexity
        for(int i = 0; i < 19; i++)
        {
            findRunTimeandTimeComplexity(arrayOfArrays[i], i, arrayOfArrays[i].length);
        }


        //Calles method to output runtime and time complexity matrix values into file
        writeOutputFile();

    }
}