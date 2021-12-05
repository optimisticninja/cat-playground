# ca

*In development*

Playground for finding reversible cellular automata transforms in a 1D N-neighborhood cellular space.

## Transforms at the cellular level

Each new cell is the mapping of a unique neighborhood state in all possible neighborhood site configurations to the Nth bit in that number.

Where bit is the new cell state and self.config.neighborhood_states is the set of unique neighborhood state configurations

```python
def interaction(self, cell, rule) -> int:
    """
    Interaction with a single cell in the automaton state
    :param cell: index of cell in state
    :param rule: bit-mapping rule to apply
    """neighbors = self.get_neighbor_sites(cell)
    if self.config.interaction == RuleOfInteraction.NEIGHBORHOOD_SET:
        neighbors_tuple = tuple(neighbors)
        bit_offset = self.config.neighborhood_states.index(neighbors_tuple)
        bit = (rule >> bit_offset) & 1
        return bit
    else:
        raise NotImplementedError
```

## References

[Cellular Automata Transforms: Theory and Applications in Multimedia Compression, Encryption, and Modeling](https://www.amazon.com/Cellular-Automata-Transforms-Applications-Compression/dp/0792378571)
