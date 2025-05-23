# Name: Patricia (Trish) Stackpole
# OSU Email: stackpop@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 12/05/2024
# Description: Student implementation of a HashMap. Using Dynamic Arrays
# as "buckets" containing Linked Lists as underlying data structure.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Checks load factor to determine if table needs to be resized.
        Inserts or updates value at key
        """

        # Check load factor, resize table if needed
        if self.table_load() >= 1:
            self.resize_table(self.get_capacity() * 2)

        # Hash the key
        hash_index = self._hash_function(key) % self._capacity
        linked_list = self._buckets.get_at_index(hash_index)
        node = linked_list.contains(key)
        if node:
            # If the key exists, update its value
            node.value = value
        else:
            # If the key does not exist, insert a new node with the key-value pair
            linked_list.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes table (adds more buckets), but only to a prime number
        """

        # Check if new_capacity is valid and ensure it is prime
        if new_capacity < 1:
            return

        if self._is_prime(new_capacity) == False:
            new_capacity = self._next_prime(new_capacity)

        # Use get_keys_and_values to get all key-value pairs
        key_value_pairs = self.get_keys_and_values()

        for i in range(key_value_pairs.length()):
            if i == new_capacity:
                new_capacity = self._next_prime(new_capacity * 2)

        # Initialize new table using dynamic array as underlying data structure
        new_table = DynamicArray()
        for _ in range(new_capacity):
            new_table.append(LinkedList())

        # Rehash and insert each key-value pair into the new table
        for i in range(key_value_pairs.length()):
            key, value = key_value_pairs.get_at_index(i)
            new_hash_index = self._hash_function(key) % new_capacity
            new_list = new_table.get_at_index(new_hash_index)
            new_list.insert(key, value)

        # Replace current buckets with new table and update capacity
        self._capacity = new_capacity
        self._buckets = new_table

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of our table
        Load factor = total number of elements in the table/number of buckets
        """

        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets, checks each bucket to see if
        its corresponding LinkedList has a head. If not, it adds to the
        count of empty buckets.
        """

        empty_count = 0

        for i in range(self._capacity):
            if self._buckets.get_at_index(i)._head is None:
                empty_count += 1

        return empty_count

    def get(self, key: str):
        """
        Returns the value of a given key, or None. Method will hash the key,
        find the entry at the index of the key, return the value.
        """

        # Hash the key
        hash_index = self._hash_function(key) % self._capacity
        # Look for key in the linked list
        linked_list = self._buckets.get_at_index(hash_index)
        node = linked_list.contains(key)

        # Return None if the key is not found
        if node: return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method will hash the key, find the entry at the index of the key,
        return True or False, depending if the key is present.
        """

        # Hash the key
        hash_index = self._hash_function(key) % self._capacity
        # Look for key in the linked list
        linked_list = self._buckets.get_at_index(hash_index)
        node = linked_list.contains(key)

        # Return None if the key is not found
        if node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes a key and value from the hash map. Hashes the value, searches
        the LinkedList in the bucket corresponding to the hashed key. Erases
        the link between the deleted key and the next/previous node.
        """

        # Hash the key to find the bucket
        hash_index = self._hash_function(key) % self._capacity
        # Look for key in the linked list
        linked_list = self._buckets.get_at_index(hash_index)
        # Abandon method if bucket doesn't exist/is Empty
        if linked_list is None: return
        cur = linked_list._head
        prev = None

        # Look through LinkedList for key
        while cur is not None:
            if cur.key == key:
                if prev is None:
                    linked_list._head = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return
            prev = cur
            cur = cur.next

        # Return if not found
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a DynamicArray containing all key-value pairs as tuples.
        """

        ret_arr = DynamicArray()

        # Iterates through each linked list in each bucket and
        # appends key-value pairs to our return array
        for i in range(self._capacity):
            current_list = self._buckets.get_at_index(i)
            if current_list is not None:
                current_node = current_list._head
                while current_node is not None:
                    ret_arr.append((current_node.key, current_node.value))
                    current_node = current_node.next

        return ret_arr

    def clear(self) -> None:
        """
        Empty our hash map. Set the head of each linked list
        in each bucket to None
        """

        # Iterates through each bucket, but not the entire linked-list
        # Sets head to None, thereby breaking the links in our lined-list
        # and emptying the bucket
        for i in range(self._capacity):
            linked_list = self._buckets[i]
            linked_list.head = None
            linked_list._size = 0

        self._size = 0

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Assigns array values as the keys to a hash map, with the initial
    value set to 1. If a duplicate is found, it increases the value by 1.
    The for loop keeps track of which values are the highest (the mode), and
    returns those in an array
    """

    map = HashMap()
    ret_arr = DynamicArray()
    count = 0

    for i in range(0, da.length()):
        # Checks if value we are adding to hash map already exists,
        # If not, value (which is also the count) is set to 1.
        if map.get(da.get_at_index(i)) == None:
            value = 1
        # Increases the value in the key/value pair by one
        else:
            value = map.get(da.get_at_index(i))
            value += 1  # Increment the value by 1
        # Adds to map or updates value
        map.put(da.get_at_index(i),value)
        if value == count:
            ret_arr.append(da.get_at_index(i))
        if value > count:
            # Clears array if new highest value is found
            ret_arr = DynamicArray()
            ret_arr.append(da.get_at_index(i))
            count = value

    return (ret_arr, count)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
