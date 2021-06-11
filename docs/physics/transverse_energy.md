# Transverse energy $E_T$

Transverse energy $E_T$ is defined as (taken from p. 4 of [this paper](https://arxiv.org/pdf/2008.11556.pdf)):

\[
E_T = E \sin\theta = \sqrt{m^2 + p^2} \sin\theta
\]

In the massless limit:

\[
E_T \approx \sqrt{p^2} \sin\theta = p_T
\]

## $E_T$-related variables in `TupleToolL0Calo`

In [`TupleToolL0Calo`](https://gitlab.cern.ch/lhcb/Analysis/-/blob/run2-patches/Phys/DecayTreeTupleTrigger/src/TupleToolL0Calo.cpp), there's 3 variables that are related to $E_T$:

- `realET`
- `TriggerET`
- `TriggerHCALET`

!!! info
    For the rest of the article, assume we use `TupleToolL0Calo` on HCAL.

### `realET`

This is $E_T$ computed at HCAL:

```cpp
trackET = TMath::Sqrt( TMath::Power( m_part2calo->caloState().x(), 2 ) + TMath::Power( m_part2calo->caloState().y(), 2 ) ) /
          TMath::Sqrt( TMath::Power( m_part2calo->caloState().x(), 2 ) + TMath::Power( m_part2calo->caloState().y(), 2 ) +
                       TMath::Power( m_part2calo->caloState().z(), 2 ) ) *
          TMath::Sqrt( TMath::Power( m_part2calo->caloState().p(), 2 ) + TMath::Power( P->measuredMass(), 2 ) );

// ...

test &= tuple->column( prefix + "_L0Calo_HCAL_realET", trackET );
```

Conceptually, it really is just:

\[
\sqrt{p^2 + m^2} \sin\theta
\]

But here both $p$ and $m$ are measured, not MC truth. I'm having trouble giving
it a good name.

!!! question
    Naively I'd call it tracker $E_T$, but from the code it is the $E_T$ at HCAL,
    and HCAL is not adjacent to a tracker: Before HCAL it is the ECAL, after HCAL
    Muon stations.

    But it really is not MC truth $E_T$ either, because we are using
    `measuredMass`.


### `TriggerET`

!!! info "Before you proceed"
    `TriggerET` and `TriggerHCALET` are defined in one block:

    ```cpp
    double triggerET( -1. ), triggerHCALET( -1. ), xtrigger( 0. ), ytrigger( 0. );
    if ( m_fillTriggerEt ) { triggerET = getAssociatedCluster( triggerHCALET, xtrigger, ytrigger ); }

    // ...

    test &= tuple->column( prefix + "_L0Calo_HCAL_TriggerET", triggerET );
    test &= tuple->column( prefix + "_L0Calo_HCAL_TriggerHCALET", triggerHCALET );
    ```

This is the _maximum_ $E_T$ measured by **the whole detector** for all L0
hadron candidates. Note that:

1. For the track, we find the center cell it supposed to hit based on its
    projectile, as well as the 3x3 neighbor cells, denote it track cells.

2. For each hadron candidate, we find the HCAL cell it hits as well as the nearby
    top, right, and top right cells. Here we have a total of 2x2 cells, denote it
    candidate cells.

3. Check if there's any overlap between the candidate cells and the track cells.
    If there is overlap, use this candidate's $E_T$ as track $E_T$ if
    $E_{T_{cand}} > E_{T_{prev}}$.

4. Repeat this process for all L0 hadron candidates.

```cpp
// First get the CALO cells in the 3x3 cluster around the track projection
std::vector<LHCb::CaloCellID> cells3x3;

if ( m_part2calo->isValid() ) {  // 'm_part2calo' is the track
const LHCb::CaloCellID centerCell = m_part2calo->caloCellID();
cells3x3.push_back( centerCell );
BOOST_FOREACH ( LHCb::CaloCellID cell, m_caloDe->neighborCells( centerCell ) ) { cells3x3.push_back( cell ); };
}
std::sort( cells3x3.begin(), cells3x3.end() );

// loop over the L0 candidates
LHCb::L0CaloCandidates* candidates = getIfExists<LHCb::L0CaloCandidates>( m_location );
if ( m_calo == "HCAL" ) typeToCheck = L0DUBase::CaloType::Hadron;

LHCb::L0CaloCandidates::iterator cand;
double                           result = -1.;  // 'result' is TriggerET

for ( cand = candidates->begin(); candidates->end() != cand; ++cand ) {
  LHCb::L0CaloCandidate* theCand = ( *cand );
  if ( theCand->type() == typeToCheck ) {
    LHCb::CaloCellID cell1, cell2, cell3, cell4;
    cell1 = theCand->id();
    cell2 = LHCb::CaloCellID( cell1.calo(), cell1.area(), cell1.row() + 1, cell1.col() );
    cell3 = LHCb::CaloCellID( cell1.calo(), cell1.area(), cell1.row(), cell1.col() + 1 );
    cell4 = LHCb::CaloCellID( cell1.calo(), cell1.area(), cell1.row() + 1, cell1.col() + 1 );
    if ( std::binary_search( cells3x3.begin(), cells3x3.end(), cell1 ) ||
         std::binary_search( cells3x3.begin(), cells3x3.end(), cell2 ) ||
         std::binary_search( cells3x3.begin(), cells3x3.end(), cell3 ) ||
         std::binary_search( cells3x3.begin(), cells3x3.end(), cell4 ) ) {
      if ( theCand->et() > result ) {
        result   = theCand->et();  // This is the key line!

        // ...
      }
    }
  }
}
```


### `TriggerHCALET`

This is the _maximum_ $E_T$ measured by **HCAL only** for all hadron
candidates associated with the track. Note that:

The procedure is similar `TriggerET`, the only difference is:
instead of using `theCand->et()`, we find the associated HCAL cells and readout
the ADC values associated with the hadron candidate and convert it to energy.


```cpp
// Compute the HCAL energy of this cluster

// ...

hcal_energy                              = 0.;  // 'hcal_energy' is TriggerHCALET
const std::vector<LHCb::L0CaloAdc>& adcs = m_adcsHcal->adcs();
for ( std::vector<LHCb::L0CaloAdc>::const_iterator itAdc = adcs.begin(); adcs.end() != itAdc; ++itAdc ) {
  LHCb::CaloCellID id = ( *itAdc ).cellID();
  if ( ( id == cell1 ) || ( id == cell2 ) || ( id == cell3 ) || ( id == cell4 ) )
    hcal_energy += ( *itAdc ).adc();
}
if ( hcal_energy > 255 ) hcal_energy = 255;
hcal_energy = hcal_energy * ( m_caloDe->L0EtGain() );
```
