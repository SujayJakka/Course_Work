import java.util.ArrayList;
import java.util.Scanner;
import java.util.Arrays;
import java.io.FileReader;
import java.io.File;
import java.io.BufferedReader;
import java.util.TreeSet;
import java.util.Set;
import java.util.SortedSet;
import java.lang.Math;
import java.util.Iterator;
import java.util.List;
import java.util.ArrayDeque;
import java.util.Deque;



public class myGameEngine implements WordSearchGame
{
   private TreeSet<String> lexicon;
   private String[][] gameBoard;
   private int height;
   private int width;
   private boolean[][] stamped;
   private static final int around = 8;
   private SortedSet<String> allWords;
   private String correctWord;
   private ArrayList<Position> currentPath;
   private ArrayList<Integer> path;

     /**
    * Loads the lexicon into a data structure for later use. 
    * 
    * @param fileName A string containing the name of the file to be opened.
    * @throws IllegalArgumentException if fileName is null
    * @throws IllegalArgumentException if fileName cannot be opened.
    */
   public myGameEngine()
   {
      gameBoard = new String[4][4];
      width = gameBoard.length;
      height = gameBoard[0].length;
      resetBoard();
    
   }
   public void loadLexicon(String fileName) 
   {
      lexicon = new TreeSet<String>();
      if(fileName == null)
      {
         throw new IllegalArgumentException("File is null");
      }
      try
      {
         Scanner scan = new Scanner(new BufferedReader(new FileReader(new File(fileName))));
         while (scan.hasNext())
         {
            String word = scan.next();
            word = word.toUpperCase();
            lexicon.add(word);
            scan.nextLine();
         }
      
      }
      
      catch (java.io.FileNotFoundException e)
      {
         throw new IllegalArgumentException();
      
      
      }
         
   
   }
   
   /**
    * Stores the incoming array of Strings in a data structure that will make
    * it convenient to find words.
    * 
    * @param letterArray This array of length N^2 stores the contents of the
    *     game board in row-major order. Thus, index 0 stores the contents of board
    *     position (0,0) and index length-1 stores the contents of board position
    *     (N-1,N-1). Note that the board must be square and that the strings inside
    *     may be longer than one character.
    * @throws IllegalArgumentException if letterArray is null, or is  not
    *     square.
    */
   public void setBoard(String[] letterArray)
   {
      if(letterArray == null)
      {
         throw new IllegalArgumentException("Array is null");
      }
      int side = (int)Math.sqrt(letterArray.length);
      if((side * side) != letterArray.length)
      {
         throw new IllegalArgumentException();
         
      }
      gameBoard = new String[side][side];
      width = side;
      height = side;
      int index = 0;
      for(int i = 0; i < width; i++)
      {
         for(int j = 0; j < height; j++)
         {
            gameBoard[i][j] = letterArray[index];
            index++;
         }
      }
      resetBoard();
   
   
   }
   
   /**
    * Creates a String representation of the board, suitable for printing to
    *   standard out. Note that this method can always be called since
    *   implementing classes should have a default board.
    */
   public String getBoard()
   {
      String board = "";
      for(int i = 0; i < width; i++)
      {
         if(i > 0)
         {
            board += "\n";
         }
         for(int j = 0; j < height; j++)
         {
            board += gameBoard[i][j] + "";
         }
      }
      return board;
   }
   
   /**
    * Retrieves all scorable words on the game board, according to the stated game
    * rules.
    * 
    * @param minimumWordLength The minimum allowed length (i.e., number of
    *     characters) for any word found on the board.
    * @return java.util.SortedSet which contains all the words of minimum length
    *     found on the game board and in the lexicon.
    * @throws IllegalArgumentException if minimumWordLength < 1
    * @throws IllegalStateException if loadLexicon has not been called.
    */
   public SortedSet<String> getAllScorableWords(int minimumWordLength)
   {
      if(minimumWordLength < 1)
      {
         throw new IllegalArgumentException();
      }
      if(lexicon == null)
      {
         throw new IllegalStateException();
      }
      allWords = new TreeSet<String>();
      currentPath = new ArrayList<Position>();
      correctWord = "";
      for(int i = 0; i < height; i++)
      {
         for(int j = 0; j < width; j++)
         {
            correctWord = gameBoard[i][j];
            if(isValidWord(correctWord) && correctWord.length() >= minimumWordLength)
            {
               allWords.add(correctWord);
            }
            if (isValidPrefix(correctWord)) 
            {
               Position temp = new Position(i,j);
               currentPath.add(temp);
               boardSearch(i, j, minimumWordLength);
               currentPath.remove(temp);
            }
               
         }
         
         
      }
      return allWords;
         
   }
   
