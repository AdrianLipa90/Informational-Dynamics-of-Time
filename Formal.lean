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

theorem historySuccessor_strictMono (k : Nat) :
    StrictMono (historySuccessor k) := by
  intro a b h
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

end Formal
