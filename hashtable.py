
class KeyNotFound(Exception):
    """Exception raised when a key is not found in the hashtable.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class KeyAlreadyExists(Exception):
    """Exception raised when a key already exists in the hashtable.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class KeyNotModifiable(Exception):
    """Exception raised when a key is tried to modify.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Entry:
    """
    Object storage in hash table.
    """

    def __init__(self, kw:str, **values):
        """
        Args
        ----
            kw (str): Identifier
        
        Kwargs
        ------
            values: Data to store.
        """

        self.kw = kw
        self.values = {key: value for key, value in values.items()}

        # Used to store a reference to the next object if the index of the hashtable is taken.
        self.next_node = None

    def __eq__(self, other) -> bool:
        """Compare two elements.
        
        if other is a string only self.kw will be compared, else
        the hash of the object.
        """

        if isinstance(other, str):
            equal = self.kw == other
            if equal:
                return True
            return False
        
        if isinstance(other, Entry):
            equal = hash(self) == hash(other)
            if equal:
                return True
            return False
        
        return NotImplemented
    
    def __iter__(self):
        """Iterate over the values.
        """

        current = self

        while current:
            yield current
            current = current.next_node

    def __len__(self):
        """Return the length of the values.
        """

        curr = self.next_node
        i = 1
        while curr:
            i += 1
            curr = curr.next_node

        return i
    
    def append(self, new_entry):
        """Append a new entry to the end of the linked list.

        Args
        ----
            new_entry (Entry): Entry to append.

        Raises
        ------
            KeyAlreadyExists: If the key already exists.
        """

        current = self

        while current.next_node:
            current = current.next_node

            if current.kw == new_entry.kw:
                raise KeyAlreadyExists(f"{new_entry} already exists!")
            

        current.next_node = new_entry

    def __str__(self):
        return f"{self.kw}"

class hashtable:
    """
    Hash table! 
    ------

    Store values in a dictionary like style in a fixed size data type!
    """
    def __init__(self, max_length, **kwargs):
        """
        Args
        ----
            max_length (int): The lenght that will be avaliable to the hashtable (not changable!)
        
        Kwargs
        -----
            hash (callable): Specify another hash function to use.
        """

        self.max_length = max_length

        self.entries = [None for _ in range(len(self))]
        
        self.hash = kwargs.get("hash", self.__default_hash)

    def __getitem__(self, index):
        """Get item at index.
        """

        if isinstance(index, int):
            return self.entries[index]
        if isinstance(index, str):
            return self.find(index)

    def __setitem__(self, kw, data):
        """Either modify or insert data.

        Args
        ----
            kw (str): Identifier
            data (dict): Data to store.
        
        Raises
        ------
            TypeError: If kw is not a string.
        """

        if self.modify_data(kw, **data):
            return
        
        if isinstance(kw, str):
            self.insert(kw, **data)

        raise TypeError("kw must be a string!")

    def __delitem__(self, kw):
        """Delete entry of kw.
        """

        self.remove(kw)
        
    def __iter__(self):
        """Iterate over the hashtable.
        """

        for entry in self.entries:
            yield entry

    def __reversed__(self):
        """Iterate over the hashtable in reverse.
        """

        for entry in reversed(self.entries):
            if isinstance(entry, Entry):
                yield entry

    def __contains__(self, kw) -> bool:
        """Check if kw is in the hashtable.
        """

        try:
            self.find(kw)
        except KeyNotFound:
            return False
        else:
            return True
        
    def __len__(self) -> int:
        """Return the length of the hashtable.
        """

        return self.max_length

    def __entry_exists_at_index(self, index) -> bool:
        """Check if entry exist at index.
        """

        entry = self[index]
        if isinstance(entry, Entry):
            return True
        return False

    def __default_hash(self, kw:str) -> int:
        
        map_to_range = lambda x: x % len(self)
        index = map_to_range(hash(kw))
        return index
    
    def __modify_data(self, kw, **data) -> bool:
        """Modify data of an entry.
        
        Args
        ----
            kw (str): Identifier.

        Kwargs
        -----
            data: The data which will attach to the kw.

        Returns
        -------
            bool: True if the data was modified, else False.
        """
        
        try:
            entry = self.find(kw)
        except KeyNotFound as e:
            return False
        else:
            entry.values.update(**data)
        return True
    
    def keys(self) -> list:
        """Return a list of all keys.
        """

        names = []
        for entry in self:
            if isinstance(entry, Entry):
                for e in entry:
                    names.append(e.kw)                
        return names
    
    def values(self) -> list:
        """Return a list of all values.
        """

        values = []
        for entry in self:
            if isinstance(entry, Entry):
                for e in entry:
                    values.append(e.values)
        return values
    
    def items(self) -> list:
        """Return a list of all items.
        """

        items = []
        for entry in self:
            if isinstance(entry, Entry):
                for e in entry:
                    items.append((e.kw, e.values))
        return items

    def insert(self, kw, **data):
        """Insert a new key value pair.
        
        Args
        ----
            kw (str): Identifier.

        Kwargs
        -----
            data: The data which will attach to the kw.

        Raises
        ------
            KeyError: If the keyword already exists.
        """

        new_entry = Entry(kw, **data)

        # Get the hash of the new keyword.
        index = self.hash(kw)
        
        # The simplest case:
        # There does not already exist anything
        # at the calculated index -> assign new
        # entry.

        entry_exist = isinstance(self[index], Entry)

        if not entry_exist:
            
            # Assign
            # Must set entries[index] to new_entry, not self[index], 
            # because self[index] will call this method again.
            self.entries[index] = new_entry
            return

        # When the hash fails...
        # (This is a linked list)
        # Append the new entry to the end of the linked list.

        self[index].append(new_entry)


    def find(self, kw:str) -> Entry:
        """Find and return the entry from the keyword.
        
        args
        ----
            kw (str): Identifier.
        
        Returns
        -------
            Entry: The Entry object with the data
                   of the kw.
        
        Raises
        ------
            KeyNotFound: If the keyword does not exist.
        """

        index = self.hash(kw)

        current_contender = self[index]
        
        # (Simple case)
        if current_contender == kw:
            return current_contender
        
        # (If hash has failed)
        for contender in self[index]:

            if contender == kw:
                return contender

        raise KeyNotFound(f"{kw} not found.")
    
    def remove(self, kw:str) -> Entry:
        """Remove the entry with the given keyword.
        
        Args
        ----
            kw (str): Identifier.

        Returns
        -------
            Entry: The Entry object with the data
                   of the kw.

        Raises
        ------
            KeyNotFound: If the keyword does not exist.
        """

        # Get hash
        index = self.hash(kw)

        first_entry = self[index]

        # (Simple case)
        if first_entry == kw:

            # Remove
            # Must set entries[index] to None, not self[index], 
            # because self[index] will call insert method.
            self.entries[index] = first_entry.next_node
            return first_entry

        # (If hash has failed)
        for contender in first_entry:

            if contender.next_node != kw:
                continue

            # Store the entry to remove in temporary variable.
            to_remove = contender.next_node

            # Point the next node to remove-entry's next node.
            contender.next_node = to_remove.next_node

            # pop
            return to_remove
            
        # Not found.
        raise KeyError(f"{kw} not found.")
    
    def __get_longest_kw(self) -> int:
        """Get the longest keyword in the hashtable.
        """

        longest = 0
        for e in self:
            if (not e):
                continue

            longest = max(0, len(e.kw))

            for linked_e in e:
                longest = max(0, len(linked_e.kw))

        return longest

    def __str__(self) -> str:
        l = self.__get_longest_kw()

        out = "Hashtable(\n"

        for i, e in enumerate(self):

            e_fmt = f"{e}" if e else ""
            out += f"\t{i} --- {e_fmt:^{l+2}}"

            if (not e):
                out += "\n"
                continue

            for j, linked_e in enumerate(e):
                if j == 0:
                    continue

                e_fmt = f"{linked_e}"
                out += f" --- {e_fmt:^{l+2}}"

            out += "\n"
        out += ")"

        return out