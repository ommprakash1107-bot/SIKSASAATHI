import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import textwrap
import ollama

MODEL = "qwen2.5:3b"   # Gemma test ke baad yahan "gemma4:e2b" likh sakte hain

# ---------------------------------------------------------------
# CONCEPT GRAPH (yahi tutor ka "dimaag" hai).
# Har concept: kya seekhna hai, uske pehle kya aana chahiye (prereqs),
# ek jaanchne wala sawal (probe), samjhane wala verified text, aur check sawal.
# NOTE: Yeh text NCERT Class 12 Biology ke do chapters ke hisaab se likha gaya hai:
#   Chapter 4 - Principles of Inheritance and Variation
#   Chapter 5 - Molecular Basis of Inheritance
# Kisi teacher se ek baar verify zaroor karwaiye.
# ---------------------------------------------------------------
CH4 = "Principles of Inheritance and Variation"
CH5 = "Molecular Basis of Inheritance"

G = {
    # ===========================================================
    # CHAPTER 4 - PRINCIPLES OF INHERITANCE AND VARIATION
    # ===========================================================
    "inheritance_variation": {
        "chapter": CH4,
        "title": "Inheritance aur variation",
        "aliases": ["inheritance and variation", "what is inheritance", "heredity",
                    "what is variation", "variation kya hai", "inheritance kya hai"],
        "prereqs": [],
        "explain": ("Inheritance is the process by which characters are passed from parents to "
                    "their offspring. It is the basis of heredity. Variation is how much the "
                    "offspring differ from their parents. Even thousands of years ago, humans used "
                    "the natural variation in plants and animals to breed useful types, for example "
                    "the Sahiwal cow of Punjab, but they did not know the scientific reason behind it."),
        "probe_q": "What do we call the process by which characters pass from parents to offspring?",
        "probe_a": "inheritance",
        "check_q": "What is variation?",
        "check_a": "the degree or amount by which offspring differ from their parents",
        "search": "inheritance variation heredity progeny differ from parents",
    },
    "mendel_experiments": {
        "chapter": CH4,
        "title": "Mendel ke pea plant experiments",
        "aliases": ["mendel", "garden pea", "pea plant", "true breeding", "true-breeding",
                    "seven traits", "contrasting traits", "mendels experiment"],
        "prereqs": ["inheritance_variation"],
        "explain": ("Gregor Mendel did hybridisation experiments on garden pea plants for seven years "
                    "(1856 to 1863). He was the first to use statistics and mathematics on a biology "
                    "problem, and he used a large number of plants, so his results were reliable. "
                    "He chose 14 true-breeding pea varieties, forming 7 pairs that differed in only one "
                    "character, such as tall or dwarf stem, round or wrinkled seed, and yellow or green seed. "
                    "A true-breeding line is one that keeps showing the same trait for many generations "
                    "of self-pollination."),
        "probe_q": "On which plant did Mendel do his experiments?",
        "probe_a": "the garden pea plant",
        "check_q": "What is a true-breeding line?",
        "check_a": "a line that shows the same stable trait for several generations after continuous self-pollination",
        "search": "Mendel garden pea hybridisation true-breeding seven pairs contrasting traits",
    },
    "gene_allele": {
        "chapter": CH4,
        "title": "Gene, allele, genotype aur phenotype",
        "aliases": ["allele", "alleles", "genotype", "phenotype", "homozygous", "heterozygous",
                    "what is a gene", "gene kya hai", "mendels factors"],
        "prereqs": ["mendel_experiments"],
        "explain": ("Mendel said that some 'factors' pass unchanged from parents to offspring through "
                    "the gametes. Today we call these factors genes; genes are the units of inheritance. "
                    "Genes that code for a pair of contrasting traits are called alleles, like T for tall "
                    "and t for dwarf. When both alleles are the same (TT or tt) the plant is homozygous, and "
                    "when they are different (Tt) it is heterozygous. The allele combination (TT, Tt, tt) "
                    "is the genotype, and the visible trait (tall or dwarf) is the phenotype."),
        "probe_q": "What did Mendel call the units that pass from parents to offspring, and what do we call them today?",
        "probe_a": "factors; today they are called genes",
        "check_q": "A plant has the genotype Tt. Is it homozygous or heterozygous?",
        "check_a": "heterozygous",
        "search": "factors genes alleles genotype phenotype homozygous heterozygous",
    },
    "monohybrid_cross": {
        "chapter": CH4,
        "title": "Monohybrid cross (ek gene ki inheritance)",
        "aliases": ["monohybrid", "inheritance of one gene", "one gene", "3:1", "1:2:1",
                    "f1 generation", "f2 generation"],
        "prereqs": ["gene_allele"],
        "explain": ("In a monohybrid cross, plants differing in only one character are crossed, "
                    "for example a true-breeding tall plant (TT) with a dwarf plant (tt). All the F1 plants "
                    "were tall (Tt). When the F1 plants were self-pollinated, the F2 generation had 3/4 tall "
                    "and 1/4 dwarf plants, a phenotypic ratio of 3:1. The genotypic ratio in F2 is "
                    "1 TT : 2 Tt : 1 tt. The traits never blended, so no plant was of in-between height."),
        "probe_q": "When a pure tall pea plant is crossed with a pure dwarf plant, what do all the F1 plants look like?",
        "probe_a": "all F1 plants are tall",
        "check_q": "What are the phenotypic and genotypic ratios in the F2 generation of a monohybrid cross?",
        "check_a": "phenotypic ratio 3:1 and genotypic ratio 1:2:1",
        "search": "monohybrid cross F1 tall F2 3:1 ratio 1:2:1 genotypic",
    },
    "punnett_square": {
        "chapter": CH4,
        "title": "Punnett square",
        "aliases": ["punnett square", "punnett", "checker board", "checkerboard"],
        "prereqs": ["monohybrid_cross"],
        "explain": ("A Punnett square is a diagram, made by the British geneticist Reginald C. Punnett, "
                    "to work out all possible genotypes of offspring in a cross. The gametes of one parent "
                    "are written along the top and the gametes of the other parent down the left side. "
                    "Each box below is filled by combining one gamete from each side. For Tt x Tt, the "
                    "boxes give 1 TT, 2 Tt and 1 tt."),
        "probe_q": "In a Punnett square, what is written along the top row and the left column?",
        "probe_a": "the gametes of the two parents",
        "check_q": "Using a Punnett square, what genotypes do you get from crossing Tt with Tt?",
        "check_a": "1 TT, 2 Tt and 1 tt",
        "search": "Punnett square gametes probability genotypes offspring",
    },
    "law_of_dominance": {
        "chapter": CH4,
        "title": "Law of Dominance (pehla law)",
        "aliases": ["law of dominance", "dominance", "dominant", "recessive", "first law"],
        "prereqs": ["monohybrid_cross"],
        "explain": ("Mendel's first law is the Law of Dominance. It says: characters are controlled by "
                    "units called factors, factors occur in pairs, and in a dissimilar pair one factor "
                    "(dominant) hides the other (recessive). That is why a Tt plant is tall: T is dominant "
                    "and t is recessive. This law explains why only one parental trait appears in F1 and "
                    "why both appear in F2 in a 3:1 ratio."),
        "probe_q": "In a Tt pea plant, which allele is expressed in the appearance?",
        "probe_a": "T, the dominant allele (the plant is tall)",
        "check_q": "What are the three points of the Law of Dominance?",
        "check_a": "characters are controlled by factors, factors occur in pairs, and in a dissimilar pair one factor dominates the other",
        "search": "Law of Dominance factors occur in pairs dominant recessive",
    },
    "law_of_segregation": {
        "chapter": CH4,
        "title": "Law of Segregation (dusra law)",
        "aliases": ["law of segregation", "segregation", "second law", "purity of gametes"],
        "prereqs": ["monohybrid_cross"],
        "explain": ("Mendel's second law is the Law of Segregation. A parent has two alleles for a "
                    "character, but when gametes are formed the two alleles separate, so each gamete "
                    "gets only one allele. The alleles do not blend, which is why the hidden recessive "
                    "trait comes back unchanged in F2. A homozygous parent makes only one kind of gamete, "
                    "while a heterozygous parent makes two kinds in equal numbers."),
        "probe_q": "How many alleles of a gene does a single gamete carry?",
        "probe_a": "only one allele",
        "check_q": "What does the Law of Segregation say?",
        "check_a": "the two alleles of a pair separate during gamete formation so that each gamete receives only one of them",
        "search": "Law of Segregation alleles separate gamete formation one allele",
    },
    "test_cross": {
        "chapter": CH4,
        "title": "Test cross",
        "aliases": ["test cross", "testcross", "test crossing"],
        "prereqs": ["law_of_dominance", "punnett_square"],
        "explain": ("By looking at a tall plant, we cannot tell if its genotype is TT or Tt. "
                    "To find out, Mendel crossed it with a dwarf (homozygous recessive, tt) plant. "
                    "This is called a test cross. If all the offspring are tall, the plant was TT "
                    "(homozygous). If half are tall and half are dwarf (1:1 ratio), the plant was Tt "
                    "(heterozygous)."),
        "probe_q": "Can you tell whether a tall pea plant is TT or Tt just by looking at it?",
        "probe_a": "no, both TT and Tt look tall",
        "check_q": "In a test cross, the unknown plant is crossed with which type of plant, and what ratio shows that it was heterozygous?",
        "check_a": "with a homozygous recessive plant; a 1:1 ratio of dominant to recessive offspring shows it was heterozygous",
        "search": "test cross dominant phenotype crossed with recessive parent genotype",
    },
    "incomplete_dominance": {
        "chapter": CH4,
        "title": "Incomplete dominance",
        "aliases": ["incomplete dominance", "snapdragon", "dog flower", "antirrhinum", "pink flower"],
        "prereqs": ["law_of_dominance"],
        "explain": ("Sometimes the F1 looks in-between the two parents. This is incomplete dominance. "
                    "In the snapdragon (dog flower), a red flower (RR) crossed with a white flower (rr) "
                    "gives pink F1 flowers (Rr), because R is not fully dominant over r. In F2 the ratio "
                    "is 1 red : 2 pink : 1 white, so here the phenotypic and genotypic ratios are the same."),
        "probe_q": "In complete dominance, does the heterozygous Tt plant look like the TT parent or in-between?",
        "probe_a": "like the TT (dominant) parent",
        "check_q": "When red and white snapdragons are crossed, what is the colour of the F1 and what is the F2 ratio?",
        "check_a": "F1 is pink; F2 ratio is 1 red : 2 pink : 1 white",
        "search": "incomplete dominance snapdragon red white pink 1:2:1",
    },
    "dominance_concept": {
        "chapter": CH4,
        "title": "Dominance asal mein kya hai",
        "aliases": ["why are some alleles dominant", "concept of dominance", "why dominant",
                    "starch grain", "starch synthesis", "what is dominance"],
        "prereqs": ["law_of_dominance"],
        "explain": ("A gene carries information, for example to make an enzyme. A changed (modified) "
                    "allele may make a normal enzyme, a non-working enzyme, or no enzyme at all. If it makes "
                    "a non-working enzyme or none, the trait depends only on the normal allele, so the normal "
                    "allele behaves as dominant and the changed one as recessive. Dominance also depends on "
                    "which trait we look at: in pea seeds, Bb gives round seeds (B looks dominant) but "
                    "medium-sized starch grains (incomplete dominance)."),
        "probe_q": "In a Tt plant, which allele decides the appearance?",
        "probe_a": "the dominant allele T",
        "check_q": "Why does a modified allele often behave as recessive?",
        "check_a": "because it makes a non-functional enzyme or no enzyme, so the trait depends only on the normal unmodified allele",
        "search": "explanation of concept of dominance enzyme modified allele starch grain",
    },
    "codominance": {
        "chapter": CH4,
        "title": "Co-dominance (ABO blood group)",
        "aliases": ["codominance", "co dominance", "codominant", "co dominant", "blood group", "abo blood", "ab blood group"],
        "prereqs": ["law_of_dominance"],
        "explain": ("In co-dominance, the F1 shows the traits of both parents together. The ABO blood "
                    "group is the example. The gene I has three alleles: IA, IB and i. IA and IB make two "
                    "slightly different sugars on red blood cells, and i makes no sugar. IA and IB are both "
                    "dominant over i, but when IA and IB come together, both express, giving blood group AB. "
                    "There are 6 possible genotypes and 4 blood groups (A, B, AB and O)."),
        "probe_q": "In a heterozygote with complete dominance, how many of the two alleles show their effect?",
        "probe_a": "only one, the dominant allele",
        "check_q": "Why does a person with IA and IB alleles have blood group AB?",
        "check_a": "because IA and IB are co-dominant, so both express their own sugar together",
        "search": "co-dominance ABO blood group IA IB i alleles",
    },
    "multiple_alleles": {
        "chapter": CH4,
        "title": "Multiple alleles",
        "aliases": ["multiple alleles", "multiple allele", "three alleles"],
        "prereqs": ["codominance"],
        "explain": ("When a character is controlled by more than two alleles, they are called multiple "
                    "alleles. The ABO blood group gene has three alleles (IA, IB and i). But one person can "
                    "carry only two alleles, so multiple alleles can be seen only when we study a whole "
                    "population."),
        "probe_q": "How many alleles does the gene for ABO blood group have?",
        "probe_a": "three: IA, IB and i",
        "check_q": "Why can multiple alleles be found only through population studies?",
        "check_a": "because one individual can carry only two alleles",
        "search": "multiple alleles ABO blood group three alleles population",
    },
    "dihybrid_cross": {
        "chapter": CH4,
        "title": "Dihybrid cross (do genes ki inheritance)",
        "aliases": ["dihybrid", "inheritance of two genes", "two genes", "two characters", "9:3:3:1"],
        "prereqs": ["monohybrid_cross"],
        "explain": ("In a dihybrid cross, plants differing in two characters are crossed. Mendel crossed "
                    "round yellow seeds (RRYY) with wrinkled green seeds (rryy). All F1 seeds were round and "
                    "yellow (RrYy), so round and yellow are dominant. In F2 he got four types in the ratio "
                    "9 round yellow : 3 wrinkled yellow : 3 round green : 1 wrinkled green."),
        "probe_q": "What is the F2 phenotypic ratio in a monohybrid cross?",
        "probe_a": "3:1",
        "check_q": "What is the F2 phenotypic ratio in Mendel's dihybrid cross?",
        "check_a": "9:3:3:1",
        "search": "dihybrid cross RRYY rryy round yellow 9:3:3:1",
    },
    "independent_assortment": {
        "chapter": CH4,
        "title": "Law of Independent Assortment",
        "aliases": ["independent assortment", "law of independent assortment", "third law"],
        "prereqs": ["dihybrid_cross"],
        "explain": ("From dihybrid crosses, Mendel made his Law of Independent Assortment: when two pairs "
                    "of traits are combined in a hybrid, one pair segregates independently of the other pair. "
                    "So an RrYy plant makes four kinds of gametes, RY, Ry, rY and ry, each 1/4 of the total. "
                    "The 9:3:3:1 ratio is simply (3 round : 1 wrinkled) multiplied by (3 yellow : 1 green)."),
        "probe_q": "In a dihybrid cross, what is the F2 phenotypic ratio?",
        "probe_a": "9:3:3:1",
        "check_q": "How many kinds of gametes does an RrYy plant make, and what are they?",
        "check_a": "four kinds: RY, Ry, rY and ry",
        "search": "law of independent assortment segregation of one pair independent RY Ry rY ry",
    },
    "chromosomal_theory": {
        "chapter": CH4,
        "title": "Chromosomal Theory of Inheritance",
        "aliases": ["chromosomal theory", "sutton", "boveri", "rediscovery", "rediscovered",
                    "why mendel was not accepted", "why was mendel ignored"],
        "prereqs": ["law_of_segregation", "independent_assortment"],
        "explain": ("Mendel published his work in 1865, but it was ignored until 1900 because communication "
                    "was poor, his idea of discrete factors and his use of maths were not accepted, and he "
                    "could not show physical proof of factors. In 1900, de Vries, Correns and von Tschermak "
                    "rediscovered his results. Walter Sutton and Theodore Boveri saw that chromosomes behave "
                    "just like genes: both occur in pairs and separate during gamete formation. Sutton joined "
                    "this with Mendel's laws and called it the chromosomal theory of inheritance."),
        "probe_q": "During gamete formation, what happens to the two alleles of a gene?",
        "probe_a": "they separate (segregate), and each gamete gets only one",
        "check_q": "Who noticed that chromosomes behave like genes, and what did Sutton call this idea?",
        "check_a": "Walter Sutton and Theodore Boveri; Sutton called it the chromosomal theory of inheritance",
        "search": "chromosomal theory of inheritance Sutton Boveri rediscovered 1900",
    },
    "linkage_recombination": {
        "chapter": CH4,
        "title": "Linkage aur Recombination (Morgan)",
        "aliases": ["linkage", "linked genes", "recombination", "morgan", "drosophila",
                    "fruit fly", "sturtevant", "genetic map"],
        "prereqs": ["independent_assortment", "chromosomal_theory"],
        "explain": ("Thomas Hunt Morgan tested the chromosomal theory using the fruit fly Drosophila, which "
                    "has a short two-week life cycle and many offspring. In his dihybrid crosses, the F2 ratio "
                    "did not match 9:3:3:1 when two genes were on the same chromosome. He called the physical "
                    "association of genes on a chromosome 'linkage', and the making of new non-parental gene "
                    "combinations 'recombination'. Tightly linked genes, like white and yellow, showed only "
                    "1.3 per cent recombination, while white and miniature wing showed 37.2 per cent. His student "
                    "Alfred Sturtevant used recombination frequency to map genes on chromosomes."),
        "probe_q": "According to the Law of Independent Assortment, what F2 ratio do we expect in a dihybrid cross?",
        "probe_a": "9:3:3:1",
        "check_q": "What is the difference between linkage and recombination?",
        "check_a": "linkage is the physical association of genes on the same chromosome; recombination is the generation of non-parental gene combinations",
        "search": "linkage recombination Morgan Drosophila white yellow 1.3 per cent Sturtevant",
    },
    "polygenic_inheritance": {
        "chapter": CH4,
        "title": "Polygenic inheritance",
        "aliases": ["polygenic", "skin colour", "skin color", "human height"],
        "prereqs": ["gene_allele"],
        "explain": ("Some traits do not come in two clear forms but in a range, like human height or skin "
                    "colour. Such traits are usually controlled by three or more genes and are called "
                    "polygenic traits; the environment also affects them. The effect of each allele adds up. "
                    "For example, if genes A, B and C control skin colour, AABBCC gives the darkest skin, "
                    "aabbcc the lightest, and three dominant plus three recessive alleles give an "
                    "intermediate colour."),
        "probe_q": "What is a gene?",
        "probe_a": "a unit of inheritance that carries information to express a trait",
        "check_q": "Why is human skin colour called a polygenic trait?",
        "check_a": "because it is controlled by three or more genes whose effects add up, along with the environment",
        "search": "polygenic inheritance skin colour three genes additive",
    },
    "pleiotropy": {
        "chapter": CH4,
        "title": "Pleiotropy",
        "aliases": ["pleiotropy", "pleiotropic", "one gene many effects"],
        "prereqs": ["gene_allele"],
        "explain": ("When a single gene shows more than one phenotypic effect, it is called a pleiotropic "
                    "gene. This usually happens because the gene affects a metabolic pathway that leads to "
                    "different traits. An example is phenylketonuria in humans: a mutation in the gene for "
                    "the enzyme phenylalanine hydroxylase causes both mental retardation and reduced hair and "
                    "skin pigmentation."),
        "probe_q": "What is a gene?",
        "probe_a": "a unit of inheritance that carries information to express a trait",
        "check_q": "What is a pleiotropic gene? Give one example.",
        "check_a": "a single gene that shows multiple phenotypic effects; example phenylketonuria",
        "search": "pleiotropy single gene multiple phenotypic expression phenylketonuria",
    },
    "sex_determination": {
        "chapter": CH4,
        "title": "Sex determination (XO, XY, ZW)",
        "aliases": ["sex determination", "xo type", "xy type", "zw type", "male heterogamety",
                    "female heterogamety", "henking", "x body", "autosomes", "sex chromosome"],
        "prereqs": ["chromosomal_theory"],
        "explain": ("In 1891, Henking saw a special structure in insect sperm that only half the sperm "
                    "received; he named it the X body, and it was later found to be the X chromosome. "
                    "Chromosomes that decide sex are sex chromosomes, and the rest are autosomes. "
                    "In the XO type (grasshopper), females are XX and males have only one X. In the XY type "
                    "(humans, Drosophila), females are XX and males are XY. In both, males make two kinds of "
                    "gametes, called male heterogamety. In birds (ZW type), females are ZW and males are ZZ, "
                    "so it is female heterogamety."),
        "probe_q": "According to the chromosomal theory, where are genes located?",
        "probe_a": "on chromosomes",
        "check_q": "In birds, which sex has two different sex chromosomes and what are they called?",
        "check_a": "the female, with Z and W chromosomes (ZW); males are ZZ",
        "search": "sex determination Henking X body XO XY ZW heterogamety",
    },
    "sex_determination_humans": {
        "chapter": CH4,
        "title": "Insaanon mein sex determination",
        "aliases": ["sex determination in humans", "human sex determination", "sex of the child",
                    "boy or girl", "son or daughter", "sex of baby"],
        "prereqs": ["sex_determination"],
        "explain": ("Humans have 23 pairs of chromosomes: 22 pairs of autosomes and one pair of sex "
                    "chromosomes. Females are XX and males are XY. A woman makes only one type of egg (X). "
                    "A man makes two types of sperm: 50 per cent carry X and 50 per cent carry Y. If an X "
                    "sperm fertilises the egg, the child is a girl (XX); if a Y sperm does, the child is a "
                    "boy (XY). So the sperm decides the sex of the child, and every pregnancy has a 50 per cent "
                    "chance of either sex. Blaming women for having daughters is wrong."),
        "probe_q": "In the XY type of sex determination, what are the sex chromosomes of males and females?",
        "probe_a": "males are XY and females are XX",
        "check_q": "Who decides the sex of a human child, the mother or the father? Why?",
        "check_a": "the father, because his sperm can carry either X or Y while the mother's egg always carries X",
        "search": "sex determination in humans XX XY sperm decides 50 per cent",
    },
    "sex_determination_honeybee": {
        "chapter": CH4,
        "title": "Honey bee mein sex determination",
        "aliases": ["sex determination in honey bee", "sex determination in honeybee",
                    "honey bee", "honeybee", "haplodiploid", "drone", "queen bee"],
        "prereqs": ["sex_determination"],
        "explain": ("In honey bees, sex depends on the number of chromosome sets. A fertilised egg grows into "
                    "a female (queen or worker), which is diploid with 32 chromosomes. An unfertilised egg grows "
                    "into a male (drone) by parthenogenesis, which is haploid with 16 chromosomes. This is called "
                    "the haplodiploid system. Males make sperm by mitosis, have no father and cannot have sons, "
                    "but they do have a grandfather and can have grandsons."),
        "probe_q": "What is the difference between a haploid and a diploid cell?",
        "probe_a": "haploid has one set of chromosomes, diploid has two sets",
        "check_q": "How does a male honey bee (drone) develop, and how many chromosomes does it have?",
        "check_a": "from an unfertilised egg by parthenogenesis; it is haploid with 16 chromosomes",
        "search": "sex determination honey bee haplodiploid drone 16 chromosomes parthenogenesis",
    },
    "mutation": {
        "chapter": CH4,
        "title": "Mutation",
        "aliases": ["mutation", "mutations", "mutagen", "mutagens", "point mutation",
                    "chromosomal aberration", "uv radiation"],
        "prereqs": ["gene_allele"],
        "explain": ("Mutation is a change in the DNA sequence, which changes the genotype and phenotype of "
                    "an organism. Like recombination, it creates variation. Loss (deletion) or gain "
                    "(insertion or duplication) of a DNA segment changes the chromosome; such chromosomal "
                    "aberrations are common in cancer cells. A change in a single base pair is a point "
                    "mutation, for example sickle cell anaemia. Deleting or inserting base pairs causes "
                    "frame-shift mutations. Chemical or physical factors that cause mutations, like UV "
                    "radiation, are called mutagens."),
        "probe_q": "What is a gene made of?",
        "probe_a": "DNA",
        "check_q": "What is a point mutation? Give one example.",
        "check_a": "a change in a single base pair of DNA; example sickle cell anaemia",
        "search": "mutation alteration DNA sequence point mutation mutagens UV",
    },
    "pedigree_analysis": {
        "chapter": CH4,
        "title": "Pedigree analysis",
        "aliases": ["pedigree", "family tree", "family history"],
        "prereqs": ["law_of_dominance"],
        "explain": ("We cannot do controlled crosses in humans like in pea plants. So we study the family "
                    "history of a trait over several generations, drawn as a family tree with standard "
                    "symbols. This is pedigree analysis. It helps trace how a trait, abnormality or disease "
                    "is inherited, and whether it is dominant or recessive, or linked to a sex chromosome."),
        "probe_q": "What is the difference between a dominant and a recessive trait?",
        "probe_a": "a dominant trait shows even with one allele; a recessive trait shows only when both alleles are recessive",
        "check_q": "Why do we use pedigree analysis in humans instead of controlled crosses?",
        "check_a": "because controlled crosses are not possible in humans, so we study the family history over generations",
        "search": "pedigree analysis family history generations human genetics",
    },
    "mendelian_disorders": {
        "chapter": CH4,
        "title": "Mendelian disorders",
        "aliases": ["mendelian disorder", "mendelian disorders", "genetic disorder",
                    "genetic disorders", "single gene disorder"],
        "prereqs": ["pedigree_analysis", "mutation"],
        "explain": ("Genetic disorders are of two kinds: Mendelian disorders and chromosomal disorders. "
                    "Mendelian disorders are caused by a change (mutation) in a single gene and are inherited "
                    "following Mendel's principles. They can be traced in a family by pedigree analysis and "
                    "may be dominant or recessive. Common examples are haemophilia, cystic fibrosis, "
                    "sickle-cell anaemia, colour blindness, phenylketonuria and thalassemia."),
        "probe_q": "What is a mutation?",
        "probe_a": "a change in the DNA sequence",
        "check_q": "What causes a Mendelian disorder? Name two examples.",
        "check_a": "a mutation in a single gene; examples haemophilia, sickle-cell anaemia, colour blindness, phenylketonuria, thalassemia",
        "search": "Mendelian disorders single gene haemophilia cystic fibrosis sickle-cell",
    },
    "colour_blindness": {
        "chapter": CH4,
        "title": "Colour blindness",
        "aliases": ["colour blindness", "color blindness", "colour blind", "color blind",
                    "red green"],
        "prereqs": ["mendelian_disorders", "sex_determination_humans"],
        "explain": ("Colour blindness is a sex-linked recessive disorder. A defect in the red or green cone "
                    "of the eye makes a person unable to tell red from green. The gene is on the X "
                    "chromosome. It is seen in about 8 per cent of males but only about 0.4 per cent of "
                    "females, because males have only one X. A carrier mother is not colour blind herself, "
                    "but her son has a 50 per cent chance of being colour blind. A daughter is normally "
                    "colour blind only if her mother is a carrier and her father is colour blind."),
        "probe_q": "How many X chromosomes do human males and females have?",
        "probe_a": "males have one X, females have two",
        "check_q": "Why is colour blindness much more common in males than in females?",
        "check_a": "because the recessive gene is on the X chromosome and males have only one X, so one copy is enough to cause it",
        "search": "colour blindness sex-linked recessive X chromosome red green cone",
    },
    "haemophilia": {
        "chapter": CH4,
        "title": "Haemophilia",
        "aliases": ["haemophilia", "hemophilia", "bleeding disorder", "queen victoria", "blood clotting"],
        "prereqs": ["mendelian_disorders", "sex_determination_humans"],
        "explain": ("Haemophilia is a sex-linked recessive disease. One protein in the chain of proteins "
                    "needed for blood clotting is affected, so even a small cut can cause non-stop bleeding. "
                    "A heterozygous (carrier) female does not suffer but can pass the disease to her sons. "
                    "A haemophilic female is very rare, because her mother must be at least a carrier and "
                    "her father must be haemophilic. Queen Victoria was a carrier, and many of her "
                    "descendants had haemophilia."),
        "probe_q": "Which chromosome carries the genes for sex-linked disorders?",
        "probe_a": "the X chromosome",
        "check_q": "What goes wrong in haemophilia, and who usually passes it to sons?",
        "check_a": "a blood-clotting protein is affected so bleeding does not stop; a carrier (heterozygous) mother passes it to sons",
        "search": "haemophilia sex linked recessive clotting carrier female Queen Victoria",
    },
    "sickle_cell_anaemia": {
        "chapter": CH4,
        "title": "Sickle-cell anaemia",
        "aliases": ["sickle cell", "sickle", "hbs", "glutamic acid", "valine"],
        "prereqs": ["mendelian_disorders"],
        "explain": ("Sickle-cell anaemia is an autosomal recessive disorder controlled by the alleles HbA "
                    "and HbS. Only HbS HbS people have the disease; HbA HbS people look normal but are carriers. "
                    "The cause is a single base change in the sixth codon of the beta globin gene, from GAG to "
                    "GUG, so glutamic acid is replaced by valine at the sixth position of the beta globin chain. "
                    "Under low oxygen, this haemoglobin polymerises and the red blood cell changes from a "
                    "biconcave disc to a sickle shape."),
        "probe_q": "What is a point mutation?",
        "probe_a": "a change in a single base pair of DNA",
        "check_q": "In sickle-cell anaemia, which amino acid is replaced by which, and at what position?",
        "check_a": "glutamic acid is replaced by valine at the sixth position of the beta globin chain",
        "search": "sickle-cell anaemia HbS glutamic acid valine sixth position beta globin GAG GUG",
    },
    "phenylketonuria": {
        "chapter": CH4,
        "title": "Phenylketonuria (PKU)",
        "aliases": ["phenylketonuria", "pku", "phenylalanine", "phenylpyruvic"],
        "prereqs": ["mendelian_disorders", "pleiotropy"],
        "explain": ("Phenylketonuria is an inborn error of metabolism, inherited as an autosomal recessive "
                    "trait. The person lacks the enzyme that converts the amino acid phenylalanine into "
                    "tyrosine. So phenylalanine builds up and is changed into phenylpyruvic acid and related "
                    "chemicals. These collect in the brain and cause mental retardation, and they are also "
                    "passed out in urine because the kidney cannot absorb them well."),
        "probe_q": "What is a pleiotropic gene?",
        "probe_a": "a single gene that shows more than one phenotypic effect",
        "check_q": "Which conversion fails in phenylketonuria, and what builds up in the body?",
        "check_a": "phenylalanine is not converted into tyrosine; phenylalanine and phenylpyruvic acid build up",
        "search": "phenylketonuria phenylalanine tyrosine phenylpyruvic acid autosomal recessive",
    },
    "thalassemia": {
        "chapter": CH4,
        "title": "Thalassemia",
        "aliases": ["thalassemia", "thalassaemia", "alpha thalassemia", "beta thalassemia"],
        "prereqs": ["mendelian_disorders"],
        "explain": ("Thalassemia is an autosomal recessive blood disease passed on when both parents are "
                    "carriers. A mutation or deletion reduces how fast one of the globin chains (alpha or "
                    "beta) of haemoglobin is made, causing anaemia. Alpha thalassemia is controlled by two "
                    "closely linked genes, HBA1 and HBA2, on chromosome 16. Beta thalassemia is controlled by "
                    "one gene, HBB, on chromosome 11. Thalassemia is a quantitative problem (too few globin "
                    "molecules), while sickle-cell anaemia is a qualitative problem (wrongly working globin)."),
        "probe_q": "Which protein in red blood cells carries oxygen, and what chains is it made of?",
        "probe_a": "haemoglobin, made of globin chains (alpha and beta)",
        "check_q": "How is thalassemia different from sickle-cell anaemia?",
        "check_a": "thalassemia is a quantitative problem of making too few globin molecules; sickle-cell anaemia is a qualitative problem of making a wrongly working globin",
        "search": "thalassemia alpha beta globin HBA1 HBA2 chromosome 16 HBB chromosome 11",
    },
    "chromosomal_disorders": {
        "chapter": CH4,
        "title": "Chromosomal disorders",
        "aliases": ["chromosomal disorder", "chromosomal disorders", "aneuploidy", "polyploidy",
                    "trisomy", "monosomy"],
        "prereqs": ["mutation"],
        "explain": ("Chromosomal disorders are caused by missing, extra or wrongly arranged chromosomes. "
                    "If chromatids fail to separate during cell division, a chromosome is gained or lost; "
                    "this is aneuploidy. If cytokinesis fails after telophase, a whole extra set of "
                    "chromosomes is added; this is polyploidy, common in plants. Normal humans have 46 "
                    "chromosomes (23 pairs). One extra copy of a chromosome is trisomy, and one missing "
                    "copy is monosomy. Examples are Down's, Turner's and Klinefelter's syndromes."),
        "probe_q": "How many chromosomes are there in a normal human cell?",
        "probe_a": "46 (23 pairs)",
        "check_q": "What is the difference between aneuploidy and polyploidy?",
        "check_a": "aneuploidy is gain or loss of one or more chromosomes due to failed segregation of chromatids; polyploidy is an increase in a whole set of chromosomes due to failed cytokinesis",
        "search": "chromosomal disorders aneuploidy polyploidy trisomy monosomy",
    },
    "downs_syndrome": {
        "chapter": CH4,
        "title": "Down's syndrome",
        "aliases": ["down syndrome", "downs syndrome", "trisomy 21", "langdon down"],
        "prereqs": ["chromosomal_disorders"],
        "explain": ("Down's syndrome is caused by an extra copy of chromosome 21 (trisomy 21). It was "
                    "first described by Langdon Down in 1866. The person is short, with a small round head, "
                    "a furrowed tongue and a partly open mouth. The palm is broad with a characteristic "
                    "crease, and physical, psychomotor and mental development is slow."),
        "probe_q": "What is trisomy?",
        "probe_a": "having one extra copy of a chromosome",
        "check_q": "What is the chromosomal cause of Down's syndrome?",
        "check_a": "an extra copy of chromosome 21 (trisomy 21)",
        "search": "Down's syndrome trisomy 21 Langdon Down",
    },
    "klinefelters_syndrome": {
        "chapter": CH4,
        "title": "Klinefelter's syndrome",
        "aliases": ["klinefelter", "klinefelters", "xxy", "47 xxy", "gynaecomastia", "gynecomastia"],
        "prereqs": ["chromosomal_disorders", "sex_determination_humans"],
        "explain": ("Klinefelter's syndrome is caused by an extra X chromosome, giving the karyotype 47, XXY. "
                    "The person develops as a male overall but also shows some female features, such as "
                    "breast development (gynaecomastia). Such individuals are sterile."),
        "probe_q": "What are the sex chromosomes of a normal human male?",
        "probe_a": "XY",
        "check_q": "What is the karyotype in Klinefelter's syndrome?",
        "check_a": "47, XXY",
        "search": "Klinefelter's syndrome 47 XXY gynaecomastia sterile",
    },
    "turners_syndrome": {
        "chapter": CH4,
        "title": "Turner's syndrome",
        "aliases": ["turner", "turners", "45 x0", "45 xo", "xo female"],
        "prereqs": ["chromosomal_disorders", "sex_determination_humans"],
        "explain": ("Turner's syndrome is caused by the absence of one X chromosome in females, giving "
                    "45, X0. These females are sterile because their ovaries are rudimentary, and they lack "
                    "other secondary sexual characters."),
        "probe_q": "What are the sex chromosomes of a normal human female?",
        "probe_a": "XX",
        "check_q": "What is the karyotype in Turner's syndrome, and why are these females sterile?",
        "check_a": "45, X0; they are sterile because their ovaries are rudimentary",
        "search": "Turner's syndrome 45 X0 rudimentary ovaries sterile",
    },

    # ===========================================================
    # CHAPTER 5 - MOLECULAR BASIS OF INHERITANCE
    # ===========================================================
    "nucleotide": {
        "chapter": CH5,
        "title": "DNA ki building block (nucleotide)",
        "aliases": ["nucleotide", "dna structure", "structure of dna", "dna kya hai", "what is dna"],
        "prereqs": [],
        "explain": ("DNA is a very long chain made of small units called nucleotides. "
                    "Each nucleotide has three parts: a phosphate group, a sugar called deoxyribose, "
                    "and a nitrogenous base. The four bases in DNA are adenine (A), guanine (G), "
                    "cytosine (C) and thymine (T)."),
        "probe_q": "What are the three parts of a nucleotide in DNA?",
        "probe_a": "a phosphate group, a deoxyribose (pentose) sugar and a nitrogenous base",
        "check_q": "Name the four nitrogenous bases found in DNA.",
        "check_a": "adenine, guanine, cytosine and thymine",
        "search": "nucleotide structure phosphate sugar nitrogenous base DNA",
    },
    "polynucleotide_chain": {
        "chapter": CH5,
        "title": "Polynucleotide chain",
        "aliases": ["polynucleotide", "nucleoside", "phosphodiester", "purine", "purines",
                    "pyrimidine", "pyrimidines", "glycosidic", "dna and rna difference",
                    "difference between dna and rna"],
        "prereqs": ["nucleotide"],
        "explain": ("Bases are of two types: purines (adenine, guanine) and pyrimidines (cytosine, "
                    "uracil, thymine). A base joined to the 1' carbon of the sugar by an N-glycosidic bond "
                    "forms a nucleoside. Adding a phosphate to the 5' carbon of the sugar forms a nucleotide. "
                    "Nucleotides are joined by 3'-5' phosphodiester bonds into a polynucleotide chain, whose "
                    "backbone is sugar and phosphate with the bases sticking out. One end has a free phosphate "
                    "(5' end) and the other a free OH (3' end). RNA differs from DNA: its sugar has an extra OH "
                    "at the 2' position, and it has uracil in place of thymine."),
        "probe_q": "Name the three parts of a nucleotide.",
        "probe_a": "a nitrogenous base, a pentose sugar and a phosphate group",
        "check_q": "Which bond joins two nucleotides, and what are the two chemical differences between DNA and RNA?",
        "check_a": "a 3'-5' phosphodiester bond; RNA has an extra 2'-OH on its ribose sugar and has uracil instead of thymine",
        "search": "polynucleotide chain nucleoside N-glycosidic phosphodiester 5' end 3' end purines pyrimidines",
    },
    "base_pairing": {
        "chapter": CH5,
        "title": "Base pairing (A-T aur G-C)",
        "aliases": ["base pairing", "complementary", "base pair", "chargaff"],
        "prereqs": ["nucleotide"],
        "explain": ("In DNA, adenine (A) always pairs with thymine (T), and guanine (G) always pairs "
                    "with cytosine (C). This is called complementary base pairing. "
                    "Because of this rule, if you know the sequence of one strand, "
                    "you can tell the sequence of the other strand. Erwin Chargaff had observed that in "
                    "double stranded DNA the ratio of A to T and of G to C is always one."),
        "probe_q": "In DNA, which base pairs with adenine, and which base pairs with guanine?",
        "probe_a": "thymine pairs with adenine and cytosine pairs with guanine",
        "check_q": "If one DNA strand reads A-T-G-C, what will the complementary strand read?",
        "check_a": "T-A-C-G",
        "search": "complementary base pairing adenine thymine guanine cytosine Chargaff",
    },
    "double_helix": {
        "chapter": CH5,
        "title": "DNA ka double helix",
        "aliases": ["double helix", "helix", "two strands", "dna ka structure", "watson and crick",
                    "watson crick", "rosalind franklin", "antiparallel", "anti parallel"],
        "prereqs": ["polynucleotide_chain", "base_pairing"],
        "explain": ("In 1953, James Watson and Francis Crick proposed the double helix model of DNA, using "
                    "X-ray data from Maurice Wilkins and Rosalind Franklin. DNA has two polynucleotide "
                    "strands twisted like a spiral staircase, with the sugar-phosphate backbone outside and "
                    "the bases inside. The two strands run in opposite directions (anti-parallel: 5' to 3' and "
                    "3' to 5'). A pairs with T by two hydrogen bonds and G pairs with C by three. The helix is "
                    "right-handed, with a pitch of 3.4 nm, about 10 base pairs per turn, and 0.34 nm between "
                    "base pairs. Stacking of base pairs adds stability."),
        "probe_q": "What holds the two strands of DNA together?",
        "probe_a": "hydrogen bonds between the paired (complementary) bases",
        "check_q": "How many hydrogen bonds are there between A and T, and between G and C?",
        "check_a": "two between A and T, three between G and C",
        "search": "double helix DNA Watson Crick anti-parallel hydrogen bonds 3.4 nm 10 bp",
    },
    "central_dogma": {
        "chapter": CH5,
        "title": "Central dogma",
        "aliases": ["central dogma", "dna to rna to protein", "reverse transcription"],
        "prereqs": ["double_helix"],
        "explain": ("Francis Crick proposed the central dogma of molecular biology: genetic information "
                    "flows from DNA to RNA to protein. In some viruses, information flows in the reverse "
                    "direction, from RNA to DNA (reverse transcription)."),
        "probe_q": "What is DNA made of?",
        "probe_a": "nucleotides",
        "check_q": "What does the central dogma say, and who proposed it?",
        "check_a": "genetic information flows from DNA to RNA to protein; proposed by Francis Crick",
        "search": "central dogma Crick DNA RNA protein",
    },
    "dna_packaging": {
        "chapter": CH5,
        "title": "DNA packaging (nucleosome, chromatin)",
        "aliases": ["packaging", "nucleosome", "histone", "histones", "chromatin",
                    "euchromatin", "heterochromatin", "beads on string", "nucleoid"],
        "prereqs": ["double_helix"],
        "explain": ("The DNA of a mammalian cell is about 2.2 metres long, far bigger than the nucleus, "
                    "so it must be packed. In prokaryotes like E. coli, negatively charged DNA is held by "
                    "positively charged proteins in a region called the nucleoid. In eukaryotes, positively "
                    "charged proteins called histones (rich in lysine and arginine) form a unit of eight, the "
                    "histone octamer. DNA wraps around it to form a nucleosome, about 200 bp of DNA. "
                    "Nucleosomes look like beads-on-string and form chromatin, which coils further into "
                    "chromosomes with the help of non-histone chromosomal (NHC) proteins. Loosely packed, "
                    "active chromatin is euchromatin; densely packed, inactive chromatin is heterochromatin."),
        "probe_q": "Describe the shape of DNA in one line.",
        "probe_a": "a double helix of two strands twisted around each other",
        "check_q": "What is a nucleosome made of?",
        "check_a": "negatively charged DNA wrapped around a positively charged histone octamer (about 200 bp of DNA)",
        "search": "packaging of DNA histone octamer nucleosome chromatin euchromatin heterochromatin",
    },
    "griffith_experiment": {
        "chapter": CH5,
        "title": "Griffith ka transforming principle",
        "aliases": ["griffith", "transforming principle", "transformation experiment",
                    "streptococcus", "pneumococcus", "s strain", "r strain"],
        "prereqs": [],
        "explain": ("In 1928, Frederick Griffith worked with the bacterium Streptococcus pneumoniae. The S "
                    "strain has a smooth polysaccharide coat and kills mice; the R strain has no coat and does "
                    "not. Heat-killed S bacteria alone did not kill mice. But a mixture of heat-killed S and "
                    "live R bacteria killed the mice, and live S bacteria were found in them. He concluded that "
                    "some 'transforming principle' from the dead S cells had changed the R cells into S cells. "
                    "He could not say what this chemical was."),
        "probe_q": "What does the word virulent mean for a bacterium?",
        "probe_a": "able to cause disease",
        "check_q": "In Griffith's experiment, what happened when heat-killed S bacteria were mixed with live R bacteria and injected into mice?",
        "check_a": "the mice died and live S bacteria were recovered, because the R bacteria were transformed",
        "search": "Griffith transforming principle Streptococcus pneumoniae S strain R strain heat-killed",
    },
    "avery_experiment": {
        "chapter": CH5,
        "title": "Avery, MacLeod aur McCarty ka experiment",
        "aliases": ["avery", "macleod", "mccarty", "biochemical nature", "dnase"],
        "prereqs": ["griffith_experiment"],
        "explain": ("Before this work, people thought the genetic material was protein. Oswald Avery, Colin "
                    "MacLeod and Maclyn McCarty (1933 to 1944) purified proteins, DNA and RNA from heat-killed "
                    "S cells to see which one transformed R cells. Only DNA caused transformation. Protein-"
                    "digesting enzymes (proteases) and RNA-digesting enzymes (RNases) did not stop it, but "
                    "DNase did. So they concluded that DNA is the hereditary material, though not everyone "
                    "was convinced."),
        "probe_q": "What did Griffith call the substance that changed R bacteria into S bacteria?",
        "probe_a": "the transforming principle",
        "check_q": "Which enzyme stopped transformation in Avery's experiment, and what did that prove?",
        "check_a": "DNase stopped it, which showed that DNA is the transforming principle (genetic material)",
        "search": "Avery MacLeod McCarty transforming principle DNA DNase protease RNase",
    },
    "hershey_chase": {
        "chapter": CH5,
        "title": "Hershey-Chase experiment",
        "aliases": ["hershey", "chase experiment", "blender experiment", "radioactive sulphur",
                    "radioactive sulfur", "radioactive phosphorus", "dna is the genetic material",
                    "genetic material"],
        "prereqs": ["avery_experiment"],
        "explain": ("Alfred Hershey and Martha Chase (1952) gave clear proof that DNA is the genetic "
                    "material, using bacteriophages (viruses that infect bacteria). They grew some viruses with "
                    "radioactive phosphorus, which labels DNA, and some with radioactive sulfur, which labels "
                    "protein. After the viruses infected E. coli, the viral coats were removed in a blender and "
                    "separated by centrifuge. Bacteria infected with radioactive-DNA viruses became radioactive, "
                    "but those infected with radioactive-protein viruses did not. So DNA, not protein, enters "
                    "the bacteria."),
        "probe_q": "Before these experiments, which molecule did scientists think was the genetic material?",
        "probe_a": "protein",
        "check_q": "In the Hershey-Chase experiment, why was radioactive phosphorus used for DNA and radioactive sulfur for protein?",
        "check_a": "because DNA contains phosphorus but no sulfur, and protein contains sulfur but no phosphorus",
        "search": "Hershey Chase bacteriophage radioactive phosphorus sulfur blender centrifuge",
    },
    "genetic_material_properties": {
        "chapter": CH5,
        "title": "Genetic material ki properties (DNA vs RNA)",
        "aliases": ["properties of genetic material", "dna vs rna", "dna versus rna",
                    "why dna is better", "criteria of genetic material"],
        "prereqs": ["hershey_chase", "polynucleotide_chain"],
        "explain": ("A genetic material must: (1) be able to copy itself, (2) be chemically and "
                    "structurally stable, (3) allow slow changes (mutation) for evolution, and (4) express "
                    "itself as Mendelian characters. Both DNA and RNA can copy themselves by base pairing, "
                    "but proteins cannot. RNA's 2'-OH group makes it reactive and easily broken, and RNA "
                    "mutates faster; thymine also gives DNA extra stability. RNA can directly code for "
                    "proteins, while DNA needs RNA. So DNA is better for storing genetic information and RNA "
                    "for transmitting it. Some viruses, like Tobacco Mosaic Virus, use RNA as genetic material."),
        "probe_q": "Which experiment gave clear proof that DNA is the genetic material?",
        "probe_a": "the Hershey-Chase experiment",
        "check_q": "Why is DNA a better genetic material than RNA?",
        "check_a": "DNA is chemically less reactive and structurally more stable; RNA's 2'-OH makes it reactive and easily degraded",
        "search": "properties of genetic material DNA versus RNA stability 2'-OH replication mutation",
    },
    "rna_world": {
        "chapter": CH5,
        "title": "RNA world",
        "aliases": ["rna world", "first genetic material"],
        "prereqs": ["genetic_material_properties"],
        "explain": ("RNA was the first genetic material. Essential life processes such as metabolism, "
                    "translation and splicing evolved around RNA. RNA acted both as genetic material and as "
                    "a catalyst. But being a catalyst made it reactive and unstable, so DNA evolved from RNA "
                    "with chemical changes that make it more stable. Being double stranded, DNA also resists "
                    "change through repair."),
        "probe_q": "Which is more stable, DNA or RNA?",
        "probe_a": "DNA",
        "check_q": "Why did DNA evolve from RNA as the genetic material?",
        "check_a": "because RNA, being a catalyst, was reactive and unstable, while DNA is chemically modified to be more stable",
        "search": "RNA world first genetic material catalyst DNA evolved from RNA",
    },
    "dna_replication": {
        "chapter": CH5,
        "title": "DNA replication",
        "aliases": ["dna replication", "replication", "replicate", "semiconservative", "semi conservative"],
        "prereqs": ["base_pairing", "double_helix"],
        "explain": ("DNA replication is the process in which a cell makes an exact copy of its DNA "
                    "before it divides. The two strands of the parent DNA separate, and each strand "
                    "acts as a template to build a new complementary strand. So every new DNA molecule "
                    "has one old (parental) strand and one newly made strand. This is why replication "
                    "is called semiconservative. Watson and Crick suggested this scheme right after "
                    "proposing the double helix."),
        "probe_q": "During DNA replication, what happens to the two strands of the parent DNA?",
        "probe_a": "they separate and each strand acts as a template for a new strand",
        "check_q": "Why is DNA replication called semiconservative?",
        "check_a": "because each new DNA molecule has one old (parental) strand and one newly made strand",
        "search": "DNA replication semiconservative template strand",
    },
    "meselson_stahl": {
        "chapter": CH5,
        "title": "Meselson aur Stahl ka experiment",
        "aliases": ["meselson", "stahl", "15n", "heavy nitrogen", "cesium chloride", "cscl",
                    "proof of semiconservative", "experimental proof", "taylor", "vicia faba"],
        "prereqs": ["dna_replication"],
        "explain": ("In 1958, Matthew Meselson and Franklin Stahl grew E. coli for many generations in a "
                    "medium with 15NH4Cl, so its DNA had heavy nitrogen (15N, which is not radioactive). They "
                    "then moved the cells to normal 14N medium and checked DNA density by centrifugation in "
                    "a caesium chloride (CsCl) gradient. After one generation (20 minutes) all DNA was of hybrid "
                    "(intermediate) density. After two generations (40 minutes) there were equal amounts of "
                    "hybrid and light DNA. This proved replication is semiconservative. Taylor and colleagues "
                    "showed the same in Vicia faba using radioactive thymidine."),
        "probe_q": "What does semiconservative replication mean?",
        "probe_a": "each new DNA molecule has one old strand and one new strand",
        "check_q": "In Meselson and Stahl's experiment, what kind of DNA was seen after one generation in 14N medium?",
        "check_a": "all DNA had hybrid (intermediate) density",
        "search": "Meselson Stahl 15N 14N CsCl density gradient hybrid DNA semiconservative",
    },
    "dna_polymerase": {
        "chapter": CH5,
        "title": "DNA polymerase aur replication ki machinery",
        "aliases": ["dna polymerase", "polymerase", "enzyme in replication", "ligase", "okazaki",
                    "replication fork", "origin of replication", "leading strand", "lagging strand",
                    "discontinuous"],
        "prereqs": ["dna_replication"],
        "explain": ("The main enzyme in replication is DNA-dependent DNA polymerase. "
                    "It reads the old strand as a template and joins new nucleotides to it, "
                    "following the base pairing rule. It is very fast and accurate: E. coli copies its DNA "
                    "in about 18 minutes, roughly 2000 bp per second. Deoxyribonucleoside triphosphates act "
                    "both as building blocks and as the energy source. Replication happens at a small opening "
                    "called the replication fork, and it starts only at a fixed region called the origin of "
                    "replication. The polymerase builds only in the 5' to 3' direction, so one new strand is "
                    "made continuously and the other in small pieces (discontinuously). "
                    "These pieces are joined together by another enzyme called DNA ligase."),
        "probe_q": "Which enzyme joins nucleotides to build the new DNA strand?",
        "probe_a": "DNA-dependent DNA polymerase",
        "check_q": "Why is one new strand made in pieces, and which enzyme joins the pieces?",
        "check_a": "because DNA polymerase works only in the 5' to 3' direction; the pieces are joined by DNA ligase",
        "search": "DNA-dependent DNA polymerase replication fork 5' to 3' discontinuous DNA ligase origin of replication",
    },
    "transcription": {
        "chapter": CH5,
        "title": "Transcription",
        "aliases": ["transcription", "transcribe", "dna to rna", "why only one strand"],
        "prereqs": ["central_dogma", "base_pairing"],
        "explain": ("Transcription is copying genetic information from one strand of DNA into RNA. It also "
                    "follows complementary base pairing, except that adenine now pairs with uracil instead of "
                    "thymine. Unlike replication, only a segment of DNA and only one of its strands is copied. "
                    "If both strands were copied, they would code for two different RNAs (and proteins), and "
                    "the two RNAs would pair with each other into double-stranded RNA that cannot be translated."),
        "probe_q": "In which direction does genetic information flow according to the central dogma?",
        "probe_a": "from DNA to RNA to protein",
        "check_q": "In transcription, which base in RNA pairs with adenine of DNA, and why is only one DNA strand copied?",
        "check_a": "uracil; if both strands were copied they would make different RNAs that would pair into double-stranded RNA and not be translated",
        "search": "transcription copying DNA into RNA one strand uracil complementarity",
    },
    "transcription_unit": {
        "chapter": CH5,
        "title": "Transcription unit (promoter, structural gene, terminator)",
        "aliases": ["transcription unit", "promoter", "terminator", "template strand",
                    "coding strand", "structural gene"],
        "prereqs": ["transcription"],
        "explain": ("A transcription unit in DNA has three parts: a promoter, the structural gene and a "
                    "terminator. RNA polymerase also works only 5' to 3', so the DNA strand with 3' to 5' "
                    "polarity is the template strand. The other strand (5' to 3') has the same sequence as the "
                    "RNA, except T instead of U, and is called the coding strand. The promoter, where RNA "
                    "polymerase binds, lies upstream (5' end) of the structural gene, and the terminator lies "
                    "downstream (3' end) and marks the end of transcription."),
        "probe_q": "What is transcription?",
        "probe_a": "copying genetic information from one strand of DNA into RNA",
        "check_q": "What are the three regions of a transcription unit, and which strand acts as the template?",
        "check_a": "promoter, structural gene and terminator; the strand with 3' to 5' polarity is the template strand",
        "search": "transcription unit promoter structural gene terminator template strand coding strand",
    },
    "split_genes": {
        "chapter": CH5,
        "title": "Gene, cistron, exon aur intron",
        "aliases": ["split gene", "split genes", "exon", "exons", "intron", "introns", "cistron",
                    "monocistronic", "polycistronic"],
        "prereqs": ["transcription_unit"],
        "explain": ("A gene is the functional unit of inheritance. A cistron is a segment of DNA that codes "
                    "for one polypeptide. Structural genes are mostly monocistronic in eukaryotes and "
                    "polycistronic in bacteria. In eukaryotes, the coding sequence is interrupted, so the genes "
                    "are called split genes. The coding parts that appear in the mature RNA are exons, and the "
                    "interrupting parts that are removed are introns."),
        "probe_q": "What are the three parts of a transcription unit?",
        "probe_a": "promoter, structural gene and terminator",
        "check_q": "What is the difference between exons and introns?",
        "check_a": "exons are coding sequences that appear in mature RNA; introns are intervening sequences that do not appear in mature RNA",
        "search": "cistron monocistronic polycistronic split genes exons introns",
    },
    "types_of_rna": {
        "chapter": CH5,
        "title": "RNA ke types (mRNA, tRNA, rRNA)",
        "aliases": ["types of rna", "mrna", "rrna", "messenger rna", "ribosomal rna",
                    "kinds of rna"],
        "prereqs": ["transcription"],
        "explain": ("In bacteria there are three main types of RNA, and all three are needed to make a "
                    "protein. Messenger RNA (mRNA) provides the template. Transfer RNA (tRNA) brings amino "
                    "acids and reads the genetic code. Ribosomal RNA (rRNA) plays structural and catalytic "
                    "roles during translation."),
        "probe_q": "What is transcription?",
        "probe_a": "copying information from DNA into RNA",
        "check_q": "What is the role of mRNA, tRNA and rRNA?",
        "check_a": "mRNA provides the template, tRNA brings amino acids and reads the code, rRNA has structural and catalytic roles in translation",
        "search": "types of RNA mRNA tRNA rRNA template amino acids catalytic",
    },
    "transcription_bacteria": {
        "chapter": CH5,
        "title": "Bacteria mein transcription",
        "aliases": ["transcription in bacteria", "prokaryotic transcription", "transcription in prokaryotes",
                    "sigma factor", "rho factor", "rna polymerase"],
        "prereqs": ["transcription_unit", "types_of_rna"],
        "explain": ("In bacteria, a single DNA-dependent RNA polymerase makes all types of RNA. It binds to the "
                    "promoter and starts (initiation), adds nucleotides following base pairing (elongation), "
                    "and stops at the terminator, where the RNA and the enzyme fall off (termination). The "
                    "enzyme itself can only do elongation; it uses the sigma (initiation) factor to start and "
                    "the rho (termination) factor to stop. Since bacterial mRNA needs no processing and there "
                    "is no nucleus, translation can start before transcription ends; the two are coupled."),
        "probe_q": "Where does RNA polymerase bind to start transcription?",
        "probe_a": "the promoter",
        "check_q": "Which factors help bacterial RNA polymerase start and stop transcription?",
        "check_a": "the sigma factor for initiation and the rho factor for termination",
        "search": "transcription in bacteria RNA polymerase sigma factor rho factor initiation elongation termination",
    },
    "transcription_eukaryotes": {
        "chapter": CH5,
        "title": "Eukaryotes mein transcription (splicing, capping, tailing)",
        "aliases": ["transcription in eukaryotes", "eukaryotic transcription", "splicing", "capping",
                    "tailing", "hnrna", "polymerase ii", "polymerase iii", "three rna polymerases"],
        "prereqs": ["transcription_bacteria", "split_genes"],
        "explain": ("Eukaryotes have at least three RNA polymerases in the nucleus. RNA polymerase I makes "
                    "rRNAs (28S, 18S, 5.8S). RNA polymerase III makes tRNA, 5S rRNA and snRNAs. RNA polymerase II "
                    "makes the precursor of mRNA, called hnRNA. The first transcript has both exons and introns, "
                    "so the introns are removed and exons joined in order; this is splicing. In capping, an "
                    "unusual nucleotide (methyl guanosine triphosphate) is added to the 5' end. In tailing, "
                    "200 to 300 adenylate residues are added to the 3' end. The processed hnRNA, now mRNA, "
                    "leaves the nucleus for translation."),
        "probe_q": "What are introns?",
        "probe_a": "intervening sequences that are not present in mature RNA",
        "check_q": "What happens in splicing, capping and tailing?",
        "check_a": "splicing removes introns and joins exons; capping adds methyl guanosine triphosphate at the 5' end; tailing adds 200-300 adenylate residues at the 3' end",
        "search": "transcription eukaryotes RNA polymerase I II III hnRNA splicing capping tailing",
    },
    "genetic_code": {
        "chapter": CH5,
        "title": "Genetic code",
        "aliases": ["genetic code", "codon", "codons", "stop codon", "start codon", "triplet code",
                    "degenerate", "universal code", "khorana", "nirenberg", "gamow"],
        "prereqs": ["types_of_rna"],
        "explain": ("The genetic code links the base sequence of mRNA to the amino acid sequence of a protein. "
                    "George Gamow argued that 4 bases must combine in threes to code for 20 amino acids, "
                    "giving 64 codons. Har Gobind Khorana's chemical method to make RNA, Marshall Nirenberg's "
                    "cell-free system and Severo Ochoa's enzyme helped decode it. Its features: the codon is a "
                    "triplet; 61 codons code for amino acids and 3 (UAA, UAG, UGA) are stop codons; some amino "
                    "acids have more than one codon (degenerate); it is read continuously without punctuation; "
                    "it is nearly universal; and AUG codes for methionine and also acts as the start codon."),
        "probe_q": "Which RNA carries the code from DNA to the ribosome?",
        "probe_a": "messenger RNA (mRNA)",
        "check_q": "Why is the genetic code called degenerate, and which codon is the start codon?",
        "check_a": "because some amino acids are coded by more than one codon; AUG is the start (initiator) codon",
        "search": "genetic code triplet 64 codons degenerate universal AUG stop codons Khorana Nirenberg",
    },
    "frameshift_mutation": {
        "chapter": CH5,
        "title": "Mutation aur genetic code (frameshift)",
        "aliases": ["frameshift", "frame shift", "reading frame", "ram has red cap",
                    "mutations and genetic code", "insertion and deletion"],
        "prereqs": ["genetic_code", "mutation"],
        "explain": ("A point mutation can change one amino acid, for example glutamate to valine in beta "
                    "globin, causing sickle cell anaemia. If one or two bases are inserted or deleted, the "
                    "reading frame shifts from that point, and all the following codons change. Think of "
                    "'RAM HAS RED CAP': adding one letter gives 'RAM HAS BRE DCA P', which makes no sense. "
                    "These are frameshift mutations. But inserting or deleting three bases (or multiples of "
                    "three) adds or removes whole codons, and the reading frame after that stays the same."),
        "probe_q": "How many bases make up one codon?",
        "probe_a": "three",
        "check_q": "Why does inserting one base cause a frameshift mutation, but inserting three bases does not?",
        "check_a": "one base shifts the reading frame and changes all following codons; three bases add a whole codon, so the reading frame stays unchanged",
        "search": "frameshift insertion deletion mutation reading frame RAM HAS RED CAP",
    },
    "trna_adapter": {
        "chapter": CH5,
        "title": "tRNA - adapter molecule",
        "aliases": ["trna", "transfer rna", "adapter molecule", "adaptor molecule", "anticodon",
                    "clover leaf", "cloverleaf", "srna"],
        "prereqs": ["genetic_code"],
        "explain": ("Francis Crick said there must be an adapter molecule that reads the code on one side and "
                    "binds an amino acid on the other. This is tRNA, earlier called sRNA (soluble RNA). tRNA has "
                    "an anticodon loop with bases complementary to the codon, and an amino acid acceptor end. "
                    "Each amino acid has its own tRNA, and a special initiator tRNA starts translation. There "
                    "are no tRNAs for stop codons. Its secondary structure looks like a clover-leaf, but the "
                    "real 3D shape is like an inverted L."),
        "probe_q": "What is a codon?",
        "probe_a": "a group of three bases on mRNA that codes for an amino acid",
        "check_q": "Why is tRNA called an adapter molecule?",
        "check_a": "because it reads the codon with its anticodon and also carries the matching amino acid",
        "search": "tRNA adapter molecule anticodon amino acid acceptor end clover-leaf inverted L",
    },
    "translation": {
        "chapter": CH5,
        "title": "Translation (protein synthesis)",
        "aliases": ["translation", "protein synthesis", "ribosome", "ribosomes", "peptide bond",
                    "charging of trna", "aminoacylation", "untranslated region", "ribozyme"],
        "prereqs": ["trna_adapter"],
        "explain": ("Translation is joining amino acids into a polypeptide in the order set by mRNA. First, "
                    "amino acids are activated with ATP and attached to their tRNA; this is charging "
                    "(aminoacylation) of tRNA. The ribosome, made of rRNAs and about 80 proteins, has a small "
                    "and a large subunit. Translation starts when the small subunit meets the mRNA, and the "
                    "initiator tRNA binds the start codon AUG. In elongation, charged tRNAs pair with codons "
                    "one by one and peptide bonds form; in bacteria, 23S rRNA acts as the enzyme (ribozyme). "
                    "At the stop codon, a release factor ends translation. Untranslated regions (UTRs) at the "
                    "5' and 3' ends help efficient translation."),
        "probe_q": "Which molecule brings amino acids to the ribosome?",
        "probe_a": "tRNA (transfer RNA)",
        "check_q": "What is charging of tRNA, and what ends translation?",
        "check_a": "charging is attaching an activated amino acid to its tRNA using ATP; a release factor binding to the stop codon ends translation",
        "search": "translation charging of tRNA aminoacylation ribosome peptide bond release factor UTR",
    },
    "gene_regulation": {
        "chapter": CH5,
        "title": "Gene expression ka regulation",
        "aliases": ["regulation of gene expression", "gene regulation", "gene expression",
                    "operator", "activator", "repressor protein"],
        "prereqs": ["transcription_unit", "translation"],
        "explain": ("Cells switch genes on or off based on metabolic, physiological or environmental "
                    "conditions. In eukaryotes, regulation can happen at four levels: transcription, "
                    "processing (splicing), transport of mRNA out of the nucleus, and translation. In "
                    "prokaryotes, the main control is at the start of transcription. Regulatory proteins can "
                    "act positively (activators) or negatively (repressors). A repressor binds to a DNA "
                    "sequence called the operator, next to the promoter, and each operon has its own operator "
                    "and repressor."),
        "probe_q": "What is transcription?",
        "probe_a": "making RNA from a DNA template",
        "check_q": "At which four levels can gene expression be regulated in eukaryotes?",
        "check_a": "transcriptional level, processing level (splicing), transport of mRNA from nucleus to cytoplasm, and translational level",
        "search": "regulation of gene expression levels operator repressor activator prokaryotes",
    },
    "lac_operon": {
        "chapter": CH5,
        "title": "Lac operon",
        "aliases": ["lac operon", "operon", "lactose", "beta galactosidase", "permease",
                    "transacetylase", "inducer", "repressor", "jacob", "monod"],
        "prereqs": ["gene_regulation"],
        "explain": ("Francois Jacob and Jacques Monod first explained the lac operon. It has one regulatory "
                    "gene, i, and three structural genes, z, y and a. The i gene makes the repressor. z makes "
                    "beta-galactosidase (breaks lactose into glucose and galactose), y makes permease (lets "
                    "lactose into the cell), and a makes transacetylase. Without lactose, the repressor binds "
                    "the operator and stops RNA polymerase. When lactose (the inducer) is present, it "
                    "inactivates the repressor, so transcription starts. Because control is by a repressor, "
                    "this is called negative regulation. Glucose or galactose cannot act as inducers."),
        "probe_q": "What does a repressor protein do in gene regulation?",
        "probe_a": "it binds to the operator and stops transcription",
        "check_q": "Name the three structural genes of the lac operon and their products.",
        "check_a": "z makes beta-galactosidase, y makes permease, a makes transacetylase",
        "search": "lac operon Jacob Monod i gene repressor z y a beta-galactosidase permease inducer",
    },
    "human_genome_project": {
        "chapter": CH5,
        "title": "Human Genome Project (HGP)",
        "aliases": ["human genome project", "hgp", "genome project", "bioinformatics",
                    "expressed sequence tags", "sequence annotation", "bacterial artificial chromosome",
                    "yeast artificial chromosome", "sanger"],
        "prereqs": ["double_helix"],
        "explain": ("The Human Genome Project was a 13-year mega project, launched in 1990 and completed in "
                    "2003, to find the complete DNA sequence of humans (about 3 x 10^9 bp). Its goals included "
                    "identifying all genes, sequencing the 3 billion base pairs, storing the data, improving "
                    "analysis tools, transferring technology and addressing ethical, legal and social issues "
                    "(ELSI). It used two approaches: Expressed Sequence Tags (genes expressed as RNA) and "
                    "sequencing the whole genome then assigning functions (sequence annotation). DNA fragments "
                    "were cloned in BAC and YAC vectors and sequenced using Frederick Sanger's method; computers "
                    "were needed to align them, which helped develop bioinformatics."),
        "probe_q": "What does the order of bases in DNA decide?",
        "probe_a": "the genetic information of an organism",
        "check_q": "What are Expressed Sequence Tags and sequence annotation?",
        "check_a": "ESTs identify all genes expressed as RNA; sequence annotation is sequencing the whole genome and then assigning functions to its regions",
        "search": "Human Genome Project 1990 2003 goals ESTs sequence annotation BAC YAC Sanger",
    },
    "human_genome_features": {
        "chapter": CH5,
        "title": "Human genome ke salient features",
        "aliases": ["features of human genome", "salient features", "human genome features", "snp",
                    "snps", "single nucleotide polymorphism", "dystrophin", "how many genes"],
        "prereqs": ["human_genome_project"],
        "explain": ("Key findings of the HGP: the human genome has 3164.7 million bp. An average gene has "
                    "3000 bases; the largest, dystrophin, has 2.4 million bases. There are about 30,000 genes, "
                    "far fewer than expected, and 99.9 per cent of bases are the same in all humans. The "
                    "function of over half the genes is unknown, and less than 2 per cent of the genome codes "
                    "for proteins. Repeated sequences make up a large part. Chromosome 1 has the most genes "
                    "(2968) and Y the fewest (231). About 1.4 million single-base differences, called SNPs, "
                    "were found."),
        "probe_q": "When was the Human Genome Project completed?",
        "probe_a": "2003",
        "check_q": "What percentage of the human genome codes for proteins, and which chromosome has the most genes?",
        "check_a": "less than 2 per cent; chromosome 1 has the most genes",
        "search": "salient features human genome 3164.7 million bp 30000 genes SNPs chromosome 1",
    },
    "dna_polymorphism": {
        "chapter": CH5,
        "title": "DNA polymorphism",
        "aliases": ["polymorphism", "dna polymorphism", "genetic variation in population"],
        "prereqs": ["human_genome_features", "mutation"],
        "explain": ("Polymorphism means variation at the genetic level, and it arises from mutations. "
                    "A mutation in germ cells can spread through a population if it does not harm "
                    "reproduction. If a variant (allele) at a locus occurs in the population with a frequency "
                    "above 0.01, it is called a DNA polymorphism. It is more common in non-coding DNA, because "
                    "mutations there usually do not affect reproduction and keep accumulating over generations."),
        "probe_q": "What percentage of DNA bases are the same in all humans?",
        "probe_a": "99.9 per cent",
        "check_q": "When is a DNA variation called a polymorphism?",
        "check_a": "when an inheritable variant (allele) at a locus occurs in the population with a frequency greater than 0.01",
        "search": "DNA polymorphism mutation germ cells frequency 0.01 non-coding",
    },
    "dna_fingerprinting": {
        "chapter": CH5,
        "title": "DNA fingerprinting",
        "aliases": ["dna fingerprinting", "fingerprinting", "dna fingerprint", "vntr", "satellite dna",
                    "minisatellite", "mini satellite", "alec jeffreys", "forensic", "paternity",
                    "southern blot"],
        "prereqs": ["dna_polymorphism"],
        "explain": ("DNA fingerprinting is a quick way to compare the DNA of two people. It looks at "
                    "repetitive DNA, where a short sequence repeats many times. In density gradient "
                    "centrifugation, this repetitive DNA forms small peaks called satellite DNA. Alec Jeffreys "
                    "developed the technique using VNTR (Variable Number of Tandem Repeats), a mini-satellite "
                    "whose repeat number differs between people. Steps: isolate DNA, cut it with restriction "
                    "enzymes, separate fragments by electrophoresis, blot them onto a membrane, hybridise with "
                    "a labelled VNTR probe, and detect bands by autoradiography. The band pattern is unique to "
                    "each person except identical twins, so it is used in forensics and paternity testing."),
        "probe_q": "What is DNA polymorphism?",
        "probe_a": "variation in DNA sequence in a population, arising from mutation",
        "check_q": "What is VNTR, and why is DNA fingerprinting useful in forensics?",
        "check_a": "Variable Number of Tandem Repeats, a mini-satellite whose repeat number varies between people; the band pattern is unique for each person except identical twins",
        "search": "DNA fingerprinting VNTR satellite DNA Alec Jeffreys Southern blot forensic paternity",
    },
}

