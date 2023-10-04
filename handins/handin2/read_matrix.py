from collections import Counter

import numpy as np


def read_sequences(path: str) -> list[str]:
    with open(path, "r") as f:
        seqs = f.read()
    seqs = seqs.replace("\n", "").split(">")[1:]
    seqs = [x.split("bp")[1] for x in seqs]

    # check that all sequences have same length
    n_nucleotides = len(seqs[0])
    for s in seqs:
        if len(s) != n_nucleotides:
            raise Exception("Sequences have different lengths")

    return seqs


def main() -> None:
    seqs = read_sequences("handins/handin2/sequences.fa")

    # map each character in each sequence into a integer representation
    nucleotide_mapping = {"A": 0, "C": 1, "G": 2, "T": 3, ".": 4, "N": 5}
    mapped_seqs = []

    for s in seqs:
        s_mapped = [nucleotide_mapping[x] for x in [x for x in s]]
        mapped_seqs.append(s_mapped)
    mapped_seqs = np.array(mapped_seqs)

    # filter out unused columns because of "."
    filtered_seqs = []
    for col in range(mapped_seqs.shape[1]):
        col_data = mapped_seqs[:, col]
        if (4 in col_data) or (5 in col_data):
            continue
        else:
            filtered_seqs.append(col_data)

    filtered_seqs = np.array(filtered_seqs)

    base_seq = []
    mutant_seq = []
    for c in filtered_seqs:
        counter = Counter(c)
        base_seq.append(max(counter, key=counter.get))
        mutant_seq.append(min(counter, key=counter.get))

    print("Using the mapping above, the sequences are:")
    print(f"Base Sequence: {base_seq}\nMutant Sequence: {mutant_seq}")

    # create matrix representation:
    final_matrix = []

    for i in range(len(seqs)):
        return_l = []
        for v, base in zip(filtered_seqs[:, i], base_seq):
            if v != base:
                return_l.append(1)  # segregating site
            else:
                return_l.append(0)

        final_matrix.append(return_l)

    final_matrix = np.array(np.array(final_matrix))

    print(f"The final matrix is: {final_matrix}")


if __name__ == "__main__":
    main()
