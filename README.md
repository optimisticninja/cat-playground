# ca

*In development*

Playground for finding reversible cellular automata transforms in a 1D N-neighborhood cellular space.

## Transforms at the cellular level

Each new cell is the mapping of a unique neighborhood state in all possible neighborhood state permutations to the Nth bit in the rule number.

```python
    def cellular_transition(self, cell, rule) -> int:
        """
        Interaction with a single cell in the automaton state
        :param cell: index of cell in state
        :param rule: bit-mapping rule to apply
        :return: new cell state
        """
        print("Rule: ", rule)
        print("Cell: ", cell)
        neighbors = self.get_neighbor_sites(cell)
        if self.config.interaction == RuleOfInteraction.NEIGHBORHOOD_TO_RULE_BIT:
            neighbors_tuple = tuple(neighbors)
            bit_offset = self.config.neighborhood_states.index(neighbors_tuple)
            new_cell_state = (rule >> bit_offset) & 1
            return new_cell_state
        else:
            raise NotImplementedError
```

# Transforms at the block level

Each new cell is the mapping of a unique neighborhood state in all possible neighborhood state permutations to the Nth bit in the rule number, XOR'd with the previous cell.

```python
    def block_transition(self, block, rule) -> []:
        """
        A function that takes as input an assignment of states
              for the cells in a single tile and produces as output another assignment
              of states for the same cells.
        :param block:
        :param rule:
        :return:
        """
        print("Block: ", block)
        print("Rule: ", rule)
        if self.config.interaction == RuleOfInteraction.NEIGHBORHOOD_TO_RULE_BIT_PREVIOUS_CELL_XOR:
            new_block = []
            neighborhood_states_idx = self.config.neighborhood_states.index(block)
            for i in range(len(block)):
                new_cell_state = ((rule >> neighborhood_states_idx) ^ block[i-1]) & 1
                new_block.append(new_cell_state)
            return new_block
        else:
            raise NotImplementedError
        raise NotImplementedError
```


## Terminology

| term | definition                                                                                                                       |
| --- |----------------------------------------------------------------------------------------------------------------------------------|
| bias | when dealing with even number neighborhoods, this is the side to pull the extra cell from (right or left)                        |
| neighbor sites | the block and neighborhood size                                                                                                  |
| neighborhood | the "radius" around the target cell. radii can be uneven                                                                         |
| block | a non-overlapping partition of the CA state to operate on. instead of updating at the cellular level, the whole block is updated |
| gateway key | the encoding/configuration of the cellular automata (initial state, neighborhood sites, total cells, boundary rule, etc.) |                                                                           

## References

[Cellular Automata Transforms: Theory and Applications in Multimedia Compression, Encryption, and Modeling](https://www.amazon.com/Cellular-Automata-Transforms-Applications-Compression/dp/0792378571)
