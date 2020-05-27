// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Wed May 27, 2020 at 04:23 AM +0800

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

#include <cstdlib>

// Arithmetic //////////////////////////////////////////////////////////////////

template <typename T>
T SUB(T x, T y) {
  return x - y;
}

template <typename T>
T PROD(T x, T y) {
  return x * y;
}

template <typename T>
T ABS(T x) {
  return std::abs(x);
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
