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

For the run 2 RDX analysis, when postprocessing our MC ntuples, we perform truth-matching _mostly_ copied from Phoebe's code for
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

        And indeed I see this happening for a fraction of a percent of all
        events.

    - Our truth-matching: Takes in the decay mode that the user wants to apply truth-
        matching to as an input and will only set `truthmatch` to a corresponding
        value for that decay mode.

        Additionally, our implementation will never fill in multiple templates
        with the same event.

To apply our truth-matching when postprocessing ntuples:

1. Main code is in [`truth_match.h`](https://github.com/umd-lhcb/lhcb-ntuples-gen/blob/master/include/functor/rdx/truth_match.h)
2. In a postprocessing configuration `YAML`[^1], add `truthmatch` integer that is calculated using:

    - `MC_TRUTH_MATCH_DST(...)` (for $D^*$ sample)
    - `MC_TRUTH_MATCH_D0(...)` (for $D^0$ sample)

    !!! note

        The input parameters for these functions can be found at the bottom of the
        truth-matching script linked above.

        As already mentioned, one required input is the decay mode ID.

[^1]: Recall instructions [here](../ntupling/step2_babymaker.md) for postprocessing.

!!! info "Optional debugging flags for truth-matching"

    The truth-matching code has some optional debugging flags that can be set
    if one wants to:

    - **not** separate $D^{**}_{(s)}$ cocktails
    - separate $D^{**}H$ cocktails
    - **not** separate $DD$ cocktails

    Nominally, for run2 our `truthmatch` int is separating $D^{**}_{(s)}$, not separating $D^{**}H$,
    and partially separating $DD$. Without setting these flags, `truthmatch` is set to encode all 
    information that should be relevant for building the run 2 RDX templates.

Once this is done, the postprocessed ntuples will contain a `truthmatch` branch
that encodes what type of decay the event was successfully truth-matched to, or
`truthmatch=0` if the event failed to pass the truth-matching requirements. The
encoding scheme for `truthmatch` works as follows: `truthmatch=a1b1b2c1c2d1`
where

1. `d1`=
    - `0` if normalization(-like) (i.e. without $\tau$)
    - `1` if signal(-like)

2. `c1c2` are two digits referring to the "primary" $D$ meson (ie. coming from the $B$). For $DD$ 
    decays, this is ambiguous, so `c1c2=00`. For non-$DD$ decays, `c1c2=`:
    - `01` for $D^0$,
        `02` for $D^+$,
        `03` for $D^{*0}$,
        `04` for $D^{*+}$

    - `10` for all (light) $D^{**0}$
        (i.e. cocktail not separated, but it's required that the specific
        $D^{**}$ is possible [included in the dec file] for the considered decay), or if separated:
        `11` for $D_0^{*0}$,
        `12` for $D_1^0$,
        `13` for $D_1'^0$,
        `14` for $D_2^{*0}$

    - `20` for all (light) $D^{**+}$, or if separated:
        `21` for $D_0^{*+}$,
        `22` for $D_1^+$,
        `23` for $D_1'^+$,
        `24` for $D_2^{*+}$

    - `30` for all heavy $D^{**0}_H$
        (again, internally required that the decay is possible), or if separated:
        `31` for $D(2S)^{*+}$,
        `32` for $D(2S)^+$,
        `33` for $D(2750)^+$,
        `34` for $D(3000)^+$

    - `40` for all heavy $D^{**+}_H$, or if separated:
        `41` for $D(2S)^{*+}$,
        `42` for $D(2S)^+$,
        `43` for $D(2750)^+$,
        `44` for $D(3000)^+$

    - `50` for all strange $D^{**}_s$
        (again, internally require the $D^{**}_s$ is possible), or if separated:
        `53` for $D_{1s}'$,
        `54` for $D_{2s}^*$
        (to keep consistent with $D^{**}$ scheme; there aren't any "$D_{0s}^*, D_{1s}$")

3. `b1b2` are used to (partially, at least for now) separate `DD` cocktails, equal to
    - `01` for a 2-body $B\rightarrow D^{(*)}D^{(*)}$, `02` for a 2-body $B\rightarrow D^{(*)(**)}D^{(*)(**)}_s$

    - `10` for a 3-body $B\rightarrow D^{(*)}D^{(*)}K^{(*)}$, `20` for a 3- or 4-body $B\rightarrow D^{(*)}_sD^{(*)(**)}\pi(\pi)$

4. `a1`=
    - `0` if not a $D^{**}_H$, $DD$, or (light) $D^{**} \rightarrow D^{(*)}\pi\pi$ decay
    - `1` if a $DD$ decay from a $B^0$
    - `2` if a $DD$ decay from a $B^+$
    - `3` if a $D^{**}_H$ decay where $D^{**}_H \rightarrow D^* \rightarrow D$
        (useful because Phoebe separates this topology from
        $D^{**}_H \rightarrow D$ directly in her templates for the
        $D^0$ sample)
    - `4` if a $D^{**}_H$ decay where $D^{**}_H \rightarrow D$
    - `5` if a (light) $D^{**} \rightarrow D^{(*)}\pi\pi$ decay

!!! example

    - $B^0 \rightarrow D^* \mu\nu$ will be encoded as `000041`
    - $B^- \rightarrow D^{*0} \mu\nu$ as `000031`
    - $B^0 \rightarrow D^0 \tau\nu$ as `000011`
    - $B^0 \rightarrow D_1' \tau\nu$ (no $2\pi$) as `000231`
    - $B^+ \rightarrow D_2^*(\rightarrow D^*\pi\pi)\mu\nu$ as `500140`
    - $B^0 \rightarrow D^{**}_H(\rightarrow D\pi\pi)\mu\nu$ as `400400`
    - $B^0 \rightarrow D^{*+}D^-(\rightarrow \mu\nu X)$ as `101000`
    - $B^0 \rightarrow D^{*+}D_s(\rightarrow \tau\nu)$ as `102001`
    - $B^0 \rightarrow D^{0}D^{*-}(\rightarrow \mu\nu X)K^+$ as `110000`
    - $B^+ \rightarrow D^{*-}D_s(\rightarrow \mu\nu X)\pi^+$ as `220000`
