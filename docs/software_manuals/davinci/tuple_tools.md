## Configure default TupleTools
There are 5 TupleTools that are added by default:

- `TupleToolKinematic`
- `TupleToolPid`
- `TupleToolANNPID`
- `TupleToolGeometry`
- `TupleToolEventInfo`

To configure, for example, `TupleToolPid`, remove it from the TupleTool list
first, then re-add it. This new instance can now be configured normally:

```python
tp.ToolList.remove('TupleToolPid')
tt_pid = tp.addTupleTool('TupleToolPid')
tt_pid.Verbose = True
```

!!! note
    If we don't remove the TupleTool first, neither `addTupleTool` nor
    `addTool` can make it configurable.


## `TupleToolApplyIsolation`
`TupleToolApplyIsolation` is used to find isolation variables for semileptonic
decays. This allows us to identify actual $B$ meson decay vertices more
readily.

### `_ISOLATION_Type`
Among the many variables produced by this tool, these four are about track type
of each track:

* `_ISOLATION_Type`
* `_ISOLATION_Type2`
* `_ISOLATION_Type3`
* `_ISOLATION_Type4`

!!! note
    These four tracks are the ones with the best BDT scores.

For each of these variables, it admits 3 possible values of type `float`:

* `1.0`: VELO only, with no other compatible segments found
* `3.0`: Forward tracks, which are VELO+(TT)+downstream segment (TT hits
         optional)
* `4.0`: Upstream tracks, VELO+TT

!!! note
    The type `1.0` tracks can be turned off by commenting out the following
    lines in `reco_Dst.py`:

    ``` python
    # Provide required information for VELO pions.
    ms_all_protos = ChargedProtoParticleMaker(name='MyProtoPMaker')
    ms_all_protos.Inputs = ['Rec/Track/Best']
    ms_all_protos.Output = 'Rec/ProtoP/MyProtoPMaker/ProtoParticles'  # This TES location will be accessible for all selection algorithms

    # VELO pions for Greg's isolation tool.
    # NOTE: The name 'StdNoPIDsVeloPions' is hard-coded in the tuple tool, so the
    #       name should not be changed.
    ms_velo_pions = NoPIDsParticleMaker('StdNoPIDsVeloPions', Particle='pion')
    ms_velo_pions.Input = ms_all_protos.Output

    # NOTE: These two lines are needed to select particles in VELO only.
    # NOTE: DARK MAGIC.
    trackSelector(ms_velo_pions, trackTypes=['Velo'])
    updateDoD(ms_velo_pions)

    DaVinci().appendToMainSequence([ms_all_protos, ms_velo_pions])
    ```


## `TupleToolSLTruth`
The truth-matching is done with a `getMCParticle` class method, which is defined as following:

```cpp
const LHCb::MCParticle* TupleToolSLTruth::getMCParticle(
    const LHCb::Particle* P ) {
  const LHCb::MCParticle* mcp( NULL );
  if ( P ) {
    // assignedPid = P->particleID().pid();
    if ( msgLevel( MSG::VERBOSE ) )
      verbose() << "Getting related MCP to " << P << endmsg;
    for ( std::vector<IParticle2MCAssociator*>::const_iterator iMCAss =
              m_p2mcAssocs.begin();
          iMCAss != m_p2mcAssocs.end(); ++iMCAss ) {
      mcp = ( *iMCAss )->relatedMCP( P );
      if ( mcp ) break;
    }
    if ( msgLevel( MSG::VERBOSE ) ) verbose() << "Got mcp " << mcp << endmsg;
  }
  return mcp;
}
```

Here it is trying to use the following MC associators in order:

- `DaVinciSmartAssociator`
- `MCMatchObjP2MCRelator`

And if one of them return a non-empty match, it will return that match right away.

!!! info
    These accociators are derived classes of `Particle2MCAssociatorBase`, which
    is defined in the `Phys` project in the
    `Phys/DaVinciMCKernel/Kernel/Particle2MCAssociatorBase.h` file.

!!! info
    For more info on MC truth-matching, take a look at [this article](../../technical_concepts/truth_matching.md).
