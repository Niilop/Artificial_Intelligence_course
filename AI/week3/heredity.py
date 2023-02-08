import csv
import itertools
import sys

import numpy as np

PROBS = {

    # Unconditional probabilities for having gene
    "gene": { 
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: { 
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    #people = load_data("data/family0.csv")
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)


    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    sub_probabilities = []
    for p in people:


        gene = check_gene(p,one_gene,two_genes)
        gene_p = PROBS["gene"][gene]

        if people[p]["mother"] != None:
            #print(p, ("is a child"))

            mother = people[p]["mother"]
            father = people[p]["father"]

            mother_gene = check_gene(mother,one_gene,two_genes)
            father_gene = check_gene(father, one_gene, two_genes)

            #print(p, "'s mother gene is", mother_gene)
            #print(p, "'s father gene is", father_gene)

            if (gene == 1):
                # either one parent gives one
                from_m = can_get_gene(mother_gene) * cannot_get_gene(father_gene)
                from_f = can_get_gene(father_gene) * cannot_get_gene(mother_gene)

                gene_p = from_f + from_m

            if (gene == 2):
                # both parents give one
                gene_p = can_get_gene(mother_gene) * can_get_gene(father_gene)
            if (gene == 0):
                # neither parents give one
                gene_p = cannot_get_gene(mother_gene) * cannot_get_gene(father_gene)

        if p in have_trait:
            #print(p, "has a trait")
            trait_p = PROBS["trait"][gene][True]
        if p not in have_trait:
            #print(p, "has no trait")
            trait_p = PROBS["trait"][gene][False]

        sub_prob = gene_p * trait_p
        sub_probabilities.append(sub_prob)

    joint_p = 1
    for val in sub_probabilities:

        joint_p *= val


    return joint_p

def check_gene(person, one_gene, two_genes,):

    if person in one_gene:
        #print(person, "has one gene")
        gene = 1

    if person in two_genes:
        #print(person, "has two genes")
        gene = 2

    if person not in one_gene and person not in two_genes:
        #print(person, "has no gene")
        gene = 0
    return gene

def can_get_gene(parent_gene):

    if (parent_gene == 0):
        chance = 0.01
    if (parent_gene == 1):
        chance = 0.50
    if (parent_gene == 2):
        chance = 0.99

    return chance

def cannot_get_gene(parent_gene):

    if (parent_gene == 0):
        chance = 0.99
    if (parent_gene == 1):
        chance = 0.50
    if (parent_gene == 2):
        chance = 0.01
    return chance

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:

        gene = check_gene(person, one_gene, two_genes)

        # Update gene
        probabilities[person]["gene"][gene] += p

        # Update trait
        if person in have_trait:
            probabilities[person]["trait"][True] += p

        if person not in have_trait:
            probabilities[person]["trait"][False] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        probabilities[person]["gene"]=normalize_dict(probabilities[person]["gene"])
        probabilities[person]["trait"]=normalize_dict(probabilities[person]["trait"])

def normalize_dict(dict):
    values = list(dict.values())
    total = sum(values)
    normalized_values = [value / total for value in values]

    return {key: normalized_values[index] for index, key in enumerate(dict.keys())}

if __name__ == "__main__":
    main()
