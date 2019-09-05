// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Thu Sep 05, 2019 at 03:39 AM -0400

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

template <typename T1, typename T2>
T1 SUM(T1 x, T2 y) {
  return x + static_cast<T1>(y);
}

template <typename T>
T GEV(T x) {
  return x / 1000;
}

template <typename T>
T GEV2(T x) {
  return GEV(GEV(x));
}

#endif
