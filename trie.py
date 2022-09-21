class TrieNode:
    """A node in the trie structure."""
    def __init__(self, char) -> None:
        # The char stored in this node.
        self.char : str = char

        # Whether this node is an end to a word.
        self.is_end : bool = False

        # A dictionary of child nodes.
        # Keys are characters, values are nodes.
        self.children : dict = {}

class Trie:
    """Trie tree."""

    def __init__(self) -> None:
        """Creates trie with root node."""
        self.root: TrieNode = TrieNode("")

    def insert(self, word : str) -> None:
        """Insert a word into the trie."""

        node: TrieNode = self.root

        # Loop through each character in a word.
        for char in word:
            # Check if node already exists.
            if char in node.children:
                node = node.children[char]
            else:
                # If node not found create new one.
                new_node: TrieNode = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True

    def is_word(self, word: str) -> bool:
        """Check if word is in a Trie."""

        node: TrieNode = self.root

        # Loop through each character in a word.
        for char in word:
            # Check if node exists
            if char in node.children:
                node = node.children[char]
            else:
                return False

        return node.is_end

    def is_predecessor(self, word: str) -> bool:

        node: TrieNode = self.root

        # Loop through each character in a word.
        for char in word:
            # Check if node exists
            if char in node.children:
                node = node.children[char]
            else:
                return False

        return True




