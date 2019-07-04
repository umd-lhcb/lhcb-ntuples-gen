This project generates ntuples (`.root` files) in **2 steps**:

1. Use `DaVinci` to generate ntuples from raw data (`.dst` files).
2. Use `babymaker` frame work to do slimming, skimming, and additional
   calculation on previous ntuples, generating new ntuples.
