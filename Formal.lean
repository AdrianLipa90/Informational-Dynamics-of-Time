import Std

namespace Formal

/--
Serial realized-history successor on prefix indices.
This is an order/index theorem only; physical time, memory dynamics and
retrodiction remain separately typed IDT claims.
-/
def historySuccessor (k n : Nat) : Nat := n + k

theorem historySuccessor_injective (k : Nat) :
    Function.Injective (historySuccessor k) := by
  intro a b h
  exact Nat.add_right_cancel h

theorem historySuccessor_preserves_lt
    (k a b : Nat) (h : a < b) :
    historySuccessor k a < historySuccessor k b := by
  exact Nat.add_lt_add_right h k

theorem initialHistoryIndex_not_in_shiftedRange
    (k i : Nat) (h : i < k) :
    ¬ ∃ n : Nat, historySuccessor k n = i := by
  rintro ⟨n, hn⟩
  have hk : k ≤ historySuccessor k n := by
    simpa [historySuccessor, Nat.add_comm] using (Nat.le_add_left k n)
  have hlt : i < historySuccessor k n := Nat.lt_of_lt_of_le h hk
  rw [hn] at hlt
  exact Nat.lt_irrefl i hlt

/-- Append-only persistence preserves the complete earlier finite lineage. -/
def appendHistory {α : Type} (history suffix : List α) : List α :=
  history ++ suffix

theorem appendHistory_preserves_prefix
    {α : Type} (history suffix : List α) :
    (appendHistory history suffix).take history.length = history := by
  simp [appendHistory]

theorem appendHistory_length
    {α : Type} (history suffix : List α) :
    (appendHistory history suffix).length = history.length + suffix.length := by
  simp [appendHistory]


/-- Repeated lifted phase doubling before quotienting by a phase period. -/
def doubleIter : Nat → Nat → Nat
  | 0, q => q
  | k + 1, q => doubleIter k (2 * q)

theorem doubleIter_eq_pow_two (k q : Nat) :
    doubleIter k q = (2 ^ k) * q := by
  induction k generalizing q with
  | zero =>
      simp [doubleIter]
  | succ k ih =>
      simp [doubleIter, ih, Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

/--
An accelerated odd block with a halving exponent a corresponds to a+1
applications of the source doubling operator on the lifted phase coordinate.
The quotient modulo the physical/projective phase period remains a separate
source-level operation.
-/
theorem acceleratedBlock_phase_exponent (a q : Nat) :
    doubleIter (a + 1) q = (2 ^ (a + 1)) * q := by
  exact doubleIter_eq_pow_two (a + 1) q

end Formal
