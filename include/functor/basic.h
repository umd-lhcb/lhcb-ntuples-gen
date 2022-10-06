// Author: Yipeng Sun
// License: BSD 2-clause
// Last Change: Thu Oct 06, 2022 at 01:33 PM -0400

#pragma once

#include <TMath.h>

#include <vector>

// Basic arithmetic ////////////////////////////////////////////////////////////

template <typename T>
T ABS(T num) {
  return TMath::Abs(num);
}

template <typename T>
T LOG(T num) {
  return TMath::Log(num);
}

template <typename T>
T SQRT(T num) {
  return TMath::Sqrt(num);
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

template <typename T, typename... ARGS>
T MIN(T arg0, ARGS... args) {
  auto result = arg0;
  auto vec    = std::vector<T>{args...};
  for (auto val : vec)
    if (val < result) result = val;
  return result;
}

template <typename T>
Int_t SIGN(T num) {
  return static_cast<Int_t>(ABS(num) / num);
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

template <typename T>
Bool_t VEC_OR_EQ(std::vector<T>& vec, T expr) {
  for (auto v : vec) {
    if (expr == v) return true;
  }
  return false;
}

// Conditional /////////////////////////////////////////////////////////////////

template <typename T>
T IF(bool condition, T true_val, T false_val) {
  if (condition) return true_val;
  return false_val;
}

template <typename T, typename U>
T IF(bool condition, T true_val, U false_val) {
  if (condition) return true_val;
  return static_cast<T>(false_val);
}

template <typename T, typename U>
U IF_VAR_EXISTS(T var, U out) {
  return out;
}

template <typename T>
Bool_t IN_RANGE(T val, T lower, T upper, Bool_t closed = false) {
  if (closed) return val >= lower && val <= upper;
  return val > lower && val < upper;
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
      for (auto sub_comb : COMBINATION(tot_size, comb_size - 1, head + 1)) {
        sub_comb.emplace(sub_comb.begin(), head);
        result.push_back(sub_comb);
      }
    } else
      result.push_back(std::vector<int>{head});
  }

  return result;
}

// Vector-related //////////////////////////////////////////////////////////////

template <typename T, typename... ARGS>
std::vector<T> BUILD_VEC(T const& arg0, ARGS const&... args) {
  return std::vector<T>{{arg0, args...}};
}

template <typename T>
T EXTRACT_ELEM(std::vector<T> vec, size_t idx) {
  return vec[idx];
}

// Type coercion ///////////////////////////////////////////////////////////////

template <typename T, typename U>
T TO_TYPE(U src, T tgt) {
  return static_cast<T>(src);
}
