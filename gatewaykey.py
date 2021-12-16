import random
from enum import Enum
import itertools


class BoundaryConfig(Enum):
    # Append/prepend zeros when edge of state is reached
    ZERO = 0,
    # Wrap indices and pull state from opposite side of state when edge is reached
    CYCLIC = 1


class RuleOfInteraction(Enum):
    # Map the bit of rule at index found in all possible neighborhood states
    #  i.e. rule_bits[index of neighborhood in config.neighborhood_states]
    NEIGHBORHOOD_TO_RULE_BIT = "neighborhood_to_rule_bit"
    NEIGHBORHOOD_TO_RULE_BIT_PREVIOUS_CELL_XOR = "neighborhood_to_rule_bit_previous_cell_xor"


# TODO: Geometric structure (when higher dimensionality supported)
# TODO: Transform type
# TODO: Basis type


class NeighborhoodBias(Enum):
    """ Which side to pull extra cell from on even-length numbers"""
    LHS = 0
    RHS = 1


# TODO: Accommodate higher dimensionality and build out entire gate key from paper
# TODO: Create serializable version (decodable string)
class GatewayKey():
    """ Configuration/Encoding of CA. """

    def __init__(self,
                 initial_state: [],
                 neighbor_sites: int,
                 boundary_config: BoundaryConfig = BoundaryConfig.ZERO,
                 interaction: RuleOfInteraction = RuleOfInteraction.NEIGHBORHOOD_TO_RULE_BIT,
                 neighborhood_bias: NeighborhoodBias = NeighborhoodBias.LHS):
        """

        :param initial_state: initial cell configuration
        :param neighbor_sites: number of cells (including target cell) in neighborhood slice (or block)
        :param boundary_config: configuration for when neighborhood reaches outside edge of state, default prepend/append zeros
        :param interaction: rule of cell interaction
        :param neighborhood_bias: which side of the cell to pull the greater portion from on even numbers
        """
        self.initial_state = initial_state
        self.neighbor_sites = neighbor_sites
        self.boundary_config = boundary_config
        self.interaction = interaction
        self.neighborhood_bias = neighborhood_bias

        self.total_cells = len(initial_state)
        # Generate all permutations of neighborhood states
        self.neighborhood_states = [
            seq for seq in itertools.product([0, 1],
                                             repeat=self.neighbor_sites)]
        self.total_neighborhood_states = len(self.neighborhood_states)