# ---------------------------------------------------------------
# Optional: book ke page dikhane ke liye (index pehle se bana hua hai)
# ---------------------------------------------------------------
base = os.path.dirname(os.path.abspath(__file__))
col = None
embedder = None
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    embedder = SentenceTransformer(os.path.join(base, "bge-small-local"), device="cpu")
    col = chromadb.PersistentClient(path=os.path.join(base, "index")).get_collection("books")
except Exception:
    col = None


def book_pages(text):
    if col is None:
        return ""
    try:
        qe = embedder.encode("Represent this sentence for searching relevant passages: " + text,
                             normalize_embeddings=True)
        r = col.query(query_embeddings=[qe.tolist()], n_results=3)
        seen = []
        for m in r["metadatas"][0]:
            s = f"{m['book']} page {m['page']}"
            if s not in seen:
                seen.append(s)
        return "; ".join(seen[:2])
    except Exception:
        return ""



def ask_llm(prompt):
    r = ollama.chat(model=MODEL, options={"temperature": 0},
                    messages=[{"role": "user", "content": prompt}])
    return r["message"]["content"].strip()



def judge(question, expected, answer):
    a = answer.strip().lower()

    # Empty or unknown answers
    if a in (
        "", "idk", "i dont know", "i don't know",
        "dont know", "no idea", "pata nahi",
        "nahi pata", "nahi", "?"
    ):
        return False

    prompt = f"""
You are a strict but fair Class 12 Biology examiner.

Question: {question}
Expected answer / key concepts: {expected}
Student answer: {answer}

Rules:
1. Check if the answer contains the essential scientific idea.
2. Ignore spelling and grammar mistakes if the meaning is clear.
3. Vague, unrelated, or incomplete answers are WRONG.
4. Do not assume understanding from a related word alone.
5. "because it is a molecule" is WRONG for the semiconservative question.
6. Return exactly one label: CORRECT or WRONG.
7. Do not add any explanation.

"""

    try:
        out = ask_llm(prompt).strip().upper()
        return out == "CORRECT"

    except Exception as e:
        print(f"[Tutor] Answer checking failed: {e}")
        return False



