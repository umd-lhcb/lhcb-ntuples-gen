// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Sat Sep 07, 2019 at 01:24 PM -0400

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

template <typename T>
T PROD(T x, T y) {
  return x*y;
}


#endif
