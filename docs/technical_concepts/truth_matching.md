# Truth matching

In LHCb, truth-matching are separated into 3 categories:

1. Neutral particles (both basic and composite)
2. Basic stable charged particles
3. Composite charged particles

They have different truth-matching strategies.

Also, take a look at [the Particle2MC TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/Particle2MC).

!!! info
    The [event model TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/LHCbPhysicsEventModelTaskForce) might also be helpful.

!!! warning
    The code below might be phased out as some of them are not present in
    `master` branch of the related projects.


## Neutral particles

The truth-matching is done purely with calorimeter info. It is implemented in
[`Calo2MCTool`](https://gitlab.cern.ch/lhcb/Rec/-/blob/7a48b9c4084f398fa7c867a8e3165e9db7682e16/Calo/CaloTools/src/Calo2MCTool.cpp).

The tool returns the MC particle that is _best matched_ to the reconstructed particle.
The technical details are in `LinkedTo` class, which is in `LHCb` project in

```
Event/LinkerEvent/Linker/LinkedTo.h
```

The MC `DST` will provide several relation tables for truth-matching. See [this TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/CaloEventModel#Relations).


## Basic stable charged particles

This is done with [`P2MCPFromProtoP`](https://gitlab.cern.ch/lhcb/Analysis/-/blob/master/Phys/DaVinciMCTools/src/P2MCPFromProtoP.cpp).

It finds the `ProtoParticle` of the reconstructed `Particle`. Then:

!!! error "Before you proceed"
    This is my own understanding! It may not be correct!

The MC `DST` file should come with a truth-table for stable charged particles.
See [this TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/MakeNTupleFromTurbo).

How is this table constructed? I have no idea. But here we should be able to go
from `ProtoParticle` to `MCParticle` with this table.


## Composite charged particles

From the _Particle2MC TWiki_:

> Each reconstructed final state daughter of the composite Particle has an associated `MCParticle`, and all these associated `MCParticle`s have the same final `MCParticle` mother.