def simplify(text):
    p = ("Explain the following facts to a school student in 3 short, very simple sentences, "
         "using one everyday example. Use ONLY these facts. Do not add any new scientific facts.\n\n"
         f"Facts: {text}")
    return ask_llm(p)


# ---------------------------------------------------------------
# Tutor ka kaam (yahi "agent loop" hai)
# ---------------------------------------------------------------
class Quit(Exception):
    pass


def get(prompt):
    s = input(prompt).strip()
    if s.lower() in ("exit", "quit"):
        raise Quit()
    return s


def _norm(s):
    # apostrophe aur hyphen hata do, taaki "Down's" = "downs", "co-dominance" = "co dominance"
    s = s.lower().replace("'", "").replace("’", "").replace("-", " ")
    return " ".join(s.split())


def find_topic(text):
    t = _norm(text)
    best, best_len = None, 0
    for cid, c in G.items():
        for al in c["aliases"] + [c["title"]]:
            al = _norm(al)
            if al and al in t and len(al) > best_len:
                best, best_len = cid, len(al)
    return best


def probe(cid):
    c = G[cid]
    print(f"\n[Tutor] Pehle ek chhota sawal: {c['title']}")
    ans = get("Tutor: " + c["probe_q"] + "\nAap: ")
    ok = judge(c["probe_q"], c["probe_a"], ans)
    print("[Tutor] Sahi!" if ok else "[Tutor] Theek hai, yahan hum thoda dhyan denge.")
    return ok


