import java.util.Iterator;
import java.util.NoSuchElementException;

/**
 * Provides an implementation of the Set interface.
 * A doubly-linked list is used as the underlying data structure.
 * Although not required by the interface, this linked list is
 * maintained in ascending natural order. In those methods that
 * take a LinkedSet as a parameter, this order is used to increase
 * efficiency.
 *
 * @author Dean Hendrix (dh@auburn.edu)
 * @author Sujay Jakka (svj0007@auburn.edu)
 *
 */
public class LinkedSet<T extends Comparable<T>> implements Set<T> {

    //////////////////////////////////////////////////////////
    // Do not change the following three fields in any way. //
    //////////////////////////////////////////////////////////

    /** References to the first and last node of the list. */
   Node front;
   Node rear;

    /** The number of nodes in the list. */
   int size;

    /////////////////////////////////////////////////////////
    // Do not change the following constructor in any way. //
    /////////////////////////////////////////////////////////

    /**
     * Instantiates an empty LinkedSet.
     */
   public LinkedSet() {
      front = null;
      rear = null;
      size = 0;
   }


    //////////////////////////////////////////////////
    // Public interface and class-specific methods. //
    //////////////////////////////////////////////////

    ///////////////////////////////////////
    // DO NOT CHANGE THE TOSTRING METHOD //
    ///////////////////////////////////////
    /**
     * Return a string representation of this LinkedSet.
     *
     * @return a string representation of this LinkedSet
     */
   @Override
    public String toString() {
      if (isEmpty()) {
         return "[]";
      }
      StringBuilder result = new StringBuilder();
      result.append("[");
      for (T element : this) {
         result.append(element + ", ");
      }
      result.delete(result.length() - 2, result.length());
      result.append("]");
      return result.toString();
   }


    ///////////////////////////////////
    // DO NOT CHANGE THE SIZE METHOD //
    ///////////////////////////////////
    /**
     * Returns the current size of this collection.
     *
     * @return  the number of elements in this collection.
     */
   public int size() {
      return size;
   }

    //////////////////////////////////////
    // DO NOT CHANGE THE ISEMPTY METHOD //
    //////////////////////////////////////
    /**
     * Tests to see if this collection is empty.
     *
     * @return  true if this collection contains no elements, false otherwise.
     */
   public boolean isEmpty() {
      return (size == 0);
   }


    /**
     * Ensures the collection contains the specified element. Neither duplicate
     * nor null values are allowed. This method ensures that the elements in the
     * linked list are maintained in ascending natural order.
     *
     * @param  element  The element whose presence is to be ensured.
     * @return true if collection is changed, false otherwise.
     */
  
   public boolean add(T element) {
      Node n = new Node(element);
      Node current = front;
   
      if ((this.contains(element)) || (element == null)) {
         return false;
      }
   
      if (isEmpty()) {
         front = n;
         rear = n;
      }
      else if (front.element.compareTo(element) > 0) {
         n.next = front;
         front.prev = n;
         front = n;
      }
      else {
         rear.next = n;
         n.prev = rear;
         rear = n;
         if (n.prev.element.compareTo(element) > 0) {
            while (current != null) {
               if (current.element.compareTo(element) > 0) {
                  rear = n.prev;
                  current.prev.next = n;
                  n.next = current;
                  n.prev = current.prev;
                  current.prev = n;
                  rear.next = null;
                  break;
               }
               current = current.next;
            }
         }
      }
      size++;
      return true;
   }
   

    /**
     * Ensures the collection does not contain the specified element.
     * If the specified element is present, this method removes it
     * from the collection. This method, consistent with add, ensures
     * that the elements in the linked lists are maintained in ascending
     * natural order.
     *
     * @param   element  The element to be removed.
     * @return  true if collection is changed, false otherwise.
     */
     
