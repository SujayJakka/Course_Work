import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.TreeSet;

import java.util.stream.Collectors;

/**
 * Provides an implementation of the WordLadderGame interface. 
 *
 * @author Sujay Jakka (svj0007@auburn.edu)
 */
public class Doublets implements WordLadderGame 
{

    // The word list used to validate words.
    // Must be instantiated and populated in the constructor.
    /////////////////////////////////////////////////////////////////////////////
    // DECLARE A FIELD NAMED lexicon HERE. THIS FIELD IS USED TO STORE ALL THE //
    // WORDS IN THE WORD LIST. YOU CAN CREATE YOUR OWN COLLECTION FOR THIS     //
    // PURPOSE OF YOU CAN USE ONE OF THE JCF COLLECTIONS. SUGGESTED CHOICES    //
    // ARE TreeSet (a red-black tree) OR HashSet (a closed addressed hash      //
    // table with chaining).
    /////////////////////////////////////////////////////////////////////////////

    /**
     * Instantiates a new instance of Doublets with the lexicon populated with
     * the strings in the provided InputStream. The InputStream can be formatted
     * in different ways as long as the first string on each line is a word to be
     * stored in the lexicon.
     */
     
   List<String> emptyLadder = new ArrayList<>();
   int wordCount;
   TreeSet<String> lexicon;
    
   public Doublets(InputStream in) {
      try {
            //////////////////////////////////////
            // INSTANTIATE lexicon OBJECT HERE  //
            //////////////////////////////////////
         lexicon = new TreeSet<String>();
         Scanner s =
                new Scanner(new BufferedReader(new InputStreamReader(in)));
         while (s.hasNext()) {
            String str = s.next();
                /////////////////////////////////////////////////////////////
                // INSERT CODE HERE TO APPROPRIATELY STORE str IN lexicon. //
                /////////////////////////////////////////////////////////////
            lexicon.add(str.toLowerCase());
            wordCount++;
            s.nextLine();
         }
         in.close();
      }
      catch (java.io.IOException e) 
      {
         System.err.println("Error reading from InputStream.");
         System.exit(1);
      }
   }


    //////////////////////////////////////////////////////////////
    // ADD IMPLEMENTATIONS FOR ALL WordLadderGame METHODS HERE  //
    //////////////////////////////////////////////////////////////
    
   public int getHammingDistance(String a, String b) 
   {
   
      int result = 0;
   
      if (a.length() != b.length()) 
      {
         return -1;
      }
   
      char[] str1 = a.toCharArray();
      char[] str2 = b.toCharArray();
   
      for (int i = 0; i < a.length(); i++) 
      {
         if (str1[i] != str2[i]) 
         {
            result++;
         }
      }
   
      return result;
   }
   
   
   public List<String> getMinLadder(String start, String end) 
   {
   
      return null;
   }
   
   public List<String> getNeighbors(String word) 
   {
   
      ArrayList result = new ArrayList();
   
      for (String s: lexicon) 
      {
         if (getHammingDistance(word, s) == 1) 
         {
            result.add(s);
         }
      }
   
      if (result.isEmpty()) 
      {
         return emptyLadder;
      }
   
      return result;
   }
   
   public int getWordCount() 
   {
   
      return lexicon.size();
   }
   
   public boolean isWord(String a) 
   {
   
      if (lexicon.contains(a)) 
      {
         return true;
      }
   
      return false;
   }
   
   public boolean isWordLadder(List<String> seq) 
   {
   
      if (seq.isEmpty()) 
      {
         return false;
      }
   
      for (int i = 0; i < seq.size() - 1; i++) 
      {
         if (getHammingDistance(seq.get(i), seq.get(i + 1)) != 1) 
         {
            return false;
         }
      }
   
      for (int i = 0; i < seq.size(); i++) 
      {
         if (!lexicon.contains(seq.get(i))) 
         {
            return false;
         }
      }
   
      return true;
   }
   
}


