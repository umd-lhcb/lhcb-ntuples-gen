// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Thu Sep 05, 2019 at 04:06 PM -0400

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

template <typename T>
T GEV(T x) {
  return x / 1000;
}

template <typename T>
T GEV2(T x) {
  return GEV(GEV(x));
}

#endif