   private Node locate(T element) {
      Node n = front;
      while (n != null) {
         if (n.element.equals(element)) {
            return n;
         }
         n = n.next;
      }
      return null;
   }
   
   
   public boolean remove(T element) {
      Node n = locate(element);
      if (isEmpty() || n == null) {
         return false;
      }
      else {
         if (n.element == front.element && size() == 1) {
            front = null;
            rear = null;
            size--;
         }
         else if (n.element == front.element && size() > 1) {
            front = front.next;
            front.prev = null;
            size--;
            return true;
         }
         else {
            n.prev.next = n.next;
            if (n.next == null) {
               rear = n.prev;
               n.prev.next = null;
            }
            else {
               n.next.prev = n.prev;
            }
            size--;
            return true;
         }
      }
      return true;
   }


    /**
     * Searches for specified element in this collection.
     *
     * @param   element  The element whose presence in this collection is to be tested.
     * @return  true if this collection contains the specified element, false otherwise.
     */
   public boolean contains(T element) {
      if (isEmpty()) {
         return false;
      }
   
      if (front == null) {
         return false;
      }
   
      Node n = front;
   
      while (n != null) {
         if (n.element.equals(element)) {
            return true;
         }
         n = n.next;
      }
   
      return false;
   }


    /**
     * Tests for equality between this set and the parameter set.
     * Returns true if this set contains exactly the same elements
     * as the parameter set, regardless of order.
     *
     * @return  true if this set contains exactly the same elements as
     *               the parameter set, false otherwise
     */
   public boolean equals(Set<T> s) {
      if(size == s.size() && complement(s).size() == 0) {
         return true;
      }
      return false;
   }


    /**
     * Tests for equality between this set and the parameter set.
     * Returns true if this set contains exactly the same elements
     * as the parameter set, regardless of order.
     *
     * @return  true if this set contains exactly the same elements as
     *               the parameter set, false otherwise
     */
   public boolean equals(LinkedSet<T> s) {
      if(size == s.size() && complement(s).size() == 0) {
         return true;
      }
      return false;
   }


    /**
     * Returns a set that is the union of this set and the parameter set.
     *
     * @return  a set that contains all the elements of this set and the parameter set
     */
   public Set<T> union(Set<T> s){
      if(s == null) {
         throw new NullPointerException();
      }
   
      LinkedSet<T> setReturn = new LinkedSet<T>();
   
      Node t = front;
   
      while(t != null) {
         setReturn.add(t.element);
         t = t.next;
      }
   
      Iterator<T> i = s.iterator();
   
      while(i.hasNext()) {
         setReturn.add(i.next());
      }
   
      return setReturn;
   }


    /**
     * Returns a set that is the union of this set and the parameter set.
     *
     * @return  a set that contains all the elements of this set and the parameter set
     */
   public Set<T> union(LinkedSet<T> s){
      return null;
   }


    /**
     * Returns a set that is the intersection of this set and the parameter set.
     *
     * @return  a set that contains elements that are in both this set and the parameter set
     */
   public Set<T> intersection(Set<T> s) {
      if(s == null) {
         throw new NullPointerException();
      }
   
      LinkedSet<T> setReturn = new LinkedSet<T>();
   
      Node t = front;
   
      while(t != null) {
         if(s.contains((T)t.element)) {
            setReturn.add((T)t.element);
         }
      
         t = t.next;
      }
   
      return setReturn;
   }

    /**
     * Returns a set that is the intersection of this set and
     * the parameter set.
     *
     * @return  a set that contains elements that are in both
     *            this set and the parameter set
     */
   public Set<T> intersection(LinkedSet<T> s) {
      if(s == null) {
         throw new NullPointerException();
      }
   
      LinkedSet<T> setReturn = new LinkedSet<T>();
   
      Node t = front;
   
      while(t != null) {
         if(s.contains((T)t.element)) {
            setReturn.add((T)t.element);
         }
      
         t = t.next;
      }
   
      return setReturn;
   }


    /**
     * Returns a set that is the complement of this set and the parameter set.
     *
     * @return  a set that contains elements that are in this set but not the parameter set
     */
   public Set<T> complement(Set<T> s) {
      if(s == null) {
         throw new NullPointerException();
      }
      LinkedSet<T> setReturn = new LinkedSet<T>();
   
      Node t = front;
   
      while(t != null) {
         if(!s.contains((T)t.element)) {
            setReturn.add((T)t.element);
         }
      
         t = t.next;
      }
   
      return setReturn;
   }


