import matplotlib.pyplot as plt

from gatewaykey import GatewayKey, NeighborhoodBias, BoundaryConfig, RuleOfInteraction


class BlockCA1D:
    def __init__(self, config: GatewayKey):
        # Capture initial state into working state
        self.state = config.initial_state
        self.config = config

    def get_block(self, cell: int) -> ():
        """
        Get block starting at @cell offset (cyclic and zero boundary currently supported)
        :param cell: target cell
        :return: block as tuple, cells added to block if boundary reached
        """
        block = self.state[cell: cell + self.config.neighbor_sites]
        to_add = self.config.neighbor_sites - len(block)
        # Handle boundary
        if len(block) < self.config.neighbor_sites:
            if self.config.boundary_config == BoundaryConfig.CYCLIC:
                # Wrap state and append missing block(s) from beginning
                block += self.state[: to_add]
            elif self.config.boundary_config == BoundaryConfig.ZERO:
                block += [0] * to_add
            else:
                raise NotImplementedError
        return tuple(block), to_add

    # TODO: Devise rules beyond existing or hill climb to try and find more complex patterns
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
                new_cell_state = ((rule >> neighborhood_states_idx) ^ block[i - 1]) & 1
                new_block.append(new_cell_state)
            return new_block
        else:
            raise NotImplementedError
        raise NotImplementedError

    def evolve(self, epochs):
        """
        Evolve for @epochs (timesteps)
        :param epochs: number of timesteps to evolve
        """
        print(self.config.neighborhood_states)
        print(self.config.total_neighborhood_states)

        for rule in range(2 ** self.config.total_neighborhood_states):
            state_history = [self.config.initial_state]
            self.state = self.config.initial_state
            for epoch in range(epochs):
                # capture previous state
                new_state = self.state.copy()
                # iterate over state by block-length
                for block_start in range(0, len(self.state), self.config.neighbor_sites):
                    block, added = self.get_block(block_start)
                    block_transition = self.block_transition(block, rule)
                    if block_start == 0:
                        new_state = list(block_transition) + new_state[block_start + self.config.neighbor_sites:]
                    else:
                        new_state = new_state[:block_start] + list(block_transition) + new_state[
                                                                                       block_start + self.config.neighbor_sites:]
                    # Slice off boundary cells to return to proper state size
                    if added:
                        new_state = new_state[:-added]
                # overwrite state with update
                self.state = new_state
                state_history.append(self.state)
            print(state_history)
            plt.imsave('img/{}.png'.format(rule), state_history)


# TODO: Run tests on standard CAs to see if there are any reversible rules
class CA1D:
    def __init__(self, config: GatewayKey):
        # Capture initial state into working state
        self.state = config.initial_state
        self.config = config

    def get_neighbor_sites(self, cell: int) -> []:
        """
        Get neighborhood sites (neighbors + cell itself) with biasing for left hand side
        on even numbers, or shifting and grabbing the rightmost
        :param cell:
        :return:
        """
        rounded_radius = self.config.neighbor_sites // 2
        lhs = cell - rounded_radius
        rhs = cell + rounded_radius
        neighborhood = []

        # Adjust for side biasing on even neighborhood sites
        if self.config.neighbor_sites % 2:
            if self.config.neighborhood_bias == NeighborhoodBias.LHS:
                lhs -= 1
            else:
                rhs += 1
        # Apply boundary configuration and retrieve neighborhood
        if self.config.boundary_config == BoundaryConfig.CYCLIC:
            if lhs < 0:
                neighborhood += self.state[lhs:] + self.state[:rhs]
            # Hm...
            elif rhs > self.config.total_cells:
                rhs = -(self.config.total_cells - rhs)
                neighborhood += self.state[lhs:] + self.state[:rhs]
            else:
                neighborhood += self.state[lhs:rhs]
            # Hm...
        elif self.config.boundary_config == BoundaryConfig.ZERO:
            if lhs < 0:
                neighborhood += ([0] * abs(lhs)) + self.state[:rhs]
            elif rhs > self.config.total_cells:
                rhs = -(self.config.total_cells - rhs)
                neighborhood += self.state[lhs:] + ([0] * rhs)
            else:
                neighborhood += self.state[lhs:rhs]
        print("Neighborhood:", neighborhood)
        return neighborhood

    # TODO: Shrink to bit-level binops on integer state instead of indexing into binary array
    # TODO:     Ensure integers can be n-bit
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

    def evolve(self, epochs: int):
        """
        Evolve for @epochs (timesteps)
        :param epochs: number of timesteps to evolve
        """
        print(self.config.neighborhood_states)
        print(self.config.total_neighborhood_states)

        for rule in range(2 ** self.config.total_neighborhood_states):
            state_history = [self.config.initial_state]
            self.state = self.config.initial_state
            for epoch in range(epochs):
                # capture previous state
                new_state = self.state.copy()
                for cell in range(len(self.state)):
                    new_state[cell] = self.cellular_transition(cell, rule)
                self.state = new_state
                state_history.append(self.state)
            print(state_history)
            plt.imsave('img/{}.png'.format(rule), state_history)
