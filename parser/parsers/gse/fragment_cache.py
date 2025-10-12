from collections import OrderedDict, deque
from parser.parsers.gse.gse_standard import start_of_pdu, middle_of_pdu, end_of_pdu

class FragmentCache:
    def __init__(self, capacity=256):
        self.fragment_cache = OrderedDict()  # frag_id -> state
        self.capacity = capacity        # max total fragment pieces
        self.total_fragments = 0        # track total fragments

    def add_fragment(self, frag_id, part_type, payload):
        # Look up or create state for this frag_id
        state = self.fragment_cache.get(frag_id)
        if state is None:
            state = {
                "pieces": deque(),      # list of (part_type, payload)
                "has_beginning": False,
                "has_end": False,
            }
            self.fragment_cache[frag_id] = state
        else:
            self.fragment_cache.move_to_end(frag_id)  # LRU update

        # Add the fragment
        state["pieces"].append((part_type, payload))
        self.total_fragments += 1

        if part_type == "beginning":
            state["has_beginning"] = True
        elif part_type == "end":
            state["has_end"] = True

        # Check for completeness
        if state["has_beginning"] and state["has_end"]:
            reassembled = b"".join(p[1] for p in state["pieces"])
            self.total_fragments -= len(state["pieces"])
            del self.fragment_cache[frag_id]
            return ("reassembled", frag_id, reassembled)

        # Enforce total fragment capacity
        while self.total_fragments > self.capacity:
            evicted_id, evicted_state = self.fragment_cache.popitem(last=False)
            self.total_fragments -= len(evicted_state["pieces"])
            return ("evicted", evicted_id, None)

        return ("incomplete", frag_id, None)