 /**
   * Computes the cummulative score for the scorable words in the given set.
   * To be scorable, a word must (1) have at least the minimum number of characters,
   * (2) be in the lexicon, and (3) be on the board. Each scorable word is
   * awarded one point for the minimum number of characters, and one point for 
   * each character beyond the minimum number.
   *
   * @param words The set of words that are to be scored.
   * @param minimumWordLength The minimum number of characters required per word
   * @return the cummulative score of all scorable words in the set
   * @throws IllegalArgumentException if minimumWordLength < 1
   * @throws IllegalStateException if loadLexicon has not been called.
   */  
   public int getScoreForWords(SortedSet<String> words, int minimumWordLength)
   {
      if(minimumWordLength < 1)
      {
         throw new IllegalArgumentException();
         
      }
         
      if(lexicon == null)
      {
         throw new IllegalStateException();
      }
      int score = 0;
      Iterator<String> itr = words.iterator();
      while(itr.hasNext())
      {
         String word = itr.next();
         if(word.length() >= minimumWordLength && isValidWord(word) && !isOnBoard(word).isEmpty())
         {
            score += (word.length() - minimumWordLength) + 1;
         }
      }
      return score;
   
   }
   
   /**
    * Determines if the given word is in the lexicon.
    * 
    * @param wordToCheck The word to validate
    * @return true if wordToCheck appears in lexicon, false otherwise.
    * @throws IllegalArgumentException if wordToCheck is null.
    * @throws IllegalStateException if loadLexicon has not been called.
    */
   public boolean isValidWord(String wordToCheck)
   {
      if(wordToCheck == null)
      {
         throw new IllegalArgumentException();
      }
      if(lexicon == null)
      {
         throw new IllegalArgumentException();
      }
      wordToCheck = wordToCheck.toUpperCase();
      return lexicon.contains(wordToCheck);
   }
   
   /**
    * Determines if there is at least one word in the lexicon with the 
    * given prefix.
    * 
    * @param prefixToCheck The prefix to validate
    * @return true if prefixToCheck appears in lexicon, false otherwise.
    * @throws IllegalArgumentException if prefixToCheck is null.
    * @throws IllegalStateException if loadLexicon has not been called.
    */
   public boolean isValidPrefix(String prefixToCheck)
   {
      if(prefixToCheck == null)
      {
         throw new IllegalArgumentException();
      }
         
      if(lexicon == null)
      {
         throw new IllegalStateException();
      }
         
      prefixToCheck = prefixToCheck.toUpperCase();
      String word = lexicon.ceiling(prefixToCheck);
      if(word != null)
      {
         return word.startsWith(prefixToCheck);
      }
      return false;
   }
       
