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


## Truth-Matching for RDX run 2

For the run 2 RDX analysis, when postprocessing our MC ntuples, we perform truth-matching copied from Phoebe's code for
the run 1 analysis.

!!! info

    Her code for truth-matching can be found in:

    - `redoHistos_D0.C`+`AddD0B_tmp.C` (for $D^0$ sample)
    - `redoHistos_Dst.C`+`AddB.C` (for $D^*$ sample)

    in this [proc folder](https://gitlab.cern.ch/bhamilto/rdvsrdst-histfactory/-/tree/master/proc)
    from her gitlab run 1 analysis (preservation) code repo.

We implement the truth-matching differently from her in order to work (more
understandably) with our workflow;
rather than using flags and filling all histograms (templates) all at the same
time based on those flags, we truth-match each decay mode
(i.e. the `MC ID`s listed [here](../data/data_sources.md#run-2-muonic-rd-monte-carlo))
separately and store the result as a coded integer `truthmatch` in our
postprocessed ntuples.

!!! warning "Difference between Phoebe's and our truth-matching"

    - Phoebe's implementation: An event can be used to fill any, and even
        multiple, templates, not just templates corresponding to the decay mode
        (eg. an event for $B^0 \rightarrow D^* \mu\nu$ MC could pass the truth-
        matching requirements and thus be filled in for the template
        corresponding to $B^0 \rightarrow D^* X_c(\rightarrow \mu\nu X')X$),

        And indeed this is seen to occur for a fraction of a percent of all
        events.

    - Our truth-matching: Takes in the decay mode that the user wants to truth-
        match against as an input and will only set `truthmatch` to a corresponding
        value for that decay mode.

        Additionally, our implementation will never fill in multiple templates
        with the same event.

To apply our truth-matching when postprocessing ntuples:

1. Use the header [`truth_match.h`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/include/functor/rdx/truth_match.h)
2. In a postprocessing configuration `YAML`[^1], add a `calculation` integer
    variable (nominally called `truthmatch`) that is calculated using:

    - `MC_TRUTH_MATCH_DST(...)` (for $D^*$ sample)
    - `MC_TRUTH_MATCH_D0(...)` (for $D^0$ sample)

    !!! note

        The input parameters for these functions can be found at the bottom of the
        truth-matching script linked above.

        As already mentioned, one required input is the decay mode ID.

[^1]: Recall instructions [here](../ntupling/step2_babymaker.md) for postprocessing.

!!! info "Optional debugging flags for truth-matching"

    The truth-matching code has some optional debugging flags that can be set
    if one:

    - Wants to not separate $D^{**}_{(s)}$ cocktails
    - Want to separate $D^{**}H$ cocktails
    - Doesn't want to separate $DD$ cocktails

    For now, the $DD$ debug flag is set to true until the code is
    developed to actually separate those cocktails (and, in fact, Phoebe does
    not separate the cocktails for her templates).

    In the encoding scheme below, this means that temporarily `truthmatch` will
    have `b1b2=0`. Without setting these flags, the coded `truthmatch` int is
    nominally set to encode all information that should be relevant for
    building the run 2 RDX templates.

Once this is done, the postprocessed ntuples will contain a `truthmatch` branch
that encodes what type of decay the event was successfully truth-matched to, or
`truthmatch=0` if the event failed to pass the truth-matching requirements. The
encoding scheme for `truthmatch` works as follows: `truthmatch=a1b1b2c1c2d1`
where

1. `d1`=
    1. 0 if normalization(-like) (i.e. without $\tau$)
    2. 1 if signal(-like)

2. `c1c2` are two digits referring to the "primary" $D$ meson. For non-$DD$
    decays, this is just the $D$ that the $B$ decays to; for now, for $DD$
    decays,  `c1c2=00`. Otherwise, `c1c2=`:
    1. `01` for $D^0$,
        `02` for $D^+$,
        `03` for $D^{*0}$,
        `04` for $D^{*+}$

    2. `10` for all (light) $D^{**0}$
        (i.e. cocktail not separated, but it's required that the specific event
        $D^{**}$ is possible for the considered decay),
        `11` for $D_0^{*0}$,
        `12` for $D_1^0$,
        `13` for $D_1'^0$,
        `14` for $D_2^{*0}$

    3. `20` for all (light) $D^{**+}$,
        `21` for $D_0^{*+}$,
        `22` for $D_1^+$,
        `23` for $D_1'^+$,
        `24` for $D_2^{*+}$

    4. `30` for all heavy $D^{**}H^0$
        (again, it's internally required that the $D^{**}H$ is possible),
        and (for debugging)
        `31` for $D(2S)^{*+}$,
        `32` for $D(2S)^+$,
        `33` for $D(2750)^+$,
        `34` for $D(3000)^+$

    5. `40` for all heavy $D^{**}H^+$, and
        `41` for $D(2S)^{*+}$,
        `42` for $D(2S)^+$,
        `43` for $D(2750)^+$,
        `44` for $D(3000)^+$

    6. `50` for all strange $D^{**}_s$
        (again, internally require specific $D^{**}_s$ to be possible), and
        `53` for $D_{1s}'$,
        `54` for $D_{2s}^*$
        (to keep consistent with $D^{**}$ scheme; there aren't any "$D_{0s}^*, D_{1s}$")

3. `b1b2` are used to separate `DD` cocktails, and will nominally be set to nonzero values for every `DD` decay. For now, this feature is not
implemented, so it will always be that `b1b2=00`

4. `a1`=
    1. `0` if not a $D^{**}H$ or $DD$ decay,
        and $D^{**} \rightarrow D^{(*)}\pi\pi$ decays are cut out if a (light)
       $D^{**}$ decay
    2. `1` if a $DD$ decay from a $B^0$
    3. `2` if a $DD$ decay from a $B^+$
    4. `3` if a $D^{**}H$ decay where $D^{**}H \rightarrow D* \rightarrow D$
        (useful because Phoebe separates this topology from
        $D^{**}H \rightarrow D^0$ directly in her templates for the
        $D^0$ sample)
    5. `4` if a $D^{**}H$ decay where $D^{**}H \rightarrow D$
    6. `5` if a (light) $D^{**}$ decay explicitly with two pion decays
        ($D^{**} \rightarrow D^{(*)}\pi\pi$) kept

!!! example

    - $B^0 \rightarrow D^* \mu\nu$ will be encoded as `000041`
    - $B^- \rightarrow D^{*0} \mu\nu$ as `000031`
    - $B^0 \rightarrow D^0 \tau\nu$ as `000011`
    - $B^0 \rightarrow D_1' \tau\nu$ (no $2\pi$) as `000231`
    - $B^+ \rightarrow D_2^*(\rightarrow D^*\pi\pi)\mu\nu$ as `500140`
    - $B^0 \rightarrow D^{**}H(\rightarrow D\pi\pi)\mu\nu$ as `400400`
    - $B^+ \rightarrow D^0X(\rightarrow \mu\nu X')X$ as `200000`
