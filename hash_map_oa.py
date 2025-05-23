# Name: Patricia (Trish) Stackpole
# OSU Email: stackpop@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 12/05/2024
# Description: Student implementation of a HashMap using dynamic arrays as the
# underlying data structure. Implementation uses open addressing with quadratic
# probing to perform hash calculations.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the
        given key is not in the hash map, a new key/value pair is added.
        """

        # Check load factor, resize table if needed
        if self.table_load() >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        index = 0
        while index < self._capacity:
            # Hash the key (Quadratic probing)
            hash_index = (self._hash_function(key) + (index ** 2)) % self._capacity
            # If keys match at hashed index or there is a tombstone
            element = self._buckets.get_at_index(hash_index)
            if element is None or element.is_tombstone:
                # Insert new element in blank space
                # HashEntry() sets tombstone to False by default
                new_element = HashEntry(key, value)
                self._buckets.set_at_index(hash_index, new_element)
                self._size += 1
                return
            elif element.key == key:
                # Update existing element
                element.value = value
                element.is_tombstone = False
                return
            # if the hashed index is empty or the key doesn't match,
            # the index is incremented, and we probe for the next available space
            index = index + 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Updates the capacity of the underlying table. All key/pair values are
        rehashed and copied to the new table.
        """

        # Check if new_capacity is valid and ensure it is prime
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Save the old table data
        old_buckets = self._buckets
        old_capacity = self._capacity

        # Initialize new table using dynamic array as underlying data structure
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)
        self._capacity = new_capacity
        self._size = 0  # Reset size and re-add the elements to count correctly

        # Rehash and insert each key-value pair into the new table using put method
        for i in range(old_capacity):
            element = old_buckets.get_at_index(i)
            if element is not None:
                self.put(element.key, element.value)
                if element.is_tombstone:
                    self._size += 1


    def table_load(self) -> float:
        """
        Calculates and returns the load factor of our table
        Load factor = total number of elements in the table/number of buckets
        """

        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets. In the hash_map_sc implementation,
        this was how many buckets did not contain a linked list. In our open
        addressing implementation, each bucket contains at most one value, not
        an entire linked list. So empty buckets will be capacity - size.
        """

        return self.get_capacity() - self.get_size()

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the
        hash map, the method returns None.
        """

        # Prevents iteration if map is empty
        if self._size == 0:
            return None

        index = 0
        while index != self._capacity:
            # Hash the key
            hash_index = (self._hash_function(key) + (index ** 2)) % self._capacity
            # If keys match at hashed index
            if self._buckets.get_at_index(hash_index) != None:
                element = self._buckets.get_at_index(hash_index)
                if key == element.key and element.is_tombstone == False:
                   return element.value
            # if the hashed index is empty and the keys don't match:
            index = index + 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """

        # Prevents iteration if map is empty
        if self._size == 0:
            return False

        index = 0
        while index != self._capacity:
            # Hash the key
            hash_index = (self._hash_function(key) + (index ** 2)) % self._capacity
            # If keys match at hashed index
            if self._buckets.get_at_index(hash_index) != None:
                element = self._buckets.get_at_index(hash_index)
                if key == element.key:
                    return True
            index = index + 1

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key
        is not in the hash map.
        """

        # Prevents iteration if map is empty
        if self._size == 0:
            return None

        index = 0
        while index != self._capacity:
            # Hash the key
            hash_index = (self._hash_function(key) + (index ** 2)) % self._capacity
            # If keys match at hashed index
            if self._buckets.get_at_index(hash_index) != None:
                element = self._buckets.get_at_index(hash_index)
                if key == element.key:
                    if element.is_tombstone == False:
                        element.is_tombstone = True
                        self._size -=1
                    return None
            index = index + 1
        return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.
        """

        ret_arr = DynamicArray()
        # Prevents iteration if map is empty
        if self._size == 0:
            return ret_arr

        # Iterates through each bucket and
        # appends key-value pairs to our return array
        for i in range(self._capacity):
            if self._buckets.get_at_index(i) != None:
                element =self._buckets.get_at_index(i)
                if element is not None and element.is_tombstone == False:
                    ret_arr.append((element.key, element.value))

        return ret_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash
        table capacity.
        """

        cleared_map = DynamicArray()
        cleared_cap = self.get_capacity()

        for _ in range(cleared_cap):
            cleared_map.append(None)

        self._buckets = cleared_map
        self._capacity = cleared_cap
        self._size = 0

    def __iter__(self):
        """
        Initializes the iterator as a private data member. Enables the hash map
        to iterate across itself.
        """

        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of the
        iterator.
        """

        while self._index < self._capacity:
            try:
                ret_value = self._buckets[self._index]
                self._index = self._index + 1
                if ret_value is not None:
                    return ret_value
            except DynamicArray:
                raise StopIteration

        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":




    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(5, hash_function_1)
    for i in range(2):
        m.put('str' + str(i), i * 100)
    m.resize_table(7)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))



    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")


        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
        


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
