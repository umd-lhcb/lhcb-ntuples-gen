// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Sat Feb 12, 2022 at 04:26 PM -0500
//
// NOTE: The particle masses and IDs are obtained from here:
//   https://gitlab.cern.ch/lhcb-conddb/DDDB/-/blob/master/param/ParticleTable.txt

#pragma once

#include "unit.h"

#define PDG_M_B0 5279.64 * MeV
#define PDG_M_Dst 2010.26 * MeV
#define PDG_M_D0 1864.83 * MeV

#define PDG_ID_B0 511
#define PDG_ID_Bu 521
#define PDG_ID_Bs 531
#define PDG_ID_mu 13
#define PDG_ID_tau 15
#define PDG_ID_Dst 413
#define PDG_ID_Dst0 423
#define PDG_ID_Dst0_s 433
#define PDG_ID_D 411
#define PDG_ID_D0 421
#define PDG_ID_Ds 431
#define PDG_ID_D0st 10411
#define PDG_ID_D0st_0 10421
#define PDG_ID_D0st_s 10431
#define PDG_ID_D1 10413
#define PDG_ID_D1_0 10423
#define PDG_ID_D1_s 20433
#define PDG_ID_D1p 20413
#define PDG_ID_D1p_0 20423
#define PDG_ID_D1p_s 10433
#define PDG_ID_D2st 415
#define PDG_ID_D2st_0 425
#define PDG_ID_D2st_s 435
#define PDG_ID_Dst2S 100413
#define PDG_ID_Dst2S_0 100423
#define PDG_ID_D2S 100411
#define PDG_ID_D2S_0 100421
#define FAKE_ID_D2750 PDG_ID_D2st
#define FAKE_ID_D2750_0 PDG_ID_D2st_0
#define FAKE_ID_D3000 PDG_ID_D1
#define FAKE_ID_D3000_0 PDG_ID_D1_0