   /**
    * Determines if the given word is in on the game board. If so, it returns
    * the path that makes up the word.
    * @param wordToCheck The word to validate
    * @return java.util.List containing java.lang.Integer objects with  the path
    *     that makes up the word on the game board. If word is not on the game
    *     board, return an empty list. Positions on the board are numbered from zero
    *     top to bottom, left to right (i.e., in row-major order). Thus, on an NxN
    *     board, the upper left position is numbered 0 and the lower right position
    *     is numbered N^2 - 1.
    * @throws IllegalArgumentException if wordToCheck is null.
    * @throws IllegalStateException if loadLexicon has not been called.
    */
   public List<Integer> isOnBoard(String wordToCheck)
   {
      if (wordToCheck == null) 
      {
         throw new IllegalArgumentException();
      }
      if (lexicon == null) 
      {
         throw new IllegalStateException();
      }
      currentPath = new ArrayList<Position>();
      wordToCheck = wordToCheck.toUpperCase();
      correctWord = "";
      path = new ArrayList<Integer>();
      for (int i = 0; i < height; i++) 
      {
         for (int j = 0; j < width; j ++) 
         {
            if (wordToCheck.equals(gameBoard[i][j])) 
            {
               path.add(i * width + j);
               return path;
            }
            if (wordToCheck.startsWith(gameBoard[i][j])) 
            {
               Position pos = new Position(i, j);
               currentPath.add(pos);
               correctWord = gameBoard[i][j];
               search(i, j, wordToCheck);
            
               if (!wordToCheck.equals(correctWord)) 
               {
                  currentPath.remove(pos);
               }
               else 
               {
                  for (Position p: currentPath) 
                  {
                     path.add((p.x * width) + p.y);
                  }
                  return path;
               }
            }
         }
      }
      return path;
   
   }
   
   private class Position
   {
      int x;
      int y;
         
      public Position(int x, int y)
      {
         this.x = x;
         this.y = y;
      }
         
      public String toString()
      {
         return "(" + x + "," + y + ")";
      }
         
      public Position[] nearby()
      {
         Position[] nbrs = new Position[around];
         int count = 0; 
         Position p;
         for(int i = -1; i <= 1; i++)
         {
            for(int j = -1; j <= 1; j++)
            {
               if(!((i == 0) && (j == 0)))
               {
                  p = new Position(x + i, y + j);
                  if(isValid(p))
                  {
                     nbrs[count++] = p;
                  }
               }
            }
         }
         return Arrays.copyOf(nbrs, count);
         
      }
   
   
   }
   
   private void boardSearch(int x, int y, int min)
   {
      Position start = new Position(x, y);
      resetBoard();
      resetPath();
      for(Position p : start.nearby())
      {
         if(!isStamped(p))
         {
            visit(p);
            if(isValidPrefix(correctWord + gameBoard[p.x][p.y]))
            {
               correctWord += gameBoard[p.x][p.y];
               currentPath.add(p);
               if(isValidWord(correctWord) && correctWord.length() >= min)
               {
                  allWords.add(correctWord);
               }
               boardSearch(p.x, p.y, min);
               currentPath.remove(p);
               int end = correctWord.length() - gameBoard[p.x][p.y].length();
               correctWord = correctWord.substring(0,end);
            }
               
         }
         
      }
      resetBoard();
      resetPath();
         
   
   
   }

   
   private boolean isValid(Position p)
   {
      return ( (p.x >= 0) && (p.x < width) && (p.y >= 0) && (p.y < height)); 
   }
   
   private void resetBoard()
   {
      stamped = new boolean[width][height];
      for(boolean[] row : stamped)
      {
         Arrays.fill(row, false);
      }
   
   }
   
   private void search(int x, int y, String wordToCheck)
   {
      Position start = new Position(x, y);
      resetBoard();
      resetPath();
      for(Position spot: start.nearby())
      {
         if(!isStamped(spot))
         {
            visit(spot);
            if(wordToCheck.startsWith(correctWord + gameBoard[spot.x][spot.y]))
            {
               correctWord += gameBoard[spot.x][spot.y];
               currentPath.add(spot);
               search(spot.x, spot.y, wordToCheck);
               if(wordToCheck.equals(correctWord))
               {
                  return;
               }
               else
               {
                  currentPath.remove(spot);
                  int end = correctWord.length() - gameBoard[spot.x][spot.y].length();
                  correctWord = correctWord.substring(0, end);
               }
            }
               
         }
         
         
      }
      resetBoard();
      resetPath();
   
   
   }
   
   private void visit(Position p)
   {
      stamped[p.x][p.y] = true;
   }
   
   private void resetPath()
   {
      for(int i = 0; i < currentPath.size(); i++)
      {
         visit(currentPath.get(i));
      }
   }
   
   private boolean isStamped(Position p)
   {
      return stamped[p.x][p.y];
   }
  

}