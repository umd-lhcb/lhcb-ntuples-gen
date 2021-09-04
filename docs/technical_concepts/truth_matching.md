# Truth matching

In LHCb, the general procedure works as follows:

1. In the MC generation, after `Gauss` and `Boole`, `Brunel` is used to
    reconstruct events.
2. During this reconstruction, truth-matching maps for
    `ProtoParticle`-`MCParticle` are also created.

    This only applies to stable particles in the detector.

    An example on truth-matching in `Brunel` is provided [in this TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/FAQ/BrunelFAQ#How_do_I_implement_MC_truth_matc).

    !!! info TES locations of the truth-matching tables
        An example of these TES locations for `TurboDst` can be found
        at [this TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/MakeNTupleFromTurbo).

3. Reconstructed events and truth-matching maps are stored in the `dst` files.
4. When reconstructing events in `DaVinci`, the truth-matching maps are loaded
    from the `dst` file and used to truth-match stable particles.
5. For composite particles: Each reconstructed final state daughter of the
    composite Particle has an associated `MCParticle`, and all these associated
    `MCParticle`s have the same final `MCParticle` mother.

LHCb has implemented many truth-matching strategies.


!!! info
    Take a look at [the Particle2MC TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/Particle2MC)
    for an overview on these strategies.


## `DaVinciSmartAssociator`

In this implementation, truth-matching are separated into 3 categories:

1. Neutral particles (both basic and composite)
2. Basic stable charged particles
3. Composite charged particles

!!! warning
    The code below might be phased out as some of them are not present in
    `master` branch of the related projects.

### Neutral particles

The truth-matching is done purely with calorimeter info. It is implemented in
[`Calo2MCTool`](https://gitlab.cern.ch/lhcb/Rec/-/blob/7a48b9c4084f398fa7c867a8e3165e9db7682e16/Calo/CaloTools/src/Calo2MCTool.cpp).

The tool returns the MC particle that is _best matched_ to the reconstructed particle.

The MC `dst` will provide several relation tables for truth-matching. See [this TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/CaloEventModel#Relations).

### Basic stable charged particles

This is done with [`P2MCPFromProtoP`](https://gitlab.cern.ch/lhcb/Analysis/-/blob/master/Phys/DaVinciMCTools/src/P2MCPFromProtoP.cpp).

It finds the `ProtoParticle` of the reconstructed `Particle`. Then use the standard
truth-matching table to find the linked `MCParticle`.
