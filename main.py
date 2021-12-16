from ca1d import CA1D, BlockCA1D, GatewayKey, BoundaryConfig, RuleOfInteraction
# Research:
#   Garden of Eden Theorem
#       - surjective (apparently are pre-injective)
#       - orphan pattern
#
# TODO: Parallelize computations
# TODO: Classify CA type (seeking highly random yet reversible) (oscillator, etc)
# TODO: Hill climb to target maximum chaos yet reversible, see below todos
# TODO: Fitness function (Rules)
#       - levenshtein_damereau of target cell with new state
#       - least timesteps until reached
#       - Does it survive cellular space expansion
#       - Bit avalanche criterion & bit independence criterion (target maximum chaos)

# TODO: Search algorithm for reversible rules
#    - GA: See fitness function (Rules)
#       - population of (rules, fitness) ( Will need to limit all permutations to streams)
#       - select fittest or generate and continue
#           - Generation: Use t-1 and t-2 neighbors, and cell itself to derive second order automata
#               - Experimentation to derive ruleset
#       - reverse evolution (second order interaction) of t to t-n with chosen rule
#       - rank fitness and put back in population
# https://en.wikipedia.org/wiki/Avalanche_effect


def standard_1d_3ns():
    state_size = 31

    # Create initial state all true with midway point off
    initial_state = [1] * state_size
    initial_state[state_size // 2] = 0

    gateway_key = GatewayKey(
        initial_state=initial_state,
        neighbor_sites=3,
        boundary_config=BoundaryConfig.CYCLIC
    )
    ca = CA1D(gateway_key)
    ca.evolve(epochs=25)


def block_1d_3ns():
    state_size = 34

    initial_state = [1] * state_size
    initial_state[state_size // 2] = 0

    gateway_key = GatewayKey(
        initial_state=initial_state,
        neighbor_sites=3,
        boundary_config=BoundaryConfig.CYCLIC,
        interaction=RuleOfInteraction.NEIGHBORHOOD_TO_RULE_BIT_PREVIOUS_CELL_XOR
    )

    ca = BlockCA1D(gateway_key)
    ca.evolve(epochs=25)


if __name__ == "__main__":
    # standard_1d_3ns()
    block_1d_3ns()




