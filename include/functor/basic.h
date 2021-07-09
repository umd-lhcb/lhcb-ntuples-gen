// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Fri Jul 09, 2021 at 09:45 PM +0200

#ifndef _LNG_FUNCTOR_BASIC_H_
#define _LNG_FUNCTOR_BASIC_H_

#include <TMath.h>

#include <vector>

// Basic arithmetic ////////////////////////////////////////////////////////////

template <class T>
T ABS(T num) {
  return TMath::Abs(num);
}

template <typename T, typename... ARGS>
T MAG(T arg0, ARGS... args) {
  auto result = arg0 * arg0;
  auto vec    = std::vector<T>{args...};
  for (auto val : vec) result += val * val;
  return TMath::Sqrt(result);
}

template <typename T, typename... ARGS>
T MAX(T arg0, ARGS... args) {
  auto result = arg0;
  auto vec    = std::vector<T>{args...};
  for (auto val : vec)
    if (val > result) result = val;
  return result;
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

// Index permutation ///////////////////////////////////////////////////////////

std::vector<std::vector<int> > COMBINATION(int tot_size, int comb_size,
                                           int head_idx = 0) {
  std::vector<std::vector<int> > result;

  for (int head = head_idx; head <= tot_size - comb_size; head++) {
    if (comb_size > 1) {
      for (auto subComb : COMBINATION(tot_size, comb_size - 1, head + 1)) {
        subComb.emplace(subComb.begin(), head);
        result.emplace_back(subComb);
      }
    } else
      result.emplace_back(std::vector<int>{head});
  }

  return result;
}

// Vector construction /////////////////////////////////////////////////////////
template <typename T, typename... ARGS>
std::vector<T> BUILD_VEC(T const& arg0, ARGS const&... args) {
  return std::vector<T>{{arg0, args...}};
}

// Boolean /////////////////////////////////////////////////////////////////////
template <typename T>
T IF(bool condition, T true_val, T false_val) {
  if (condition) return true_val;
  return false_val;
}

#endif
