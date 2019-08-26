## `TIS` functor
`TIS` is a (undocumented) `LoKi` functor， and it stands for _Trigger
Independent Signal_. There's another similar term: _TOS: Trigger On Signal_.

### Functor usage
```
TIS(<trigger_line_to_look>, <trigger_decision_storage_location>)
```

!!! note
    `<trigger_decision_storage_location>` is a `TES` location

### An example from _lhcb-ana-2014-052-v2r1_

```python
INTREE((ABSID == 'mu+') & (TIS('L0.*', 'L0TriggerTisTos')))
```

The line above should be interpreted as following:

1. In the decay tree, find a $\mu$.
2. We look over all `L0.*` trigger lines with `TES` `L0TriggerTisTos`, and
   require to have a trigger independent signal:
    - Since we are triggering on $\mu$, this requires that the trigger cannot
      be due to the $\mu$.
    - Also note that the whole decay tree is just a $\mu$ and a $D$, so it
      means that we are either TOS on $D$, TIS in the **whole** event, or both.
