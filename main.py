import itertools
from enum import Enum

import matplotlib.pyplot as plt
from db import *
from sqlalchemy.orm import sessionmaker


class BoundaryConfig(Enum):
    ZERO = 0,
    CYCLIC = 1


class NeighborhoodBiasing(Enum):
    LHS = 0,
    RHS = 1


class RuleOfInteraction(Enum):
    # Mapping of binary numbers to neighborhood state
    NEIGHBORHOOD_SET = "neighborhood_set"


class GeometricStructure(Enum):
    ONE_D = 0,
    SQUARE = 1,
    HEXAGONAL = 2


class TransformType(Enum):
    ORTHOGONAL= 0,
    ORTHOGONAL_PROGRESSIVE = 1,
    NON_ORTHOGONAL = 2,
    SELF_GENERATING = 3


class BasisType(Enum):
    TODO = 0


class NeighborhoodBias(Enum):
    LHS = 0
    RHS = 1


class GatewayKey():
    def __init__(self, cells, neighborhood_sites):
        self.interaction = RuleOfInteraction.NEIGHBORHOOD_SET
        self.neighborhood_sites = neighborhood_sites
        self.neighborhood_states = [seq for seq in itertools.product([0, 1], repeat=self.neighborhood_sites)]
        self.num_states = len(self.neighborhood_states)
        # TODO: Accomodate higher dimensionality, see self.dimensionality
        self.total_cells = len(cells)
        self.initial_config = cells
        self.boundary_config = BoundaryConfig.CYCLIC
        self.geometric_structure = GeometricStructure.ONE_D
        # TODO: Accomodate higher dimensionality
        self.dimensionality = 1
        self.transform_type = TransformType.ORTHOGONAL
        self.basis_type = BasisType.TODO
        self.neighbohood_bias = NeighborhoodBias.RHS


class CA:
    def __init__(self, total_cells, neighborhood_sites):
        # Create initial state all true with midway point off
        self.state = [1] * total_cells
        self.state[total_cells // 2] = 0
        # Snapshot initial config
        self.config = GatewayKey(self.state, neighborhood_sites)
        self.history = []

    # TODO: Higher dimensionality
    # TODO: Currently implemented as cyclic, zero boundary needs to be accommodated as well
    def get_neighbor_sites(self, cell: int) -> []:
        """
        Get neighborhood sites (neighbors + cell itself) with biasing for left hand side
        on even numbers, or shifting and grabbing the rightmost
        :param cell:
        :return:
        """
        distance = self.config.neighborhood_sites // 2
        lhs = cell - distance
        rhs = cell + distance
        neighborhood = []
        if self.config.boundary_config == BoundaryConfig.CYCLIC:
            if self.config.neighborhood_sites % 2:
                if self.config.neighbohood_bias == NeighborhoodBias.LHS:
                    lhs -= 1
                else:
                    rhs += 1
                if lhs < 0:
                    neighborhood += self.state[lhs:] + self.state[:rhs]
                elif rhs > self.config.total_cells:
                    rhs = -(self.config.total_cells - rhs)
                    neighborhood += self.state[lhs:] + self.state[:rhs]
                else:
                    neighborhood += self.state[lhs:rhs]
            else:
                if lhs < 0:
                    neighborhood += self.state[lhs:] + self.state[:rhs]
                elif rhs > self.config.total_cells:
                    rhs = -(self.config.total_cells - rhs)
                    neighborhood += self.state[lhs:] + self.state[:rhs]
                else:
                    neighborhood += self.state[lhs:rhs]
        else:
            raise NotImplementedError
        print("Neighborhood:", neighborhood)
        return neighborhood

    # TODO: Interaction should do a whole epoch set of n timesteps
    def interaction(self, cell, rule) -> int:
        """
        Interaction with a single cell in the automaton state
        :param cell: index of cell in state
        :param rule: bit-mapping rule to apply
        :return: new cell state
        """
        print("Rule: ", rule)
        print("Cell: ", cell)
        neighbors = self.get_neighbor_sites(cell)
        if self.config.interaction == RuleOfInteraction.NEIGHBORHOOD_SET:
            neighbors_tuple = tuple(neighbors)
            bit_offset = self.config.neighborhood_states.index(neighbors_tuple)
            new_cell_state = (rule >> bit_offset) & 1
            return new_cell_state
        else:
            raise NotImplementedError


if __name__ == "__main__":
    GRID_SIZE = 31
    EPOCHS = 15
    NEIGHBORHOOD_SITES = 4

    ca = CA(GRID_SIZE, NEIGHBORHOOD_SITES)

    print(ca.config.neighborhood_states)
    print(ca.config.num_states)

    start_states = set()
    end_states = set()
    Session = sessionmaker(bind=engine)
    session = Session()
    for rule in range(2 ** ca.config.num_states):
        state_history = [ca.config.initial_config]
        state_transitions = []
        ca.state = ca.config.initial_config
        for epoch in range(EPOCHS):
            # capture previous state
            new_state = ca.state.copy()
            for cell in range(GRID_SIZE):
                new_state[cell] = ca.interaction(cell, rule)
            ca.state = new_state
            state_history.append(ca.state)
            state_transitions.append(StateTransition(epoch, rule, "".join(str(i) for i in ca.state)))
        print(state_history)
        for state_transition in state_transitions:
            session.add(state_transition)
        session.commit()
        plt.imsave('img/{}.png'.format(rule), state_history)
    session.close()


