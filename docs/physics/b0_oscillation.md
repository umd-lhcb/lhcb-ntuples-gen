$B_0$ oscillation refers to the fact some of the $B_0$ oscillate into
$\bar{B_0}$ before they decay.

For real data reconstruction, this doesn't require additional consideration,
as we only know the quark content of the $B$ mesons, be it $B_0$ or $\bar{B_0}$,
before they decay.

However, for MC truth reconstruction, we are concerned about the initial states
of the $B$ mesons. Instead of naively writing decay descriptors like this:
```python
'${b0}[B~0 -> ${dst}(D*(2010)+ -> ${d0}(D0 -> ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu-]CC'
```

We need to take $B_0$ oscillation into account:
```python
'('
'${b0}[B~0 => ${dst}(D*(2010)+ => ${d0}(D0 => ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu- ${anu_mu}nu_mu~]CC'
'||'
'${b0}[B0 => ${dst}(D*(2010)+ => ${d0}(D0 => ${k}K- ${pi}pi+) ${spi}pi+) ${mu}mu- ${anu_mu}nu_mu~]CC'
')'
```
