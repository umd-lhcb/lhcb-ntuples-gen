// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Sep 21, 2020 at 03:26 PM +0800

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

#include <TMath.h>
#include <TROOT.h>

#include <vector>

// Basic arithmetic ////////////////////////////////////////////////////////////

template <class T>
T ABS(T num) {
  return TMath::Abs(num);
}

// Boolean /////////////////////////////////////////////////////////////////////

Bool_t VEC_ALL_TRUE(std::vector<Bool_t>& vec) {
  return std::all_of(vec.begin(), vec.end(), [](Bool_t v) { return v; });
}

Bool_t VEC_ALL_FALSE(std::vector<Bool_t>& vec) {
  return std::all_of(vec.begin(), vec.end(), [](Bool_t v) { return !v; });
}

Bool_t VEC_AND(std::vector<Bool_t>& vec) {
  return std::find(vec.begin(), vec.end(), false) == vec.end();
}

Bool_t VEC_OR(std::vector<Bool_t>& vec) {
  return std::find(vec.begin(), vec.end(), true) != vec.end();
}

template <class T>
Bool_t VEC_OR_EQ(std::vector<T>& vec, T expr) {
  for (auto v : vec) {
    if (expr == v) return true;
  }
  return false;
}

// Units ///////////////////////////////////////////////////////////////////////

template <typename T>
T GEV(T x) {
  return x / 1000;
}

template <typename T>
T GEV2(T x) {
  return GEV(GEV(x));
}

#endif
