import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * Defines a library of selection methods on Collections.
 *
 * @author  Sujay Jakka (svj0007@auburn.edu)
 *
 */
public final class Selector {

/**
* Can't instantiate this class.
*
* D O   N O T   C H A N G E   T H I S   C O N S T R U C T O R
*
*/
   private Selector() { }


   /**
    * Returns the minimum value in the Collection coll as defined by the
    * Comparator comp. If either coll or comp is null, this method throws an
    * IllegalArgumentException. If coll is empty, this method throws a
    * NoSuchElementException. This method will not change coll in any way.
    *
    * @param coll    the Collection from which the minimum is selected
    * @param comp    the Comparator that defines the total order on T
    * @return        the minimum value in coll
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> T min(Collection<T> coll, Comparator<T> comp) 
   {
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
      
      if(coll.size() == 0)
      {
         throw new NoSuchElementException("Error");
      }
      T min = null;
      for(T x : coll)
      {
         if(min == null)
         {
            min = x;
         }
         else
         {
            if(comp.compare(x, min) < 0)
            {
               min = x;
            }
         }
      }
      return min;
   }


   /**
    * Selects the maximum value in the Collection coll as defined by the
    * Comparator comp. If either coll or comp is null, this method throws an
    * IllegalArgumentException. If coll is empty, this method throws a
    * NoSuchElementException. This method will not change coll in any way.
    *
    * @param coll    the Collection from which the maximum is selected
    * @param comp    the Comparator that defines the total order on T
    * @return        the maximum value in coll
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> T max(Collection<T> coll, Comparator<T> comp) {
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
      
      if(coll.size() == 0)
      {
         throw new NoSuchElementException("Error");
      }
      T max = null;
      for(T x : coll)
      {
         if(max == null)
         {
            max = x;
         }
         else
         {
            if(comp.compare(x, max) > 0)
            {
               max = x;
            }
         }
      }
      return max;
   }


   /**
    * Selects the kth minimum value from the Collection coll as defined by the
    * Comparator comp. If either coll or comp is null, this method throws an
    * IllegalArgumentException. If coll is empty or if there is no kth minimum
    * value, this method throws a NoSuchElementException. This method will not
    * change coll in any way.
    *
    * @param coll    the Collection from which the kth minimum is selected
    * @param k       the k-selection value
    * @param comp    the Comparator that defines the total order on T
    * @return        the kth minimum value in coll
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> T kmin(Collection<T> coll, int k, Comparator<T> comp) {
      ArrayList<T> arr = new ArrayList<T>(coll);
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
      if (coll.size() == 0 || coll.size() < k) {
         throw new NoSuchElementException("Error");
      }
      java.util.Collections.sort(arr, comp);
      T result = null; 
      int diff = 1;
      T temp = arr.get(0);
   
      if (k == 1) 
      {
         result = arr.get(0);
         return result;
      }
   
      for (int i=0; i < arr.size(); i++) 
      {
         if (arr.get(i) != temp) {
            diff++;
            if (diff == k)
            { 
               result = arr.get(i);
            }
         }
         temp = arr.get(i); 
      }
   
      if (diff < k || k < 1) {
         throw new NoSuchElementException("Error");
      }
   
      return result;
   
   
   }


   /**
    * Selects the kth maximum value from the Collection coll as defined by the
    * Comparator comp. If either coll or comp is null, this method throws an
    * IllegalArgumentException. If coll is empty or if there is no kth maximum
    * value, this method throws a NoSuchElementException. This method will not
    * change coll in any way.
    *
    * @param coll    the Collection from which the kth maximum is selected
    * @param k       the k-selection value
    * @param comp    the Comparator that defines the total order on T
    * @return        the kth maximum value in coll
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> T kmax(Collection<T> coll, int k, Comparator<T> comp) {
      ArrayList<T> arr = new ArrayList<T>(coll);
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
      if (coll.size() == 0 || coll.size() < k) {
         throw new NoSuchElementException("Error");
      }
      java.util.Collections.sort(arr, comp);
      T result = null; 
      int diff = 1;
      T temp = arr.get(arr.size()-1);
   
      if (k == 1) 
      {
         result = arr.get(arr.size()-1);
         return result;
      }
      
      for (int i = arr.size() - 1; i >= 0; i--) 
      {
         if (arr.get(i) != temp) 
         {
            diff++;
            if (diff == k) 
            {
               result = arr.get(i);
            }
         }
         temp = arr.get(i);
      }
   
      if (diff < k || k < 1) {
         throw new NoSuchElementException("Error");
      }
   
      return result;
   
   
      
   }


   /**
    * Returns a new Collection containing all the values in the Collection coll
    * that are greater than or equal to low and less than or equal to high, as
    * defined by the Comparator comp. The returned collection must contain only
    * these values and no others. The values low and high themselves do not have
    * to be in coll. Any duplicate values that are in coll must also be in the
    * returned Collection. If no values in coll fall into the specified range or
    * if coll is empty, this method throws a NoSuchElementException. If either
    * coll or comp is null, this method throws an IllegalArgumentException. This
    * method will not change coll in any way.
    *
    * @param coll    the Collection from which the range values are selected
    * @param low     the lower bound of the range
    * @param high    the upper bound of the range
    * @param comp    the Comparator that defines the total order on T
    * @return        a Collection of values between low and high
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> Collection<T> range(Collection<T> coll, T low, T high,
                                                     Comparator<T> comp) {
      ArrayList<T> result = new ArrayList<T>();
      
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
   
      if(coll.size() == 0)
      {
         throw new NoSuchElementException("Error");
      }
      
      for(T x : coll)
      {
         if ((comp.compare(x, low) >= 0) && (comp.compare(x, high) <= 0)) 
         {
            result.add(x);
         }
      }
      if(result.size() == 0)
      {
         throw new NoSuchElementException("Error");
      }
      return result;
   }


   /**
    * Returns the smallest value in the Collection coll that is greater than
    * or equal to key, as defined by the Comparator comp. The value of key
    * does not have to be in coll. If coll or comp is null, this method throws
    * an IllegalArgumentException. If coll is empty or if there is no
    * qualifying value, this method throws a NoSuchElementException. This
    * method will not change coll in any way.
    *
    * @param coll    the Collection from which the ceiling value is selected
    * @param key     the reference value
    * @param comp    the Comparator that defines the total order on T
    * @return        the ceiling value of key in coll
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> T ceiling(Collection<T> coll, T key, Comparator<T> comp) {
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
      if(coll.size() == 0)
      {
         throw new NoSuchElementException("Error");
      }
      int ex = 0;
      for(T x : coll)
      {
         if((comp.compare(x, key) >= 0))
         {
            ex++;
         }
      }
      if(ex == 0)
      {
         throw new NoSuchElementException("Error");
      }
      T result = coll.iterator().next();
      for(T x : coll)
      {
         if((comp.compare(x, key) >= 0) && (comp.compare(x, result) <= 0))
         {
            result = x;
         }
      }
      return result;
   }


   /**
    * Returns the largest value in the Collection coll that is less than
    * or equal to key, as defined by the Comparator comp. The value of key
    * does not have to be in coll. If coll or comp is null, this method throws
    * an IllegalArgumentException. If coll is empty or if there is no
    * qualifying value, this method throws a NoSuchElementException. This
    * method will not change coll in any way.
    *
    * @param coll    the Collection from which the floor value is selected
    * @param key     the reference value
    * @param comp    the Comparator that defines the total order on T
    * @return        the floor value of key in coll
    * @throws        IllegalArgumentException as per above
    * @throws        NoSuchElementException as per above
    */
   public static <T> T floor(Collection<T> coll, T key, Comparator<T> comp) {
      if(coll == null || comp == null)
      {
         throw new IllegalArgumentException("Error");
      }
      if(coll.size() == 0)
      {
         throw new NoSuchElementException("Error");
      }
      int ex = 0;
      for(T x : coll)
      {
         if((comp.compare(x, key) <= 0))
         {
            ex++;
         }
      }
      if(ex == 0)
      {
         throw new NoSuchElementException("Error");
      }
      T result = coll.iterator().next();
      for(T x : coll)
      {
         if((comp.compare(x, result) >= 0) && (comp.compare(x, key) <= 0))
         {
            result = x;
         }
      }
      return result;
   }

}