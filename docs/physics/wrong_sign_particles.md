Note that we are not guaranteed to be reconstructing real particles. Instead,
we are looking at combinations of reconstructed tracks with specific properties
consistent with originating from a common vertex. These reconstructed particles
may original from different mothers---they may still pass our vertexing
criteria by sheer coincidence combined with resolution effects and the fact
that tracks don't have an origin point.

By looking at wrong-sign combinations, we get a pure sample of "candidates"
that **did not** originate from a common mother (charged was not conserved in
this "decay" mode, so it is not physical). We can be absolutely sure that no
signal or physics background contaminates these samples because there is no
such thing as a $B^{++}$ (again, charge not conserved). Therefore, these
combinations can be used to study and model these random combinations of tracks
that pass our selection.

A caveat to remember is that the wrong-sign combinations are not guaranteed to
look exactly like the background in the right-sign we are trying to understand.
This is where the candidates with mass greater than $m_B$ come in handy. Here we
know neither the right-sign nor the wrong-sign has any physics candidates in
them, and we can see how the two differ.

!!! example "An example from muonic $R(D^{(*)})$"
    In [`b2D0MuXFakeB2DMuNuForTauMuLine`](http://lhcbdoc.web.cern.ch/lhcbdoc/stripping/config/stripping21/semileptonic/strippingb2d0muxfakeb2dmunufortaumuline.html),
    the decay $B^- \to D^0 \mu^-$ is defined by:

    ```python
    DecayDescriptors = [ '[B- -> D0 mu-]cc' , '[B+ -> D0 mu+]cc' ]
    ```

    Note the latter decay is actually wrong-sign; the right-sign should be
    a `D~0` ($\bar{D^0}$), instead of a `D0` ($D^0$).

    Therefore, if in our reconstruction, we define the decay to be:

    ```python
    DecayDescriptor = '[B- -> D0 mu-]cc'
    ```

    Then **NOT ALL** events passing stripping cuts contain a $B^-$ candidate,
    because we are only reconstructing _right-sign_ candidates with the decay
    descriptor above.

    Indeed, if we inspect the `DaVinci` log with the two decay descriptors:

    - $B^-$ with both signs:
        ```
        SELECT:/Event/Semileptonic/Phys/b2D0MuXFakeB|     2.232 |     2.417 |    0.685      10.7     0.86 |    1868 |     4.517 |
        SelMyStrippedMuFilteredEvent                |    16.129 |    17.152 |    2.212    2950.3    68.08 |    1868 |    32.042 |
        SelMyStrippedChargedK                       |     0.016 |     0.005 |    0.003       0.1     0.00 |    1833 |     0.010 |
        SelMyStrippedChargedPi                      |     0.000 |     0.003 |    0.002       0.0     0.00 |    1833 |     0.007 |
        SelMyD0                                     |     0.278 |     0.334 |    0.210      44.0     1.02 |    1833 |     0.613 |
        SelMyStrippedMu                             |     0.000 |     0.004 |    0.003       0.0     0.00 |    1823 |     0.008 |
        SelMyB-                                     |     0.197 |     0.178 |    0.116       0.7     0.05 |    1823 |     0.325 |
        SelMyComboD0                                |     0.005 |     0.004 |    0.003       0.0     0.00 |    1812 |     0.008 |
        ```
    - $B^-$ with right-sign only:
        ```
        SELECT:/Event/Semileptonic/Phys/b2D0MuXFakeB|     1.761 |     1.887 |    0.618       6.2     0.65 |    1868 |     3.526 |
        SelMyStrippedMuFilteredEvent                |    13.238 |    13.371 |    1.952    1455.4    33.61 |    1868 |    24.978 |
        SelMyStrippedChargedK                       |     0.000 |     0.004 |    0.002       0.2     0.00 |    1833 |     0.007 |
        SelMyStrippedChargedPi                      |     0.000 |     0.003 |    0.002       0.0     0.00 |    1833 |     0.006 |
        SelMyD0                                     |     0.278 |     0.257 |    0.187      33.3     0.77 |    1833 |     0.473 |
        SelMyStrippedMu                             |     0.000 |     0.003 |    0.002       0.0     0.00 |    1823 |     0.006 |
        SelMyB-                                     |     0.093 |     0.121 |    0.087       0.5     0.03 |    1823 |     0.221 |
        SelMyComboD0                                |     0.000 |     0.003 |    0.002       0.0     0.00 |    1197 |     0.004 |
        ```

    With both signs, $B^-$ selection only kills 11 events (1823 -> 1812). With
    right-sign only, the same selection (with a different decay descriptor, of
    course) kills 626 events (1823 -> 1197).
