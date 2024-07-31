import java.util.Comparator;

/**
 * Autocomplete term representing a (query, weight) pair.
 * 
 */
public class Term implements Comparable<Term> {
   private String query;
   private long weight;

   /**
    * Initialize a term with the given query and weight.
    * This method throws a NullPointerException if query is null,
    * and an IllegalArgumentException if weight is negative.
    */
   public Term(String query, long weight) {
      if(query == null)
      {
         throw new NullPointerException("Query is null");
      
      }
      
      if(weight < 0)
      {
         throw new IllegalArgumentException("Weight is negative");
      
      }
      
      this.query = query;
      this.weight = weight;
      
      
   
   }

   /**
    * Compares the two terms in descending order of weight.
    */
   public static Comparator<Term> byDescendingWeightOrder() {
      return new compareByDescendingWeightOrder();
   }
   
   public static class compareByDescendingWeightOrder implements Comparator<Term>
   {
      public int compare(Term obj1, Term obj2)
      {
         if(obj1.weight == obj2.weight)
         {
            return 0;
         }
               
         if(obj1.weight < obj2.weight)
         {
            return 1;
               
         }
               
         return -1;
      }
   
   }

   /**
    * Compares the two terms in ascending lexicographic order of query,
    * but using only the first length characters of query. This method
    * throws an IllegalArgumentException if length is less than or equal
    * to zero.
    */
   public static Comparator<Term> byPrefixOrder(int length) {
      if(length <= 0)
      {
         throw new IllegalArgumentException("length is less than or equal to zero");
      }
      else
      {
         return new compareByPrefixOrder(length);  
      
      }
   
   }
   
   private static class compareByPrefixOrder implements Comparator<Term>
   {
      private int length;
      private compareByPrefixOrder(int length)
      {
         this.length = length;
      }
         
      public int compare(Term obj1, Term obj2)
      {
         String pre1, pre2;
         if(obj1.query.length() < length)
         {
            pre1 = obj1.query;
         }
         else
         {
            pre1 = obj1.query.substring(0, length);
         }
               
         if(obj2.query.length() < length)
         {
            pre2 = obj2.query;
         }
         else
         {
            pre2 = obj2.query.substring(0, length);
         }
         
         return pre1.compareTo(pre2);
         
      }
   
   
   
   
   }

   /**
    * Compares this term with the other term in ascending lexicographic order
    * of query.
    */
   @Override
   public int compareTo(Term other) {
      return this.query.compareTo(other.query);
   
   }

   /**
    * Returns a string representation of this term in the following format:
    * query followed by a tab followed by weight
    */
   @Override
   public String toString(){
      return query + "\t" + weight;
   
   }

}