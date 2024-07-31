import java.util.Arrays;


/**
 * Autocomplete.
 */
public class Autocomplete {

   private Term[] terms;

	/**
	 * Initializes a data structure from the given array of terms.
	 * This method throws a NullPointerException if terms is null.
	 */
   public Autocomplete(Term[] terms) {
      if(terms == null)
      {
         throw new NullPointerException("Terms is null.");
      }
      else
      {
         this.terms = new Term[terms.length];
         for(int i = 0; i < terms.length; i++)
         {
            this.terms[i] = terms[i];
         }
         
         Arrays.sort(this.terms);
      
      }
   }

	/** 
	 * Returns all terms that start with the given prefix, in descending order of weight. 
	 * This method throws a NullPointerException if prefix is null.
	 */
   public Term[] allMatches(String prefix) {
      if(prefix == null)
      {
         throw new NullPointerException("Prefix is null.");
      }
        
      else
      {
         Term term = new Term(prefix, 0);
         int indexOne = BinarySearch.firstIndexOf(terms, term, Term.byPrefixOrder(prefix.length()));
         if(indexOne == -1)
         {
            return new Term[0];
         }
         int indexLast = BinarySearch.lastIndexOf(terms, term, Term.byPrefixOrder(prefix.length()));
         Term[] matchesarr = new Term[1 + indexLast - indexOne];
         for(int i = 0; i < matchesarr.length; i++)
         {
            matchesarr[i] = terms[indexOne++];
            
         } 
         Arrays.sort(matchesarr, Term.byDescendingWeightOrder());
         return matchesarr;
      }
         
   }

}

