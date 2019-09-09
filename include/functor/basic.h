// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Mon Sep 09, 2019 at 02:49 AM -0400

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

// Arithmetic //////////////////////////////////////////////////////////////////

template <typename T>
T SUB(T x, T y) {
  return x - y;
}

template <typename T>
T PROD(T x, T y) {
  return x * y;
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
