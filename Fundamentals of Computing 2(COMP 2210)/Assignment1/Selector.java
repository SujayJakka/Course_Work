import java.util.Arrays;

/**
* Defines a library of selection methods
* on arrays of ints.
*
* @author   Sujay Jakka (svj0007@auburn.edu)
* @author   Dean Hendrix (dh@auburn.edu)
* @version  1/30/2022
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
    * Selects the minimum value from the array a. This method
    * throws IllegalArgumentException if a is null or has zero
    * length. The array a is not changed by this method.
    */
   public static int min(int[] a) 
   {
      if(a == null || a.length == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int min = a[0];
      for(int num : a)
      {
         if(num < min)
         {
            min = num;
         }
      }
      return min;
      
   }


   /**
    * Selects the maximum value from the array a. This method
    * throws IllegalArgumentException if a is null or has zero
    * length. The array a is not changed by this method.
    */
   public static int max(int[] a) {
      if(a == null || a.length == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int max = a[0];
      for(int num : a)
      {
         if(num > max)
         {
            max = num;
         }
      }
      return max;
      
   }


   /**
    * Selects the kth minimum value from the array a. This method
    * throws IllegalArgumentException if a is null, has zero length,
    * or if there is no kth minimum value. Note that there is no kth
    * minimum value if k < 1, k > a.length, or if k is larger than
    * the number of distinct values in the array. The array a is not
    * changed by this method.
    */
   public static int kmin(int[] a, int k) {
      if (a == null || a.length == 0 || k > a.length || k < 1) 
      {
         throw new IllegalArgumentException("Error");
      }
   
      int[] a2 = Arrays.copyOf(a, a.length);
      Arrays.sort(a2);
      int result = 0; 
      int diff = 1;
      int comp = a[0];
   
      if (k == 1) 
      {
         result = a2[0];
         return result;
      }
   
      for (int i=0; i < a2.length; i++) 
      {
         if (a2[i] != comp) {
            diff++;
            if (diff == k)
            { 
               result = a2[i];
            }
         }
         comp = a2[i]; 
      }
   
      if (diff < k) {
         throw new IllegalArgumentException("Error");
      }
   
      return result;
   }


   /**
    * Selects the kth maximum value from the array a. This method
    * throws IllegalArgumentException if a is null, has zero length,
    * or if there is no kth maximum value. Note that there is no kth
    * maximum value if k < 1, k > a.length, or if k is larger than
    * the number of distinct values in the array. The array a is not
    * changed by this method.
    */
   public static int kmax(int[] a, int k) {
      if (a == null || a.length == 0 || k > a.length || k < 1)
      {
         throw new IllegalArgumentException("Error");
      }
      
      int[] a2 = Arrays.copyOf(a, a.length);
      Arrays.sort(a2);
      int result = 0; 
      int diff = 1;
      int comp = a2[a2.length - 1];
   
      if (k == 1) 
      {
         result = a2[a2.length - 1];
         return result;
      }
      
      for (int i = a2.length - 1; i >= 0; i--) 
      {
         if (a2[i] != comp) 
         {
            diff++;
            if (diff == k) 
            {
               result = a2[i];
            }
         }
         comp = a2[i];
      }
   
      if (diff < k) 
      {
         throw new IllegalArgumentException("Error");
      }
      return result;
   
   }


   /**
    * Returns an array containing all the values in a in the
    * range [low..high]; that is, all the values that are greater
    * than or equal to low and less than or equal to high,
    * including duplicate values. The length of the returned array
    * is the same as the number of values in the range [low..high].
    * If there are no qualifying values, this method returns a
    * zero-length array. Note that low and high do not have
    * to be actual values in a. This method throws an
    * IllegalArgumentException if a is null or has zero length.
    * The array a is not changed by this method.
    */
   public static int[] range(int[] a, int low, int high) {
      if(a == null || a.length == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int size = 0;
      for (int num : a) 
      {
         if (low <= num && num <= high ) 
         {
            size++;
         }
      }
      int[] result = new int[size];
      if(size == 0)
      {
         return result;
      }
      int i = 0;
      for(int num: a)
      {
         if (low <= num && num <= high) 
         {
            result[i] = num;
            i++;
         }
      }
      return result;
   }


   /**
    * Returns the smallest value in a that is greater than or equal to
    * the given key. This method throws an IllegalArgumentException if
    * a is null or has zero length, or if there is no qualifying
    * value. Note that key does not have to be an actual value in a.
    * The array a is not changed by this method.
    */
   public static int ceiling(int[] a, int key) {
      if(a == null || a.length == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int ex = 0;
      for(int num : a)
      {
         if(num >= key)
         {
            ex++;
         }
      }
      if(ex == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int result = 10000000;
      for(int num : a)
      {
         if(num >= key && num<=result)
         {
            result = num;
         }
      }
      return result;
   }


   /**
    * Returns the largest value in a that is less than or equal to
    * the given key. This method throws an IllegalArgumentException if
    * a is null or has zero length, or if there is no qualifying
    * value. Note that key does not have to be an actual value in a.
    * The array a is not changed by this method.
    */
   public static int floor(int[] a, int key) {
      if(a == null || a.length == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int ex = 0;
      for(int num : a)
      {
         if(num <= key)
         {
            ex++;
         }
      }
      if(ex == 0)
      {
         throw new IllegalArgumentException("Error");
      }
      int result = -10000000;
      for(int num : a)
      {
         if(num <= key && num>=result)
         {
            result = num;
         }
      }
      return result;
   }
}
