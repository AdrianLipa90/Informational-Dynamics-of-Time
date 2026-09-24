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



/--
FSI.02 local-to-global cocycle direction. A globally potentialized transition
field has exact identity loops and satisfies the ordered triple-overlap
composition law. The group laws are passed explicitly so the theorem stays
dependency-free and the source repository keeps the interpretation of the
transition algebra.
-/
def transitionFromPotential {G X : Type}
    (mul : G → G → G)
    (inv : G → G)
    (p : X → G) (a b : X) : G :=
  mul (p b) (inv (p a))

theorem transitionFromPotential_refl
    {G X : Type}
    (mul : G → G → G)
    (inv : G → G)
    (one : G)
    (hMulInv : ∀ x : G, mul x (inv x) = one)
    (p : X → G) (a : X) :
    transitionFromPotential mul inv p a a = one := by
  exact hMulInv (p a)

theorem transitionFromPotential_cocycle
    {G X : Type}
    (mul : G → G → G)
    (inv : G → G)
    (one : G)
    (hAssoc : ∀ x y z : G, mul (mul x y) z = mul x (mul y z))
    (hInvMul : ∀ x : G, mul (inv x) x = one)
    (hOneMul : ∀ x : G, mul one x = x)
    (p : X → G) (a b c : X) :
    mul (transitionFromPotential mul inv p b c)
        (transitionFromPotential mul inv p a b) =
      transitionFromPotential mul inv p a c := by
  unfold transitionFromPotential
  rw [hAssoc]
  rw [← hAssoc (inv (p b)) (p b) (inv (p a))]
  rw [hInvMul]
  rw [hOneMul]



/--
FSI.03 IDT-side denominator-cleared positive-ray invariant. For a normalized
shape coordinate q_i / q_sum, common positive scaling multiplies numerator and
denominator by the same factor. ratioEquivalent records equality of ratios by
cross multiplication, without introducing division into this core theorem.
-/
def ratioEquivalent (a b c d : Nat) : Prop :=
  a * d = c * b

theorem commonScale_preserves_ratio
    (lambda qi qsum : Nat) :
    ratioEquivalent (lambda * qi) (lambda * qsum) qi qsum := by
  unfold ratioEquivalent
  simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

end Formal
