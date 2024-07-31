import java.util.Arrays;
import java.util.Comparator;

/**
 * Binary search.
 */
public class BinarySearch {

    /**
     * Returns the index of the first key in a[] that equals the search key, 
     * or -1 if no such key exists. This method throws a NullPointerException
     * if any parameter is null.
     */
   public static <Key> int firstIndexOf(Key[] a, Key key, Comparator<Key> comparator) {
      if(a == null)
      {
         throw new NullPointerException("Array is null");
      }
           
      if(key == null)
      {
         throw new NullPointerException("Key is null");
      }
           
      if(comparator == null)
      {
         throw new NullPointerException("Comparator is null");
      }
           
      int low = 0;
      int high = a.length - 1;
      if(comparator.compare(a[0], key) == 0)
      {
         return 0;
      }
      while (low <= high)
      {
         int mid = low + (high-low) / 2;
         if(comparator.compare(key, a[mid]) < 0)
         {
            high = mid - 1;
         }
               
         else if(comparator.compare(key, a[mid]) > 0)
         {
            low = mid + 1;
         }
               
         else if(comparator.compare(a[mid-1], a[mid]) == 0)
         {
            high = mid - 1;
         }
         else
         {
            return mid;
         }
           
      }
      return -1;
           
   
   }

    /**
     * Returns the index of the last key in a[] that equals the search key, 
     * or -1 if no such key exists. This method throws a NullPointerException
     * if any parameter is null.
     */
   public static <Key> int lastIndexOf(Key[] a, Key key, Comparator<Key> comparator) {
      if(a == null)
      {
         throw new NullPointerException("Array is null");
      }
           
      if(key == null)
      {
         throw new NullPointerException("Key is null");
      }
           
      if(comparator == null)
      {
         throw new NullPointerException("Comparator is null");
      }
           
      int low = 0;
      int high = a.length - 1;
      if(comparator.compare(a[high], key) == 0)
      {
         return high;
      }
      while (low <= high)
      {
         int mid = low + (high-low) / 2;
         if(comparator.compare(key, a[mid]) < 0)
         {
            high = mid - 1;
         }
               
         else if(comparator.compare(key, a[mid]) > 0)
         {
            low = mid + 1;
         }
               
         else if(comparator.compare(a[mid], a[mid + 1]) == 0)
         {
            low = mid + 1;
         }
         else
         {
            return mid;
         }
           
      }
      return -1;
   }

}
