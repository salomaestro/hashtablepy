
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
            return True if self.kw == other else False
        if isinstance(other, Entry):
            return True if hash(self) == hash(other) else False

    def __str__(self):
        return f"{self.kw}"

class Hashtable:
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
        self.entries = [None for i in range(max_length)]
        self.hash = kwargs.get("hash", self.__default_hash)

    def __exist_entry(self, index) -> bool:
        """Check if entry exist at index.
        """

        if isinstance(self.entries[index], Entry):
            return True
        return False

    def __default_hash(self, kw:str, max_length:int) -> int:
        # return len(kw) ** 5 % max_length
        return hash(kw) % max_length # The modulo will map hash between 0 to max_length.

    def insert(self, kw, **data):
        """Insert a new key value pair.
        
        Args
        ----
            kw (str): Identifier.
        Kwargs
        -----
            data: The data which will attach to the kw.
        """

        # init a new entry object
        new = Entry(kw, **data)

        # Get the hash of the new keyword.
        index = self.hash(kw, self.max_length)
        
        # The simplest case:
        # There does not already exist anything
        # at the calculated index -> assign new
        # entry.
        if not self.__exist_entry(index):
            self.entries[index] = new
            return

        # When the hash fails...
        
        # Get the entry that has the same hash
        same_hash = self.entries[index]

        # Iterate until it does not anymore have a next_node
        while (not same_hash.next_node is None):
            same_hash = same_hash.next_node

        # Assign the new entry as the next_node of the
        # element that previously was the last element.
        same_hash.next_node = new

    def find(self, kw:str) -> Entry:
        """Find and return the entry from the keyword.
        
        args
        ----
            kw (str): Identifier.
        
        Returns
        -------
            Entry: The Entry object with the data
                   of the kw.
        """

        # Get the hash
        index = self.hash(kw, self.max_length)

        # Find a first contender.
        contender = self.entries[index]
        
        # (Simple case)
        # This will compare if the kw (str) is equal 
        # to the contender.kw (str).
        if contender == kw:
            return contender
        
        # (If hash has failed)
        # Iterate over all nodes at hash location
        # and return if match is found.
        while (contender.next_node):
            contender = contender.next_node

            if contender == kw:
                return contender
        
        # If not found.
        raise KeyError(f"{kw} not found.")
    
    def remove(self, kw:str) -> Entry:
        """Remove the entry with the given keyword.
        
        Args
        ----
            kw (str): Identifier.

        Returns
        -------
            Entry: The Entry object with the data
                   of the kw.
        """

        # Get hash
        index = self.hash(kw, self.max_length)

        contender = self.entries[index]

        # (Simple case)
        # Compare if match
        if contender == kw:

            # If match then set the first Entry of the entries
            # lsit to be the match's next node.
            self.entries[index] = contender.next_node
            return contender

        # (If hash has failed)
        # Iterate as long as next node exist.
        while (contender.next_node):
            
            # If match
            if contender.next_node == kw:

                # Store the entry to remove in temporary variable.
                to_remove = contender.next_node

                # Point the next node to remove-entry's next node.
                contender.next_node = to_remove.next_node

                # pop
                return to_remove
            
            # Update
            contender = contender.next_node
        
        # Not found.
        raise KeyError(f"{kw} not found.")
    
    def __get_longest_kw(self) -> int:
        longest = 0
        for e in self.entries:
            if (not e):
                continue

            longest = max(0, len(e.kw))

            while (e.next_node):
                longest = max(0, len(e.kw))
                e = e.next_node
        return longest

    def __str__(self) -> str:
        l = self.__get_longest_kw()

        out = "Hashtable(\n"

        for i, e in zip(range(self.max_length), self.entries):
            e_fmt = f"{e}" if e else ""
            out += f"\t{i} --- {e_fmt:^{l+2}}"

            if (not e):
                out += "\n"
                continue

            while (e.next_node):
                e_fmt = f"{e.next_node}"
                out += f" --- {e_fmt:^{l+2}}"
                e = e.next_node

            out += "\n"
        out += ")"
        return out