    /**
     * Returns a set that is the complement of this set and
     * the parameter set.
     *
     * @return  a set that contains elements that are in this
     *            set but not the parameter set
     */
   public Set<T> complement(LinkedSet<T> s) {
      if(s == null) {
         throw new NullPointerException();
      }
   
      LinkedSet<T> setReturn = new LinkedSet<T>();
   
      Node t = front;
   
      while(t != null) {
         if(!s.contains((T)t.element)) {
            setReturn.add((T)t.element);
         }
      
         t = t.next;
      }
   
      return setReturn;
   }


    /**
     * Returns an iterator over the elements in this LinkedSet.
     * Elements are returned in ascending natural order.
     *
     * @return  an iterator over the elements in this LinkedSet
     */
   public Iterator<T> iterator() {
      return new LinkedIterator();
   }
   
   private class LinkedIterator implements Iterator<T> {
      private Node current = front;
   
      public boolean hasNext() {
         return current != null;
      }
      public T next() {
         if (!hasNext())
            throw new NoSuchElementException();
      
         T result = current.element;
         current = current.next;
         return result;
      }
      public void remove() {
         throw new UnsupportedOperationException();
      }
   }


    /**
     * Returns an iterator over the elements in this LinkedSet.
     * Elements are returned in descending natural order.
     *
     * @return  an iterator over the elements in this LinkedSet
     */
   public Iterator<T> descendingIterator() {
      return new descendingtIterator(rear);
   }
   
   private class descendingtIterator implements Iterator<T> {
      Node t;
      public descendingtIterator(Node rear) {
         t = rear;
      }
   
      public boolean hasNext() {
         return t != null && t.element != null;
      }
   
      public T next() {
         if(t != null) {
            T r = t.element;
            t = t.prev;
            return r;
         }
         return null;
      }
   
      public void remove() {
         throw new UnsupportedOperationException();
      }
   
   }


    /**
     * Returns an iterator over the members of the power set
     * of this LinkedSet. No specific order can be assumed.
     *
     * @return  an iterator over members of the power set
     */
   public Iterator<Set<T>> powerSetIterator() {
      return new powerIterator(front,size);
   }
   
   private class powerIterator implements Iterator<Set<T>> {
      private Node current;
      private int size;
      private int count;
   
      public powerIterator(Node rear,int size) {
         current = rear;
         size = size;
         count = 0;
      }
   
      public boolean hasNext() {
         if (count == 0) {
            return true;
         }
         return ((count < (int) Math.pow(2,size)) && (current != null));
      }
   
      public Set<T> next() {
         if (!hasNext()) {
            throw new NoSuchElementException();
         }
         Set<T> result = new LinkedSet<T>();
         if (count == 0) {
            count++;
            return result;
         }
         String binary = Integer.toBinaryString(count);
         for (int i = binary.length() - 1; i >= 0; i--) {
            if (binary.charAt(i) == '1') {
               result.add(current.element);
            }
            current = current.prev;
         }
         count++;
         current = rear;
         return result;
      }      
      public void remove() {
         throw new UnsupportedOperationException();
      }
   }



    //////////////////////////////
    // Private utility methods. //
    //////////////////////////////

    // Feel free to add as many private methods as you need.

    ////////////////////
    // Nested classes //
    ////////////////////

    //////////////////////////////////////////////
    // DO NOT CHANGE THE NODE CLASS IN ANY WAY. //
    //////////////////////////////////////////////

    /**
     * Defines a node class for a doubly-linked list.
     */
   class Node {
        /** the value stored in this node. */
      T element;
        /** a reference to the node after this node. */
      Node next;
        /** a reference to the node before this node. */
      Node prev;
   
        /**
         * Instantiate an empty node.
         */
      public Node() {
         element = null;
         next = null;
         prev = null;
      }
   
        /**
         * Instantiate a node that containts element
         * and with no node before or after it.
         */
      public Node(T e) {
         element = e;
         next = null;
         prev = null;
      }
   }

}