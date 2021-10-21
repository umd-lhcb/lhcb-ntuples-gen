# Truth-Matching

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

# Truth-Matching for RD(*) Run 2

For the run 2 R(D(*)) analysis, when postprocessing our MC ntuples, we perform truth-matching copied from Phoebe's code for
the run 1 analysis. Her code for truth-matching can be found in `redoHistos_D0.C`+`AddD0B_tmp.C` (for `D0` sample) and
`redoHistos_Dst.C`+`AddB.C` (for `D*` sample) in this
[proc folder](https://gitlab.cern.ch/bhamilto/rdvsrdst-histfactory/-/tree/master/proc) from her run 1 analysis (preservation)
code repo. We implement the truth-matching differently from her in order to work (more understandably) with our workflow; rather than
using flags and filling all histograms (templates) all at the same time based on those flags, we truth-match each decay mode (ie. the `MC ID`s
listed [here](https://umd-lhcb.github.io/lhcb-ntuples-gen/data/data_sources/#run-2-muonic-rd-monte-carlo)) separately and store
the result as a coded integer `truthmatch` in our postprocessed ntuples.

!!! warning
    There is one minor difference of note that results from our differing truth-matching schemes. In Phoebe's implementation, an
    event can be used to fill any, and even multiple, templates, not just templates corresponding to the decay mode (eg. an event for
    `B0->D*munu` MC could pass the truth-matching requirements and thus be filled in for the template corresponding to `B0->D*Xc(->munuX')X`),
    and indeed this is seen to occur for a fraction of a percent of all events. On the other hand, our truth-matching takes in the decay mode
    that the user wants to truth-match against as an input and will only set `truthmatch` to a corresponding value for that decay mode.
    Additionally, our implementation will never fill in multiple templates with the same event.

To apply our truth-matching when postprocessing ntuples, using the script found
[here](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/a9e19c89da3dfbd7ee0aa34781cd75f6ea7cdd32/include/functor/rdx/truth_match.h), in the
configuration `YAML` file (recall instructions [here](https://umd-lhcb.github.io/lhcb-ntuples-gen/ntupling/step2_babymaker/) for postprocessing),
add a `calculation` integer variable (nominally called `truthmatch`) that is calculated using either `MC_TRUTH_MATCH_DST(...)` (for `D* sample`)
or `MC_TRUTH_MATCH_D0(...)` (for `D0` sample). The input parameters for these functions can be found at the bottom of the truth-matching script
linked above. As already mentioned, one required input is the decay mode ID.

!!! info
    The truth-matching code has some optional debugging flags that can be set if one wants to not separate `D**(s)` cocktails, does want to
    separate `D**H` cocktails, or doesn't want to separate `DD` cocktails. For now, the `DD` debug flag is set to true until the code is
    developed to actually separate those cocktails (and, in fact, Phoebe does not separate the cocktails for her templates). In the encoding
    scheme below, this means that temporarily `truthmatch` will have `b1b2=0`. Without setting these flags, the coded `truthmatch` int is
    nominally set to encode all information that should be relevant for building the run 2 R(D(*)) templates.

Once this is done, the postprocessed ntuples will contain a `truthmatch` branch that encodes what type of decay the event was successfully
truth-matched to, or `truthmatch=0` if the event failed to pass the truth-matching requirements. The encoding scheme for `truthmatch` works as
follows: `truthmatch=a1b1b2c1c2d1` where

1. `d1`=
    1. 0 if normalization(-like) (ie. without tau)
    2. 1 if signal(-like)
2. `c1c2` are two digits referring to the "primary" `D` meson. For non-DD decays, this is just the `D` that the `B` decays to; for now, for DD
decays,  `c1c2=00`. Otherwise, `c1c2=`
    1. `01` for `D0`, `02` for `D+`, `03` for `D*0`, `04` for `D*+`
    2. `10` for all (light) `D**^0` (ie. cocktail not separated, but it's required that the specific event `D**` is possible for the
    considered decay), `11` for `D0*^0`, `12` for `D1^0`, `13` for `D1'^0`, `14` for `D2*^0`
    3. `20` for all (light) `D**^+`, `21` for `D0*^+`, `22` for `D1^+`, `23` for `D1'^+`, `24` for `D2*^+`
    4. `30` for all heavy `D**H^0` (again, it's internally required that the `D**H` is possible), and (for debugging) `31` for `D*(2S)^+`, `32`
    for `D(2S)^+`, `33` for `D(2750)^+`, `34` for `D(3000)^+`
    5. `40` for all heavy `D**H^+`, and `41` for `D*(2S)^+`, `42` for `D(2S)^+`, `43` for `D(2750)^+`, `44` for `D(3000)^+`
    6. `50` for all strange `D**s` (again, internally require specific `D**s` to be possible), and `53` for `D1'_s`, `54` for `D2*_s` (to keep
    consistent with `D**` scheme; there aren't any "`D0*_s, D1_s`")
3. `b1b2` are used to separate `DD` cocktails, and will nominally be set to nonzero values for every `DD` decay. For now, this feature is not
implemented, so it will always be that `b1b2=00`
5. `a1`=
    1. `0` if not a `D**H` or DD decay, and `D**->D(*)pipi` decays are cut out if a (light) `D**` decay
    2. `1` if a `DD` decay from a `B0`
    3. `2` if a `DD` decay from a `B+`  
    4. `3` if a `D**H` decay where `D**H->D*->D` (useful because Phoebe separates this topology from `D**H->D0` directly in her templates for
    the `D0` sample)
    5. `4` if a `D**H` decay where `D**H->D`
    6. `5` if a (light) `D**` decay explicitly with two pion decays (`D**->D(*)pipi`) kept

!!! info
    For examples: successful truth-matching to `B0->D*munu` will be encoded as `000041`, `B-->D*0munu` as `000031`, `B0->D0taunu` as `000011`,
    `B0->D1'taunu` (no 2pi) as `000231`, `B+->D2*(->D*pipi)munu` as `500140`, `B0->D**H(->Dpipi)munu` as `400400`, and `B+->D0X(->munuX)X` as `200000`