def diagnose(target):
    """Prerequisite Descent: neeche ki taraf jaakar toota hua 'jad' dhoondhta hai."""
    to_teach, visited = [], set()
    count = [0]

    def check(c):
        for p in G[c]["prereqs"]:
            if p in visited or count[0] >= 5:
                continue
            visited.add(p)
            count[0] += 1
            print(f"\n[Agent soch raha hai] '{G[c]['title']}' samajhne ke liye "
                  f"'{G[p]['title']}' aana zaroori hai. Pehle yeh check karta hun.")
            if not probe(p):
                check(p)              # aur neeche jaao
                to_teach.append(p)    # sabse gehri kami pehle sikhai jayegi
    check(target)
    return to_teach


def teach(cid, weak):
    c = G[cid]
    print(f"\n=== Seekhte hain: {c['title']} ===")
    print(c["explain"])
    pages = book_pages(c["search"])
    if pages:
        print(f"(Book mein padhiye: {pages})")
    ans = get("\nTutor: " + c["check_q"] + "\nAap: ")
    if judge(c["check_q"], c["check_a"], ans):
        print("[Tutor] Bahut accha! Aap samajh gayi/gaye. ✅")
        return
    print("\n[Tutor] Koi baat nahi, ise aur aasaan tarike se samjhata hun:")
    print(simplify(c["explain"]))
    ans = get("\nTutor: Ek baar phir: " + c["check_q"] + "\nAap: ")
    if judge(c["check_q"], c["check_a"], ans):
        print("[Tutor] Ab sahi hai! ✅")
    else:
        print(f"[Tutor] Sahi jawab: {c['check_a']}.\nHum is topic par baad mein dobara aayenge.")
        weak.append(c["title"])


