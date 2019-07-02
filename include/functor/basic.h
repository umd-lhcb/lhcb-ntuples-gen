// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Jul 02, 2019 at 03:28 AM -0400

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

template <typename T1, typename T2>
T1 SUM(T1 x, T2 y) {
  auto y1 = static_cast<T1>(y);
  return x + y1;
}

#endif
