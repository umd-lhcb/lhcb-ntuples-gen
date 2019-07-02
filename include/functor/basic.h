// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Tue Jul 02, 2019 at 05:14 PM -0400

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

template <typename T1, typename T2>
T1 SUM(T1 x, T2 y) {
  return x + static_cast<T1>(y);
}

#endif