def show_topics():
    for ch in (CH4, CH5):
        titles = [c["title"] for c in G.values() if c["chapter"] == ch]
        print(f"\n  [{ch}] ({len(titles)} topics)")
        print(textwrap.fill(" | ".join(titles), width=100,
                            initial_indent="    ", subsequent_indent="    "))


def session():
    print("\nAap kaunsa topic samajhna chahti hain? Jaise: 'mujhe DNA replication samajh nahi aa raha'")
    print("(Abhi mere paas yeh topics hain:)")
    show_topics()
    text = get("\nAap: ")
    target = find_topic(text)
    if not target:
        print("[Tutor] Yeh topic abhi mere paas nahi hai. Upar wali list mein se koi topic likhiye.")
        return
    print(f"\n[Tutor] Theek hai, hum '{G[target]['title']}' seekhenge. "
          "Pehle main dekhunga ki aapko iske pehle ka kya aata hai.")
    roots = diagnose(target)
    if roots:
        names = ", ".join(G[r]["title"] for r in roots)
        print(f"\n[Tutor] Mujhe lagta hai ki pehle yeh samajhna zaroori hai: {names}. Wahin se shuru karte hain.")
    else:
        print("\n[Tutor] Aapko pehle ka sab aata hai. Ab seedha naya topic samajhte hain.")
    weak = []
    for cid in roots + [target]:
        teach(cid, weak)
    print("\n=== Aaj ka saar ===")
    print("Seekha: " + ", ".join(G[c]["title"] for c in roots + [target]))
    if weak:
        print("Dobara dekhna hai: " + ", ".join(weak))


def main():
    print("Namaste! Main aapka personal biology tutor hun. (Band karne ke liye kabhi bhi: exit)")
    try:
        while True:
            session()
            again = get("\nKya aur koi topic seekhna hai? (yes / no): ")
            if again.lower() not in ("y", "yes", "haan", "ha"):
                break
    except (Quit, KeyboardInterrupt, EOFError):
        pass
    print("\nDhanyavaad! Phir milte hain. 🙂")


if __name__ == "__main__":
    main()


