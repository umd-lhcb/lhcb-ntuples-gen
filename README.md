# lhcb-ntuples-gen [![github CI](https://github.com/umd-lhcb/lhcb-ntuples-gen/workflows/CI/badge.svg?branch=master)](https://github.com/umd-lhcb/lhcb-ntuples-gen/actions?query=workflow%3ACI)

This is a special branch for preserving Manuel's trigger emulation study.
To fully run the study, follow these steps (copy as-is):

1. `git submodule update`
2. `nix develop`
3. `make install-dep`
4. `(cd ./studies/ntuple-RDX_l0_hadron_tos_training_sample && ./gen_l0hadron_samples.py)`
5. `(cd ./studies/l0hadron_train_bdt && ./train_l0hadron_bdt.py)`
6. `(cd ./studies/l0hadron_train_xgb && ./train_l0hadron_xgb.py)`
7. `(cd ./studies/trigger_emulation-l0_hadron_tos_bdt_debug && ./plot_l0hadron_bdt_debug.py)`
8. `(cd ./studies/trigger_emulation-l0_hadron_tos_xgb_debug && ./plot_l0hadron_xgb_eff.py)`

The generated plots are located in:

- `studies/l0hadron_train_bdt`
- `studies/l0hadron_train_xgb`
