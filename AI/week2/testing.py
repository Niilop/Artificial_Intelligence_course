

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
        is_child = False
        gene = 0
        gene_p = 0
        trait_p = 0

        gene = check_gene(p,one_gene,two_genes)
        gene_p = PROBS["gene"][gene]
        print(p, "gene is ", gene)
        if people[p]["mother"] != None:
            #print(p, ("is a child"))
            is_child = True
            mother = people[p]["mother"]
            father = people[p]["father"]

            mother_gene = check_gene(mother,one_gene,two_genes)
            father_gene = check_gene(father, one_gene, two_genes)

            #print(p, "'s mother gene is", mother_gene)
            #print(p, "'s father gene is", father_gene)

            chance_m = 0
            chance_f = 0

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

        print(gene_p)
        sub_prob = gene_p * trait_p
        print(sub_prob)
        sub_probabilities.append(sub_prob)

    joint_p = 1
    for val in sub_probabilities:

        joint_p *= val


    return joint_p

def check_gene(person, one_gene, two_genes,):
    gene = 0
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

people = {
'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}
one_gene = ("")
two_genes = ("")
have_trait = ("James")

print(joint_probability(people, one_gene, two_genes, have_trait))