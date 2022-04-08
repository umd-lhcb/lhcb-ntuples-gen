## Generic

- LHCb [DeveloperKit](https://lhcb.github.io/DevelopKit/)


## Trigger Configuration Key (TCK)

- This [TWiki](https://twiki.cern.ch/twiki/bin/view/LHCb/TCK#TCKsh) explains
  briefly how to use `TCKsh` to study TCKs.
- This [starter kit page](https://lhcb.github.io/starterkit-lessons/second-analysis-steps/hlt-intro.html#exploring-a-tck-list-of-trigger-lines)
  provides some sample usage for `TCKsh`
- This [page](https://lbtriggerreport.cern.ch/reports/) has all TCK info for
  LHCb.

    !!! note
        This link have `.pdf` files that list all TCKs for a given period of
        time.

        For example, in the [2016 year-end report](https://lbtriggerreport.cern.ch/reports/2016/last_report_2016_6500_summary.pdf):

        - All TCKs in this period, such as `0x1138160E`, are listed in **page 6**.
        - TCK vs. fill number are listed in **page 18**. The fill number is related
          to time, but the relationship is unknown to us[^1].


[^1]: "us" refers to Yipeng Sun.


## Find particle masses used by the `LoKi` functors

The full mass table for a particular `DaVinci` version can be looked up
with[^2]:

```
lb-run DaVinci/<dv_version> dump_particle_properties | tee ParticleTable.txt
```

Alternatively, the latest mass table is available at [cern-gitlab](https://gitlab.cern.ch/lhcb-conddb/DDDB/-/blob/master/param/ParticleTable.txt)


[^2]: Suggested by Phoebe Hamilton.


## Notes on `pidcalib2`

A guide to `pidcalib2` can be found [here](https://gitlab.cern.ch/lhcb-rta/pidcalib2).

!!! example "usage of `--cut` and `--pid-cut`"
    Say `pidcalib2` is invoked like this:

    ```
    lb-conda pidcalib pidcalib2.make_eff_hists \
        --cut "A" --cut "B" \
        --pid-cut "PA" --pid-cut "PB"
    ```

    Then 2 histograms will be generated, with the following efficiencies:

    1. $\epsilon_1 = \frac{N(\text{A & B & PA})}{N(\text{A & B})}$
    2. $\epsilon_2 = \frac{N(\text{A & B & PB})}{N(\text{A & B})}$

    Note that all cuts supplied in all `--cut` flags are all applied first.
