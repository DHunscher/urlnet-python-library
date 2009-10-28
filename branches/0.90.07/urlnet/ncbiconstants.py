#!/usr/bin/env python
# $Id$
###################################################################
#                                                                 #
#                     UrlNet Python Library                       #
#            Copyright (c) Dale A. Hunscher, 2007-2009            #
#                     All rights reserved                         #
#                                                                 #
#                                                                 #
# UrlNet is free for non-commercial use.                          #
# For commercial uses, contact dale.hunscher@thenextroguewave.com #
#                                                                 #
###################################################################

"""
NCBI constants
"""

# constants for databases

PUBMED = 'pubmed'
PROTEIN = 'protein'
NUCLEOTIDE = 'nucleotide'
NUCCORE = 'nuccore'
NUCGSS = 'nucgss'
NUCEST = 'nucest'
STRUCTURE = 'structure'
GENOME = 'genome'
BOOKS = 'books'
CANCERCHROMOSOMES = 'cancerchromosomes'
CDD = 'cdd'
GAP = 'gap'
DOMAINS = 'domains'
GENE = 'gene'
GENOMEPRJ = 'genomeprj'
GENSAT = 'gensat'
GEO = 'geo'
GDS = 'gds'
HOMOLOGENE = 'homologene'
JOURNALS = 'journals'
MESH = 'mesh'
NCBISEARCH = 'ncbisearch'
NLMCATALOG = 'nlmcatalog'
OMIA = 'omia'
OMIM = 'omim'
PMC = 'pmc'
POPSET = 'popset'
PROBE = 'probe'
PROTEINCLUSTERS = 'proteinclusters'
PCASSAY = 'pcassay'
PCCOMPOUND = 'pccompound'
PCSUBSTANCE = 'pcsubstance'
SNP = 'snp'
TAXONOMY = 'taxonomy'
TOOLKIT = 'toolkit'
UNIGENE = 'unigene'
UNISTS = 'unists'

# sequence for testing db input
dblist = (
    PUBMED , 
    PROTEIN , 
    NUCLEOTIDE , 
    NUCCORE , 
    NUCGSS , 
    NUCEST , 
    STRUCTURE , 
    GENOME , 
    BOOKS , 
    CANCERCHROMOSOMES , 
    CDD , 
    GAP , 
    DOMAINS , 
    GENE , 
    GENOMEPRJ , 
    GENSAT , 
    GEO , 
    GDS , 
    HOMOLOGENE , 
    JOURNALS , 
    MESH , 
    NCBISEARCH , 
    NLMCATALOG , 
    OMIA , 
    OMIM , 
    PMC , 
    POPSET , 
    PROBE , 
    PROTEINCLUSTERS , 
    PCASSAY , 
    PCCOMPOUND , 
    PCSUBSTANCE , 
    SNP , 
    TAXONOMY , 
    TOOLKIT , 
    UNIGENE , 
    UNISTS , 
    )

# sequence for testing db input
dbentitynamesdict = {
    PUBMED : 'publication' ,
    PROTEIN : 'protein' ,
    NUCLEOTIDE : 'nucleotide' ,
    NUCCORE : 'core nucleotide' ,
    NUCGSS : 'genetic sequence data bank' ,
    NUCEST : 'expressed sequence tags' ,
    STRUCTURE : 'structure' ,
    GENOME : 'genome' ,
    BOOKS : 'ncbi bookshelf' ,
    CANCERCHROMOSOMES : 'cancer chromosomes' ,
    CDD : 'conserved domain database' ,
    GAP : 'genotype and phenotype' ,
    DOMAINS : 'domains' ,
    GENE : 'gene' ,
    GENOMEPRJ : 'genome project' ,
    GENSAT : 'gene expression nervous system atlas' ,
    GEO : 'gene expression omnibus' ,
    GDS : 'geo datasets' ,
    HOMOLOGENE : 'genomic homologs' ,
    JOURNALS : 'journals' ,
    MESH : 'medical subject headings' ,
    NCBISEARCH : 'ncbi search' ,
    NLMCATALOG : 'nlm catalog' ,
    OMIA : 'online mendelian inheritance in animals' ,
    OMIM : 'online mendelian inheritance in man' ,
    PMC : 'pubmed central' ,
    POPSET : 'population dna sequence set' ,
    PROBE : 'probe' ,
    PROTEINCLUSTERS : 'protein clusters' ,
    PCASSAY : 'pubchem bioassay' ,
    PCCOMPOUND : 'pubchem compound' ,
    PCSUBSTANCE : 'pubchem substance' ,
     SNP : 'single nucleotide polymorphisms' ,
    TAXONOMY : 'taxonomy' ,
    TOOLKIT : 'toolkit' ,
    UNIGENE : 'unified genetic transcriptome' ,
    UNISTS : 'unigene sequence tagged sites' ,
    }

# links between databases (and within a database)
BOOKS_GENE = 'books_gene'
BOOKS_OMIM = 'books_omim'
BOOKS_PCSUBSTANCE = 'books_pcsubstance'
BOOKS_PMC_REFS = 'books_pmc_refs'
BOOKS_PUBMED_REFS = 'books_pubmed_refs'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CASECELL = 'cancerchromosomes_cancerchromosomes_casecell'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CELLCASE = 'cancerchromosomes_cancerchromosomes_cellcase'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOCGH = 'cancerchromosomes_cancerchromosomes_cytocgh'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOCLINCGH = 'cancerchromosomes_cancerchromosomes_cytoclincgh'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOCLINSKY = 'cancerchromosomes_cancerchromosomes_cytoclinsky'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTODIAGCGH = 'cancerchromosomes_cancerchromosomes_cytodiagcgh'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTODIAGSKY = 'cancerchromosomes_cancerchromosomes_cytodiagsky'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOSKY = 'cancerchromosomes_cancerchromosomes_cytosky'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_DIAG = 'cancerchromosomes_cancerchromosomes_diag'
CANCERCHROMOSOMES_CANCERCHROMOSOMES_TEXTUAL = 'cancerchromosomes_cancerchromosomes_textual'
CANCERCHROMOSOMES_PMC = 'cancerchromosomes_pmc'
CANCERCHROMOSOMES_PUBMED = 'cancerchromosomes_pubmed'
CDD_CDD_RELATED = 'cdd_cdd_related'
CDD_GENE = 'cdd_gene'
CDD_HOMOLOGENE = 'cdd_homologene'
CDD_PMC = 'cdd_pmc'
CDD_PROTEIN = 'cdd_protein'
CDD_PROTEIN_SUMMARY = 'cdd_protein_summary'
CDD_PUBMED = 'cdd_pubmed'
CDD_STRUCTURE = 'cdd_structure'
CDD_TAXONOMY = 'cdd_taxonomy'
DOMAINS_DOMAINS_NEW = 'domains_domains_new'
DOMAINS_PMC = 'domains_pmc'
DOMAINS_PROTEIN = 'domains_protein'
DOMAINS_PUBMED = 'domains_pubmed'
DOMAINS_STRUCTURE = 'domains_structure'
DOMAINS_TAXONOMY = 'domains_taxonomy'
DOMAINS_VAST = 'domains_vast'
GDS_GDS = 'gds_gds'
GDS_GEO = 'gds_geo'
GDS_GEO_URL = 'gds_geo_url'
GDS_PMC = 'gds_pmc'
GDS_PUBMED = 'gds_pubmed'
GDS_TAXONOMY = 'gds_taxonomy'
GENE_BOOKS = 'gene_books'
GENE_CDD = 'gene_cdd'
GENE_GENOME = 'gene_genome'
GENE_GENSAT = 'gene_gensat'
GENE_GEO = 'gene_geo'
GENE_HOMOLOGENE = 'gene_homologene'
GENE_MAPVIEW = 'gene_mapview'
GENE_NUCCORE = 'gene_nuccore'
GENE_NUCCORE_MGC = 'gene_nuccore_mgc'
GENE_NUCEST = 'gene_nucest'
GENE_NUCEST_MGC = 'gene_nucest_mgc'
GENE_NUCGSS = 'gene_nucgss'
GENE_NUCGSS_MGC = 'gene_nucgss_mgc'
GENE_NUCLEOTIDE = 'gene_nucleotide'
GENE_NUCLEOTIDE_MGC = 'gene_nucleotide_mgc'
GENE_NUCLEOTIDE_MGC_URL = 'gene_nucleotide_mgc_url'
GENE_OMIA = 'gene_omia'
GENE_OMIM = 'gene_omim'
GENE_PCASSAY = 'gene_pcassay'
GENE_PCCOMPOUND = 'gene_pccompound'
GENE_PCSUBSTANCE = 'gene_pcsubstance'
GENE_PMC = 'gene_pmc'
GENE_PROBE = 'gene_probe'
GENE_PROTEIN = 'gene_protein'
GENE_PROTEINCLUSTERS = 'gene_proteinclusters'
GENE_PUBMED = 'gene_pubmed'
GENE_PUBMED_RIF = 'gene_pubmed_rif'
GENE_SNP = 'gene_snp'
GENE_SNP_GENEGENOTYPE = 'gene_snp_genegenotype'
GENE_SNP_GENEVIEW = 'gene_snp_geneview'
GENE_TAXONOMY = 'gene_taxonomy'
GENE_UNIGENE = 'gene_unigene'
GENE_UNISTS = 'gene_unists'
GENOME_ASSEMBLY = 'genome_assembly'
GENOME_GENE = 'genome_gene'
GENOME_GENOMEPRJ = 'genome_genomeprj'
GENOME_NUCCORE = 'genome_nuccore'
GENOME_NUCCORE_COMP = 'genome_nuccore_comp'
GENOME_NUCCORE_COMP_MRNA = 'genome_nuccore_comp_mrna'
GENOME_NUCCORE_MRNA = 'genome_nuccore_mrna'
GENOME_NUCCORE_SAMESPECIES = 'genome_nuccore_samespecies'
GENOME_NUCEST_COMP_MRNA = 'genome_nucest_comp_mrna'
GENOME_NUCGSS_COMP_MRNA = 'genome_nucgss_comp_mrna'
GENOME_NUCLEOTIDE_COMP = 'genome_nucleotide_comp'
GENOME_NUCLEOTIDE_COMP_MRNA = 'genome_nucleotide_comp_mrna'
GENOME_NUCLEOTIDE_COMP_PROTEIN = 'genome_nucleotide_comp_protein'
GENOME_NUCLEOTIDE_MRNA = 'genome_nucleotide_mrna'
GENOME_OMIM = 'genome_omim'
GENOME_PMC = 'genome_pmc'
GENOME_PROTEIN = 'genome_protein'
GENOME_PROTEINCLUSTERS = 'genome_proteinclusters'
GENOME_PUBMED = 'genome_pubmed'
GENOME_STRUCTURE = 'genome_structure'
GENOME_TAXONOMY = 'genome_taxonomy'
GENOME_TRACE = 'genome_trace'
GENOMEPRJ_GENOME = 'genomeprj_genome'
GENOMEPRJ_GENOMEPRJ = 'genomeprj_genomeprj'
GENOMEPRJ_NUCCORE = 'genomeprj_nuccore'
GENOMEPRJ_NUCCORE_INSDC = 'genomeprj_nuccore_insdc'
GENOMEPRJ_NUCCORE_INSDC_WGS = 'genomeprj_nuccore_insdc_wgs'
GENOMEPRJ_NUCCORE_MRNA = 'genomeprj_nuccore_mrna'
GENOMEPRJ_NUCCORE_ORGANELLA = 'genomeprj_nuccore_organella'
GENOMEPRJ_NUCCORE_ORGANELLE_SCAFFOLD = 'genomeprj_nuccore_organelle_scaffold'
GENOMEPRJ_NUCCORE_SCAFFOLD = 'genomeprj_nuccore_scaffold'
GENOMEPRJ_NUCCORE_WGS = 'genomeprj_nuccore_wgs'
GENOMEPRJ_NUCEST = 'genomeprj_nucest'
GENOMEPRJ_NUCEST_EST = 'genomeprj_nucest_est'
GENOMEPRJ_NUCEST_INSDC = 'genomeprj_nucest_insdc'
GENOMEPRJ_NUCEST_INSDC_WGS = 'genomeprj_nucest_insdc_wgs'
GENOMEPRJ_NUCEST_MRNA = 'genomeprj_nucest_mrna'
GENOMEPRJ_NUCEST_ORGANELLA = 'genomeprj_nucest_organella'
GENOMEPRJ_NUCEST_ORGANELLE_SCAFFOLD = 'genomeprj_nucest_organelle_scaffold'
GENOMEPRJ_NUCEST_SCAFFOLD = 'genomeprj_nucest_scaffold'
GENOMEPRJ_NUCEST_WGS = 'genomeprj_nucest_wgs'
GENOMEPRJ_NUCGSS = 'genomeprj_nucgss'
GENOMEPRJ_NUCGSS_INSDC = 'genomeprj_nucgss_insdc'
GENOMEPRJ_NUCGSS_INSDC_WGS = 'genomeprj_nucgss_insdc_wgs'
GENOMEPRJ_NUCGSS_MRNA = 'genomeprj_nucgss_mrna'
GENOMEPRJ_NUCGSS_ORGANELLA = 'genomeprj_nucgss_organella'
GENOMEPRJ_NUCGSS_ORGANELLE_SCAFFOLD = 'genomeprj_nucgss_organelle_scaffold'
GENOMEPRJ_NUCGSS_SCAFFOLD = 'genomeprj_nucgss_scaffold'
GENOMEPRJ_NUCGSS_WGS = 'genomeprj_nucgss_wgs'
GENOMEPRJ_NUCLEOTIDE = 'genomeprj_nucleotide'
GENOMEPRJ_NUCLEOTIDE_EST = 'genomeprj_nucleotide_est'
GENOMEPRJ_NUCLEOTIDE_INSDC = 'genomeprj_nucleotide_insdc'
GENOMEPRJ_NUCLEOTIDE_INSDC_WGS = 'genomeprj_nucleotide_insdc_wgs'
GENOMEPRJ_NUCLEOTIDE_MRNA = 'genomeprj_nucleotide_mrna'
GENOMEPRJ_NUCLEOTIDE_ORGANELLA = 'genomeprj_nucleotide_organella'
GENOMEPRJ_NUCLEOTIDE_ORGANELLE_SCAFFOLD = 'genomeprj_nucleotide_organelle_scaffold'
GENOMEPRJ_NUCLEOTIDE_SCAFFOLD = 'genomeprj_nucleotide_scaffold'
GENOMEPRJ_NUCLEOTIDE_WGS = 'genomeprj_nucleotide_wgs'
GENOMEPRJ_PMC = 'genomeprj_pmc'
GENOMEPRJ_POPSET = 'genomeprj_popset'
GENOMEPRJ_PROTEIN = 'genomeprj_protein'
GENOMEPRJ_PROTEIN_INSDC = 'genomeprj_protein_insdc'
GENOMEPRJ_PUBMED = 'genomeprj_pubmed'
GENOMEPRJ_TAXONOMY = 'genomeprj_taxonomy'
GENOMEPRJ_TRACE = 'genomeprj_trace'
GENSAT_GENE = 'gensat_gene'
GENSAT_GENSAT = 'gensat_gensat'
GENSAT_GEO = 'gensat_geo'
GENSAT_NUCCORE = 'gensat_nuccore'
GENSAT_NUCEST = 'gensat_nucest'
GENSAT_NUCGSS = 'gensat_nucgss'
GENSAT_NUCLEOTIDE = 'gensat_nucleotide'
GENSAT_PMC = 'gensat_pmc'
GENSAT_PUBMED = 'gensat_pubmed'
GENSAT_TAXONOMY = 'gensat_taxonomy'
GENSAT_UNIGENE = 'gensat_unigene'
GEO_GDS = 'geo_gds'
GEO_GENE = 'geo_gene'
GEO_GENSAT = 'geo_gensat'
GEO_GEO_CHR = 'geo_geo_chr'
GEO_GEO_HOMOLOGS = 'geo_geo_homologs'
GEO_GEO_PROF = 'geo_geo_prof'
GEO_GEO_SEQ = 'geo_geo_seq'
GEO_HOMOLOGENE = 'geo_homologene'
GEO_NUCCORE = 'geo_nuccore'
GEO_NUCEST = 'geo_nucest'
GEO_NUCGSS = 'geo_nucgss'
GEO_NUCLEOTIDE = 'geo_nucleotide'
GEO_OMIM = 'geo_omim'
GEO_PMC = 'geo_pmc'
GEO_PUBMED = 'geo_pubmed'
GEO_TAXONOMY = 'geo_taxonomy'
GEO_UNIGENE = 'geo_unigene'
HOMOLOGENE_CDD = 'homologene_cdd'
HOMOLOGENE_GENE = 'homologene_gene'
HOMOLOGENE_GEO = 'homologene_geo'
HOMOLOGENE_HOMOLOGENE = 'homologene_homologene'
HOMOLOGENE_NUCCORE = 'homologene_nuccore'
HOMOLOGENE_NUCEST = 'homologene_nucest'
HOMOLOGENE_NUCGSS = 'homologene_nucgss'
HOMOLOGENE_NUCLEOTIDE = 'homologene_nucleotide'
HOMOLOGENE_OMIA = 'homologene_omia'
HOMOLOGENE_OMIM = 'homologene_omim'
HOMOLOGENE_PMC = 'homologene_pmc'
HOMOLOGENE_PROTEIN = 'homologene_protein'
HOMOLOGENE_PUBMED = 'homologene_pubmed'
HOMOLOGENE_SNP = 'homologene_snp'
HOMOLOGENE_SNP_GENEGENOTYPE = 'homologene_snp_genegenotype'
HOMOLOGENE_TAXONOMY = 'homologene_taxonomy'
HOMOLOGENE_UNIGENE = 'homologene_unigene'
JOURNALS_GENOME = 'journals_genome'
JOURNALS_NUCCORE = 'journals_nuccore'
JOURNALS_NUCEST = 'journals_nucest'
JOURNALS_NUCGSS = 'journals_nucgss'
JOURNALS_PMC = 'journals_pmc'
JOURNALS_PMC_ARCHIVE = 'journals_pmc_archive'
JOURNALS_POPSET = 'journals_popset'
JOURNALS_PROTEIN = 'journals_protein'
JOURNALS_PUBMED = 'journals_pubmed'
MESH_PCCOMPOUND_EXPANDED = 'mesh_pccompound_expanded'
MESH_PCSUBSTANCE_EXPANDED = 'mesh_pcsubstance_expanded'
MESH_TAXONOMY = 'mesh_taxonomy'
NCBISEARCH_NCBISEARCH = 'ncbisearch_ncbisearch'
NUCCORE_ASSEMBLY = 'nuccore_assembly'
NUCCORE_COMP_NUCCORE = 'nuccore_comp_nuccore'
NUCCORE_GENE = 'nuccore_gene'
NUCCORE_GENOME = 'nuccore_genome'
NUCCORE_GENOME_COMP = 'nuccore_genome_comp'
NUCCORE_GENOME_MRNA = 'nuccore_genome_mrna'
NUCCORE_GENOME_SAMESPECIES = 'nuccore_genome_samespecies'
NUCCORE_GENOMEPRJ = 'nuccore_genomeprj'
NUCCORE_GENOMEPRJ_INSDC = 'nuccore_genomeprj_insdc'
NUCCORE_GENOMEPRJ_INSDC_WGS = 'nuccore_genomeprj_insdc_wgs'
NUCCORE_GENOMEPRJ_ORGANELLE_SCAFFOLD = 'nuccore_genomeprj_organelle_scaffold'
NUCCORE_GENOMEPRJ_SCAFFOLD = 'nuccore_genomeprj_scaffold'
NUCCORE_GENSAT = 'nuccore_gensat'
NUCCORE_GEO = 'nuccore_geo'
NUCCORE_HOMOLOGENE = 'nuccore_homologene'
NUCCORE_MAPVIEW = 'nuccore_mapview'
NUCCORE_MRNA_COMP_GENOME = 'nuccore_mrna_comp_genome'
NUCCORE_MRNA_GENOMEPRJ = 'nuccore_mrna_genomeprj'
NUCCORE_MRNA_NUCCORE = 'nuccore_mrna_nuccore'
NUCCORE_NUCCORE = 'nuccore_nuccore'
NUCCORE_NUCCORE_COMP = 'nuccore_nuccore_comp'
NUCCORE_NUCCORE_MGC_REFSEQ = 'nuccore_nuccore_mgc_refseq'
NUCCORE_NUCCORE_MRNA = 'nuccore_nuccore_mrna'
NUCCORE_OMIM = 'nuccore_omim'
NUCCORE_ORGANELLA_GENOMEPRJ = 'nuccore_organella_genomeprj'
NUCCORE_PCASSAY = 'nuccore_pcassay'
NUCCORE_PCASSAY_DNA_TARGET = 'nuccore_pcassay_dna_target'
NUCCORE_PCASSAY_RNA_TARGET = 'nuccore_pcassay_rna_target'
NUCCORE_PCCOMPOUND = 'nuccore_pccompound'
NUCCORE_PCSUBSTANCE = 'nuccore_pcsubstance'
NUCCORE_PMC = 'nuccore_pmc'
NUCCORE_POPSET = 'nuccore_popset'
NUCCORE_PROBE = 'nuccore_probe'
NUCCORE_PROTEIN = 'nuccore_protein'
NUCCORE_PROTEIN_MGC_URL = 'nuccore_protein_mgc_url'
NUCCORE_PROTEIN_WGS = 'nuccore_protein_wgs'
NUCCORE_PROTEINCLUSTERS = 'nuccore_proteinclusters'
NUCCORE_PUBMED = 'nuccore_pubmed'
NUCCORE_PUBMED_REFSEQ = 'nuccore_pubmed_refseq'
NUCCORE_SNP = 'nuccore_snp'
NUCCORE_SNP_GENEGENOTYPE = 'nuccore_snp_genegenotype'
NUCCORE_SNP_GENEVIEW = 'nuccore_snp_geneview'
NUCCORE_STRUCTURE = 'nuccore_structure'
NUCCORE_TAXONOMY = 'nuccore_taxonomy'
NUCCORE_TRACE = 'nuccore_trace'
NUCCORE_UNIGENE = 'nuccore_unigene'
NUCCORE_UNISTS = 'nuccore_unists'
NUCCORE_WGS_GENOMEPRJ = 'nuccore_wgs_genomeprj'
NUCEST_ASSEMBLY = 'nucest_assembly'
NUCEST_GENE = 'nucest_gene'
NUCEST_GENOMEPRJ_EST = 'nucest_genomeprj_est'
NUCEST_GENOMEPRJ_INSDC = 'nucest_genomeprj_insdc'
NUCEST_GENOMEPRJ_INSDC_WGS = 'nucest_genomeprj_insdc_wgs'
NUCEST_GENOMEPRJ_ORGANELLE_SCAFFOLD = 'nucest_genomeprj_organelle_scaffold'
NUCEST_GENOMEPRJ_SCAFFOLD = 'nucest_genomeprj_scaffold'
NUCEST_GENSAT = 'nucest_gensat'
NUCEST_GEO = 'nucest_geo'
NUCEST_HOMOLOGENE = 'nucest_homologene'
NUCEST_MAPVIEW = 'nucest_mapview'
NUCEST_MRNA_COMP_GENOME = 'nucest_mrna_comp_genome'
NUCEST_MRNA_GENOMEPRJ = 'nucest_mrna_genomeprj'
NUCEST_OMIM = 'nucest_omim'
NUCEST_ORGANELLA_GENOMEPRJ = 'nucest_organella_genomeprj'
NUCEST_PCASSAY = 'nucest_pcassay'
NUCEST_PCASSAY_DNA_TARGET = 'nucest_pcassay_dna_target'
NUCEST_PCASSAY_RNA_TARGET = 'nucest_pcassay_rna_target'
NUCEST_PCCOMPOUND = 'nucest_pccompound'
NUCEST_PCSUBSTANCE = 'nucest_pcsubstance'
NUCEST_PMC = 'nucest_pmc'
NUCEST_POPSET = 'nucest_popset'
NUCEST_PROBE = 'nucest_probe'
NUCEST_PROTEIN_MGC_URL = 'nucest_protein_mgc_url'
NUCEST_PROTEINCLUSTERS = 'nucest_proteinclusters'
NUCEST_PUBMED = 'nucest_pubmed'
NUCEST_PUBMED_REFSEQ = 'nucest_pubmed_refseq'
NUCEST_SNP = 'nucest_snp'
NUCEST_SNP_GENEGENOTYPE = 'nucest_snp_genegenotype'
NUCEST_SNP_GENEVIEW = 'nucest_snp_geneview'
NUCEST_STRUCTURE = 'nucest_structure'
NUCEST_TAXONOMY = 'nucest_taxonomy'
NUCEST_TRACE = 'nucest_trace'
NUCEST_UNIGENE = 'nucest_unigene'
NUCEST_UNISTS = 'nucest_unists'
NUCEST_WGS_GENOMEPRJ = 'nucest_wgs_genomeprj'
NUCGSS_ASSEMBLY = 'nucgss_assembly'
NUCGSS_GENE = 'nucgss_gene'
NUCGSS_GENOMEPRJ = 'nucgss_genomeprj'
NUCGSS_GENOMEPRJ_INSDC = 'nucgss_genomeprj_insdc'
NUCGSS_GENOMEPRJ_INSDC_WGS = 'nucgss_genomeprj_insdc_wgs'
NUCGSS_GENOMEPRJ_ORGANELLE_SCAFFOLD = 'nucgss_genomeprj_organelle_scaffold'
NUCGSS_GENOMEPRJ_SCAFFOLD = 'nucgss_genomeprj_scaffold'
NUCGSS_GENSAT = 'nucgss_gensat'
NUCGSS_GEO = 'nucgss_geo'
NUCGSS_HOMOLOGENE = 'nucgss_homologene'
NUCGSS_MAPVIEW = 'nucgss_mapview'
NUCGSS_MRNA_COMP_GENOME = 'nucgss_mrna_comp_genome'
NUCGSS_MRNA_GENOMEPRJ = 'nucgss_mrna_genomeprj'
NUCGSS_OMIM = 'nucgss_omim'
NUCGSS_ORGANELLA_GENOMEPRJ = 'nucgss_organella_genomeprj'
NUCGSS_PCASSAY = 'nucgss_pcassay'
NUCGSS_PCASSAY_DNA_TARGET = 'nucgss_pcassay_dna_target'
NUCGSS_PCASSAY_RNA_TARGET = 'nucgss_pcassay_rna_target'
NUCGSS_PCCOMPOUND = 'nucgss_pccompound'
NUCGSS_PCSUBSTANCE = 'nucgss_pcsubstance'
NUCGSS_PMC = 'nucgss_pmc'
NUCGSS_POPSET = 'nucgss_popset'
NUCGSS_PROBE = 'nucgss_probe'
NUCGSS_PROTEIN = 'nucgss_protein'
NUCGSS_PROTEIN_MGC_URL = 'nucgss_protein_mgc_url'
NUCGSS_PROTEINCLUSTERS = 'nucgss_proteinclusters'
NUCGSS_PUBMED = 'nucgss_pubmed'
NUCGSS_PUBMED_REFSEQ = 'nucgss_pubmed_refseq'
NUCGSS_SNP = 'nucgss_snp'
NUCGSS_SNP_GENEGENOTYPE = 'nucgss_snp_genegenotype'
NUCGSS_SNP_GENEVIEW = 'nucgss_snp_geneview'
NUCGSS_STRUCTURE = 'nucgss_structure'
NUCGSS_TAXONOMY = 'nucgss_taxonomy'
NUCGSS_TRACE = 'nucgss_trace'
NUCGSS_UNIGENE = 'nucgss_unigene'
NUCGSS_UNISTS = 'nucgss_unists'
NUCGSS_WGS_GENOMEPRJ = 'nucgss_wgs_genomeprj'
OMIA_GENE = 'omia_gene'
OMIA_HOMOLOGENE = 'omia_homologene'
OMIA_OMIM = 'omia_omim'
OMIA_PROTEIN = 'omia_protein'
OMIA_PUBMED = 'omia_pubmed'
OMIA_TAXONOMY = 'omia_taxonomy'
OMIA_UNIGENE = 'omia_unigene'
OMIA_UNISTS = 'omia_unists'
OMIM_BOOKS = 'omim_books'
OMIM_GENE = 'omim_gene'
OMIM_GENOME = 'omim_genome'
OMIM_GEO = 'omim_geo'
OMIM_HOMOLOGENE = 'omim_homologene'
OMIM_MAPVIEW = 'omim_mapview'
OMIM_NUCCORE = 'omim_nuccore'
OMIM_NUCEST = 'omim_nucest'
OMIM_NUCGSS = 'omim_nucgss'
OMIM_NUCLEOTIDE = 'omim_nucleotide'
OMIM_OMIA = 'omim_omia'
OMIM_OMIM = 'omim_omim'
OMIM_PCASSAY = 'omim_pcassay'
OMIM_PCCOMPOUND = 'omim_pccompound'
OMIM_PCSUBSTANCE = 'omim_pcsubstance'
OMIM_PMC = 'omim_pmc'
OMIM_PROTEIN = 'omim_protein'
OMIM_PUBMED_CALCULATED = 'omim_pubmed_calculated'
OMIM_PUBMED_CITED = 'omim_pubmed_cited'
OMIM_SNP = 'omim_snp'
OMIM_SNP_GENEGENOTYPE = 'omim_snp_genegenotype'
OMIM_SNP_GENEVIEW = 'omim_snp_geneview'
OMIM_STRUCTURE = 'omim_structure'
OMIM_UNIGENE = 'omim_unigene'
OMIM_UNISTS = 'omim_unists'
PCASSAY_GENE = 'pcassay_gene'
PCASSAY_NUCCORE = 'pcassay_nuccore'
PCASSAY_NUCCORE_DNA_TARGET = 'pcassay_nuccore_dna_target'
PCASSAY_NUCCORE_RNA_TARGET = 'pcassay_nuccore_rna_target'
PCASSAY_NUCEST = 'pcassay_nucest'
PCASSAY_NUCEST_DNA_TARGET = 'pcassay_nucest_dna_target'
PCASSAY_NUCEST_RNA_TARGET = 'pcassay_nucest_rna_target'
PCASSAY_NUCGSS = 'pcassay_nucgss'
PCASSAY_NUCGSS_DNA_TARGET = 'pcassay_nucgss_dna_target'
PCASSAY_NUCGSS_RNA_TARGET = 'pcassay_nucgss_rna_target'
PCASSAY_NUCLEOTIDE = 'pcassay_nucleotide'
PCASSAY_NUCLEOTIDE_DNA_TARGET = 'pcassay_nucleotide_dna_target'
PCASSAY_NUCLEOTIDE_RNA_TARGET = 'pcassay_nucleotide_rna_target'
PCASSAY_OMIM = 'pcassay_omim'
PCASSAY_PCASSAY_ACTIVITYNEIGHBOR = 'pcassay_pcassay_activityneighbor'
PCASSAY_PCASSAY_ACTIVITYNEIGHBOR_FIVE = 'pcassay_pcassay_activityneighbor_five'
PCASSAY_PCASSAY_NEIGHBOR = 'pcassay_pcassay_neighbor'
PCASSAY_PCASSAY_NEIGHBOR_FIVE = 'pcassay_pcassay_neighbor_five'
PCASSAY_PCASSAY_TARGETNEIGHBOR = 'pcassay_pcassay_targetneighbor'
PCASSAY_PCASSAY_TARGETNEIGHBOR_FIVE = 'pcassay_pcassay_targetneighbor_five'
PCASSAY_PCCOMPOUND = 'pcassay_pccompound'
PCASSAY_PCCOMPOUND_ACTIVE = 'pcassay_pccompound_active'
PCASSAY_PCCOMPOUND_FIVE = 'pcassay_pccompound_five'
PCASSAY_PCCOMPOUND_INACTIVE = 'pcassay_pccompound_inactive'
PCASSAY_PCCOMPOUND_INCONCLUSIVE = 'pcassay_pccompound_inconclusive'
PCASSAY_PCSUBSTANCE = 'pcassay_pcsubstance'
PCASSAY_PCSUBSTANCE_ACTIVE = 'pcassay_pcsubstance_active'
PCASSAY_PCSUBSTANCE_FIVE = 'pcassay_pcsubstance_five'
PCASSAY_PCSUBSTANCE_INACTIVE = 'pcassay_pcsubstance_inactive'
PCASSAY_PCSUBSTANCE_INCONCLUSIVE = 'pcassay_pcsubstance_inconclusive'
PCASSAY_PMC = 'pcassay_pmc'
PCASSAY_PROTEIN = 'pcassay_protein'
PCASSAY_PROTEIN_TARGET = 'pcassay_protein_target'
PCASSAY_PUBMED = 'pcassay_pubmed'
PCASSAY_STRUCTURE = 'pcassay_structure'
PCASSAY_TAXONOMY = 'pcassay_taxonomy'
PCCOMPOUND_GENE = 'pccompound_gene'
PCCOMPOUND_MESH = 'pccompound_mesh'
PCCOMPOUND_NUCCORE = 'pccompound_nuccore'
PCCOMPOUND_NUCEST = 'pccompound_nucest'
PCCOMPOUND_NUCGSS = 'pccompound_nucgss'
PCCOMPOUND_NUCLEOTIDE = 'pccompound_nucleotide'
PCCOMPOUND_OMIM = 'pccompound_omim'
PCCOMPOUND_PCASSAY = 'pccompound_pcassay'
PCCOMPOUND_PCASSAY_ACTIVE = 'pccompound_pcassay_active'
PCCOMPOUND_PCASSAY_INACTIVE = 'pccompound_pcassay_inactive'
PCCOMPOUND_PCASSAY_INCONCLUSIVE = 'pccompound_pcassay_inconclusive'
PCCOMPOUND_PCCOMPOUND = 'pccompound_pccompound'
PCCOMPOUND_PCCOMPOUND_MIXTURE = 'pccompound_pccompound_mixture'
PCCOMPOUND_PCCOMPOUND_PARENT_CONNECTIVITY_POPUP = 'pccompound_pccompound_parent_connectivity_popup'
PCCOMPOUND_PCCOMPOUND_PARENT_CONNECTIVITY_PULLDOWN = 'pccompound_pccompound_parent_connectivity_pulldown'
PCCOMPOUND_PCCOMPOUND_PARENT_ISOTOPES_POPUP = 'pccompound_pccompound_parent_isotopes_popup'
PCCOMPOUND_PCCOMPOUND_PARENT_ISOTOPES_PULLDOWN = 'pccompound_pccompound_parent_isotopes_pulldown'
PCCOMPOUND_PCCOMPOUND_PARENT_POPUP = 'pccompound_pccompound_parent_popup'
PCCOMPOUND_PCCOMPOUND_PARENT_PULLDOWN = 'pccompound_pccompound_parent_pulldown'
PCCOMPOUND_PCCOMPOUND_PARENT_STEREO_POPUP = 'pccompound_pccompound_parent_stereo_popup'
PCCOMPOUND_PCCOMPOUND_PARENT_STEREO_PULLDOWN = 'pccompound_pccompound_parent_stereo_pulldown'
PCCOMPOUND_PCCOMPOUND_PARENT_TAUTOMER_POPUP = 'pccompound_pccompound_parent_tautomer_popup'
PCCOMPOUND_PCCOMPOUND_PARENT_TAUTOMER_PULLDOWN = 'pccompound_pccompound_parent_tautomer_pulldown'
PCCOMPOUND_PCCOMPOUND_SAMEANYTAUTOMER_POPUP = 'pccompound_pccompound_sameanytautomer_popup'
PCCOMPOUND_PCCOMPOUND_SAMEANYTAUTOMER_PULLDOWN = 'pccompound_pccompound_sameanytautomer_pulldown'
PCCOMPOUND_PCCOMPOUND_SAMECONNECTIVITY_POPUP = 'pccompound_pccompound_sameconnectivity_popup'
PCCOMPOUND_PCCOMPOUND_SAMECONNECTIVITY_PULLDOWN = 'pccompound_pccompound_sameconnectivity_pulldown'
PCCOMPOUND_PCCOMPOUND_SAMEISOTOPIC_POPUP = 'pccompound_pccompound_sameisotopic_popup'
PCCOMPOUND_PCCOMPOUND_SAMEISOTOPIC_PULLDOWN = 'pccompound_pccompound_sameisotopic_pulldown'
PCCOMPOUND_PCCOMPOUND_SAMESTEREOCHEM_POPUP = 'pccompound_pccompound_samestereochem_popup'
PCCOMPOUND_PCCOMPOUND_SAMESTEREOCHEM_PULLDOWN = 'pccompound_pccompound_samestereochem_pulldown'
PCCOMPOUND_PCSUBSTANCE = 'pccompound_pcsubstance'
PCCOMPOUND_PCSUBSTANCE_SAME = 'pccompound_pcsubstance_same'
PCCOMPOUND_PMC = 'pccompound_pmc'
PCCOMPOUND_PROBE = 'pccompound_probe'
PCCOMPOUND_PROTEIN = 'pccompound_protein'
PCCOMPOUND_PUBMED = 'pccompound_pubmed'
PCCOMPOUND_PUBMED_MESH = 'pccompound_pubmed_mesh'
PCCOMPOUND_PUBMED_PUBLISHER = 'pccompound_pubmed_publisher'
PCCOMPOUND_STRUCTURE = 'pccompound_structure'
PCCOMPOUND_TAXONOMY = 'pccompound_taxonomy'
PCSUBSTANCE_BOOKS = 'pcsubstance_books'
PCSUBSTANCE_GENE = 'pcsubstance_gene'
PCSUBSTANCE_MESH = 'pcsubstance_mesh'
PCSUBSTANCE_NUCCORE = 'pcsubstance_nuccore'
PCSUBSTANCE_NUCEST = 'pcsubstance_nucest'
PCSUBSTANCE_NUCGSS = 'pcsubstance_nucgss'
PCSUBSTANCE_NUCLEOTIDE = 'pcsubstance_nucleotide'
PCSUBSTANCE_OMIM = 'pcsubstance_omim'
PCSUBSTANCE_PCASSAY = 'pcsubstance_pcassay'
PCSUBSTANCE_PCASSAY_ACTIVE = 'pcsubstance_pcassay_active'
PCSUBSTANCE_PCASSAY_INACTIVE = 'pcsubstance_pcassay_inactive'
PCSUBSTANCE_PCASSAY_INCONCLUSIVE = 'pcsubstance_pcassay_inconclusive'
PCSUBSTANCE_PCCOMPOUND = 'pcsubstance_pccompound'
PCSUBSTANCE_PCCOMPOUND_SAME = 'pcsubstance_pccompound_same'
PCSUBSTANCE_PCSUBSTANCE = 'pcsubstance_pcsubstance'
PCSUBSTANCE_PCSUBSTANCE_PARENT_CONNECTIVITY_POPUP = 'pcsubstance_pcsubstance_parent_connectivity_popup'
PCSUBSTANCE_PCSUBSTANCE_PARENT_CONNECTIVITY_PULLDO = 'pcsubstance_pcsubstance_parent_connectivity_pulldo'
PCSUBSTANCE_PCSUBSTANCE_PARENT_ISOTOPES_POPUP = 'pcsubstance_pcsubstance_parent_isotopes_popup'
PCSUBSTANCE_PCSUBSTANCE_PARENT_ISOTOPES_PULLDOWN = 'pcsubstance_pcsubstance_parent_isotopes_pulldown'
PCSUBSTANCE_PCSUBSTANCE_PARENT_POPUP = 'pcsubstance_pcsubstance_parent_popup'
PCSUBSTANCE_PCSUBSTANCE_PARENT_PULLDOWN = 'pcsubstance_pcsubstance_parent_pulldown'
PCSUBSTANCE_PCSUBSTANCE_PARENT_STEREO_POPUP = 'pcsubstance_pcsubstance_parent_stereo_popup'
PCSUBSTANCE_PCSUBSTANCE_PARENT_STEREO_PULLDOWN = 'pcsubstance_pcsubstance_parent_stereo_pulldown'
PCSUBSTANCE_PCSUBSTANCE_PARENT_TAUTOMER_POPUP = 'pcsubstance_pcsubstance_parent_tautomer_popup'
PCSUBSTANCE_PCSUBSTANCE_PARENT_TAUTOMER_PULLDOWN = 'pcsubstance_pcsubstance_parent_tautomer_pulldown'
PCSUBSTANCE_PCSUBSTANCE_SAME_POPUP = 'pcsubstance_pcsubstance_same_popup'
PCSUBSTANCE_PCSUBSTANCE_SAME_PULLDOWN = 'pcsubstance_pcsubstance_same_pulldown'
PCSUBSTANCE_PCSUBSTANCE_SAMEANYTAUTOMER_POPUP = 'pcsubstance_pcsubstance_sameanytautomer_popup'
PCSUBSTANCE_PCSUBSTANCE_SAMEANYTAUTOMER_PULLDOWN = 'pcsubstance_pcsubstance_sameanytautomer_pulldown'
PCSUBSTANCE_PCSUBSTANCE_SAMECONNECTIVITY_POPUP = 'pcsubstance_pcsubstance_sameconnectivity_popup'
PCSUBSTANCE_PCSUBSTANCE_SAMECONNECTIVITY_PULLDOW = 'pcsubstance_pcsubstance_sameconnectivity_pulldow'
PCSUBSTANCE_PCSUBSTANCE_SAMEISOTOPIC_POPUP = 'pcsubstance_pcsubstance_sameisotopic_popup'
PCSUBSTANCE_PCSUBSTANCE_SAMEISOTOPIC_PULLDOWN = 'pcsubstance_pcsubstance_sameisotopic_pulldown'
PCSUBSTANCE_PCSUBSTANCE_SAMESTEREOCHEM_POPUP = 'pcsubstance_pcsubstance_samestereochem_popup'
PCSUBSTANCE_PCSUBSTANCE_SAMESTEREOCHEM_PULLDOWN = 'pcsubstance_pcsubstance_samestereochem_pulldown'
PCSUBSTANCE_PMC = 'pcsubstance_pmc'
PCSUBSTANCE_PROBE = 'pcsubstance_probe'
PCSUBSTANCE_PROTEIN = 'pcsubstance_protein'
PCSUBSTANCE_PUBMED = 'pcsubstance_pubmed'
PCSUBSTANCE_PUBMED_MESH = 'pcsubstance_pubmed_mesh'
PCSUBSTANCE_PUBMED_PUBLISHER = 'pcsubstance_pubmed_publisher'
PCSUBSTANCE_STRUCTURE = 'pcsubstance_structure'
PCSUBSTANCE_TAXONOMY = 'pcsubstance_taxonomy'
PMC_BOOKS_REFS = 'pmc_books_refs'
PMC_CANCERCHROMOSOMES = 'pmc_cancerchromosomes'
PMC_CDD = 'pmc_cdd'
PMC_DOMAINS = 'pmc_domains'
PMC_GDS = 'pmc_gds'
PMC_GENE = 'pmc_gene'
PMC_GENOME = 'pmc_genome'
PMC_GENOMEPRJ = 'pmc_genomeprj'
PMC_GENSAT = 'pmc_gensat'
PMC_GEO = 'pmc_geo'
PMC_HOMOLOGENE = 'pmc_homologene'
PMC_NUCCORE = 'pmc_nuccore'
PMC_NUCEST = 'pmc_nucest'
PMC_NUCGSS = 'pmc_nucgss'
PMC_NUCLEOTIDE = 'pmc_nucleotide'
PMC_OMIM = 'pmc_omim'
PMC_PCASSAY = 'pmc_pcassay'
PMC_PCCOMPOUND = 'pmc_pccompound'
PMC_PCSUBSTANCE = 'pmc_pcsubstance'
PMC_PMC_REFS = 'pmc_pmc_refs'
PMC_POPSET = 'pmc_popset'
PMC_PROTEIN = 'pmc_protein'
PMC_PUBMED = 'pmc_pubmed'
PMC_REFS_PUBMED = 'pmc_refs_pubmed'
PMC_SNP = 'pmc_snp'
PMC_STRUCTURE = 'pmc_structure'
PMC_TAXONOMY = 'pmc_taxonomy'
PMC_UNISTS = 'pmc_unists'
POPSET_GENOMEPRJ = 'popset_genomeprj'
POPSET_NUCCORE = 'popset_nuccore'
POPSET_PMC = 'popset_pmc'
POPSET_PROTEIN = 'popset_protein'
POPSET_PUBMED = 'popset_pubmed'
POPSET_TAXONOMY = 'popset_taxonomy'
PROBE_GENE = 'probe_gene'
PROBE_NUCCORE = 'probe_nuccore'
PROBE_NUCEST = 'probe_nucest'
PROBE_NUCGSS = 'probe_nucgss'
PROBE_NUCLEOTIDE = 'probe_nucleotide'
PROBE_PCCOMPOUND = 'probe_pccompound'
PROBE_PCSUBSTANCE = 'probe_pcsubstance'
PROBE_PROBE = 'probe_probe'
PROBE_PUBMED = 'probe_pubmed'
PROBE_SNP = 'probe_snp'
PROBE_TAXONOMY = 'probe_taxonomy'
PROTEIN_CDD = 'protein_cdd'
PROTEIN_CDD_SUMMARY = 'protein_cdd_summary'
PROTEIN_DOMAINS = 'protein_domains'
PROTEIN_GENE = 'protein_gene'
PROTEIN_GENOME = 'protein_genome'
PROTEIN_GENOMEPRJ = 'protein_genomeprj'
PROTEIN_GENOMEPRJ_INSDC = 'protein_genomeprj_insdc'
PROTEIN_HOMOLOGENE = 'protein_homologene'
PROTEIN_MAPVIEW = 'protein_mapview'
PROTEIN_NUCCORE = 'protein_nuccore'
PROTEIN_NUCCORE_MGC = 'protein_nuccore_mgc'
PROTEIN_NUCCORE_WGS = 'protein_nuccore_wgs'
PROTEIN_NUCEST_MGC = 'protein_nucest_mgc'
PROTEIN_NUCGSS = 'protein_nucgss'
PROTEIN_NUCGSS_MGC = 'protein_nucgss_mgc'
PROTEIN_NUCLEOTIDE_COMP_GENOME = 'protein_nucleotide_comp_genome'
PROTEIN_NUCLEOTIDE_MGC = 'protein_nucleotide_mgc'
PROTEIN_NUCLEOTIDE_MGC_URL = 'protein_nucleotide_mgc_url'
PROTEIN_NUCLEOTIDE_WGS = 'protein_nucleotide_wgs'
PROTEIN_OMIA = 'protein_omia'
PROTEIN_OMIM = 'protein_omim'
PROTEIN_PCASSAY = 'protein_pcassay'
PROTEIN_PCASSAY_TARGET = 'protein_pcassay_target'
PROTEIN_PCCOMPOUND = 'protein_pccompound'
PROTEIN_PCSUBSTANCE = 'protein_pcsubstance'
PROTEIN_PMC = 'protein_pmc'
PROTEIN_POPSET = 'protein_popset'
PROTEIN_PROTEIN = 'protein_protein'
PROTEIN_PROTEIN_CDART_SUMMARY = 'protein_protein_cdart_summary'
PROTEIN_PROTEIN_REFSEQ2UNIPROT = 'protein_protein_refseq2uniprot'
PROTEIN_PROTEIN_UNIPROT2REFSEQ = 'protein_protein_uniprot2refseq'
PROTEIN_PROTEINCLUSTERS = 'protein_proteinclusters'
PROTEIN_PUBMED = 'protein_pubmed'
PROTEIN_PUBMED_REFSEQ = 'protein_pubmed_refseq'
PROTEIN_SNP = 'protein_snp'
PROTEIN_SNP_GENEGENOTYPE = 'protein_snp_genegenotype'
PROTEIN_SNP_GENEVIEW = 'protein_snp_geneview'
PROTEIN_STRUCTURE = 'protein_structure'
PROTEIN_STRUCTURE_RELATED = 'protein_structure_related'
PROTEIN_TAXONOMY = 'protein_taxonomy'
PROTEIN_UNIGENE = 'protein_unigene'
PROTEINCLUSTERS_GENE = 'proteinclusters_gene'
PROTEINCLUSTERS_GENOME = 'proteinclusters_genome'
PROTEINCLUSTERS_NUCCORE = 'proteinclusters_nuccore'
PROTEINCLUSTERS_NUCEST = 'proteinclusters_nucest'
PROTEINCLUSTERS_NUCGSS = 'proteinclusters_nucgss'
PROTEINCLUSTERS_NUCLEOTIDE = 'proteinclusters_nucleotide'
PROTEINCLUSTERS_PROTEIN = 'proteinclusters_protein'
PROTEINCLUSTERS_PUBMED_CDD = 'proteinclusters_pubmed_cdd'
PROTEINCLUSTERS_PUBMED_CURATED = 'proteinclusters_pubmed_curated'
PROTEINCLUSTERS_PUBMED_GENERIF = 'proteinclusters_pubmed_generif'
PROTEINCLUSTERS_PUBMED_HOMOLOGY = 'proteinclusters_pubmed_homology'
PROTEINCLUSTERS_PUBMED_REFSEQ = 'proteinclusters_pubmed_refseq'
PROTEINCLUSTERS_PUBMED_STRUCTURE = 'proteinclusters_pubmed_structure'
PROTEINCLUSTERS_PUBMED_SWISSPROT = 'proteinclusters_pubmed_swissprot'
PUBMED_BOOKS_REFS = 'pubmed_books_refs'
PUBMED_CANCERCHROMOSOMES = 'pubmed_cancerchromosomes'
PUBMED_CDD = 'pubmed_cdd'
PUBMED_DOMAINS = 'pubmed_domains'
PUBMED_GDS = 'pubmed_gds'
PUBMED_GENE = 'pubmed_gene'
PUBMED_GENE_RIF = 'pubmed_gene_rif'
PUBMED_GENOME = 'pubmed_genome'
PUBMED_GENOMEPRJ = 'pubmed_genomeprj'
PUBMED_GENSAT = 'pubmed_gensat'
PUBMED_GEO = 'pubmed_geo'
PUBMED_HOMOLOGENE = 'pubmed_homologene'
PUBMED_NUCCORE = 'pubmed_nuccore'
PUBMED_NUCCORE_REFSEQ = 'pubmed_nuccore_refseq'
PUBMED_NUCEST = 'pubmed_nucest'
PUBMED_NUCEST_REFSEQ = 'pubmed_nucest_refseq'
PUBMED_NUCGSS = 'pubmed_nucgss'
PUBMED_NUCGSS_REFSEQ = 'pubmed_nucgss_refseq'
PUBMED_NUCLEOTIDE = 'pubmed_nucleotide'
PUBMED_NUCLEOTIDE_REFSEQ = 'pubmed_nucleotide_refseq'
PUBMED_OMIA = 'pubmed_omia'
PUBMED_OMIM_CALCULATED = 'pubmed_omim_calculated'
PUBMED_OMIM_CITED = 'pubmed_omim_cited'
PUBMED_PCASSAY = 'pubmed_pcassay'
PUBMED_PCCOMPOUND = 'pubmed_pccompound'
PUBMED_PCCOMPOUND_MESH = 'pubmed_pccompound_mesh'
PUBMED_PCCOMPOUND_PUBLISHER = 'pubmed_pccompound_publisher'
PUBMED_PCSUBSTANCE = 'pubmed_pcsubstance'
PUBMED_PCSUBSTANCE_MESH = 'pubmed_pcsubstance_mesh'
PUBMED_PCSUBSTANCE_PUBLISHER = 'pubmed_pcsubstance_publisher'
PUBMED_PMC = 'pubmed_pmc'
PUBMED_PMC_LOCAL = 'pubmed_pmc_local'
PUBMED_PMC_REFS = 'pubmed_pmc_refs'
PUBMED_POPSET = 'pubmed_popset'
PUBMED_PROBE = 'pubmed_probe'
PUBMED_PROTEIN = 'pubmed_protein'
PUBMED_PROTEIN_REFSEQ = 'pubmed_protein_refseq'
PUBMED_PROTEINCLUSTERS = 'pubmed_proteinclusters'
PUBMED_PUBMED = 'pubmed_pubmed'
PUBMED_PUBMED_REFS = 'pubmed_pubmed_refs'
PUBMED_SNP = 'pubmed_snp'
PUBMED_STRUCTURE = 'pubmed_structure'
PUBMED_TAXONOMY_ENTREZ = 'pubmed_taxonomy_entrez'
PUBMED_UNIGENE = 'pubmed_unigene'
PUBMED_UNISTS = 'pubmed_unists'
SNP_GENE = 'snp_gene'
SNP_HAPVARSET = 'snp_hapvarset'
SNP_HOMOLOGENE = 'snp_homologene'
SNP_NUCCORE = 'snp_nuccore'
SNP_NUCEST = 'snp_nucest'
SNP_NUCGSS = 'snp_nucgss'
SNP_NUCLEOTIDE = 'snp_nucleotide'
SNP_OMIM = 'snp_omim'
SNP_PMC = 'snp_pmc'
SNP_PROBE = 'snp_probe'
SNP_PROTEIN = 'snp_protein'
SNP_PUBMED = 'snp_pubmed'
SNP_SNP_GENEGENOTYPE = 'snp_snp_genegenotype'
SNP_STRUCTURE = 'snp_structure'
SNP_TAXONOMY = 'snp_taxonomy'
SNP_TRACE = 'snp_trace'
SNP_UNIGENE = 'snp_unigene'
SNP_UNISTS = 'snp_unists'
STRUCTURE_CDD = 'structure_cdd'
STRUCTURE_DOMAINS = 'structure_domains'
STRUCTURE_GENOME = 'structure_genome'
STRUCTURE_MMDB = 'structure_mmdb'
STRUCTURE_NUCCORE = 'structure_nuccore'
STRUCTURE_NUCEST = 'structure_nucest'
STRUCTURE_NUCGSS = 'structure_nucgss'
STRUCTURE_NUCLEOTIDE = 'structure_nucleotide'
STRUCTURE_OMIM = 'structure_omim'
STRUCTURE_PCASSAY = 'structure_pcassay'
STRUCTURE_PCCOMPOUND = 'structure_pccompound'
STRUCTURE_PCSUBSTANCE = 'structure_pcsubstance'
STRUCTURE_PMC = 'structure_pmc'
STRUCTURE_PROTEIN = 'structure_protein'
STRUCTURE_PUBMED = 'structure_pubmed'
STRUCTURE_SNP = 'structure_snp'
STRUCTURE_TAXONOMY = 'structure_taxonomy'
TAXONOMY_CDD = 'taxonomy_cdd'
TAXONOMY_DOMAINS = 'taxonomy_domains'
TAXONOMY_GDS = 'taxonomy_gds'
TAXONOMY_GENE_EXP = 'taxonomy_gene_exp'
TAXONOMY_GENOME_EXP = 'taxonomy_genome_exp'
TAXONOMY_GENOMEPRJ = 'taxonomy_genomeprj'
TAXONOMY_GENSAT = 'taxonomy_gensat'
TAXONOMY_GEO_EXP = 'taxonomy_geo_exp'
TAXONOMY_HOMOLOGENE = 'taxonomy_homologene'
TAXONOMY_MESH = 'taxonomy_mesh'
TAXONOMY_NUCCORE = 'taxonomy_nuccore'
TAXONOMY_NUCEST = 'taxonomy_nucest'
TAXONOMY_NUCGSS = 'taxonomy_nucgss'
TAXONOMY_NUCLEOTIDE_EXP = 'taxonomy_nucleotide_exp'
TAXONOMY_OMIA = 'taxonomy_omia'
TAXONOMY_PCASSAY = 'taxonomy_pcassay'
TAXONOMY_PCCOMPOUND = 'taxonomy_pccompound'
TAXONOMY_PCSUBSTANCE = 'taxonomy_pcsubstance'
TAXONOMY_PMC = 'taxonomy_pmc'
TAXONOMY_POPSET = 'taxonomy_popset'
TAXONOMY_PROBE = 'taxonomy_probe'
TAXONOMY_PROTEIN_EXP = 'taxonomy_protein_exp'
TAXONOMY_PUBMED = 'taxonomy_pubmed'
TAXONOMY_PUBMED_ENTREZ = 'taxonomy_pubmed_entrez'
TAXONOMY_SNP_EXP = 'taxonomy_snp_exp'
TAXONOMY_STRUCTURE_EXP = 'taxonomy_structure_exp'
TAXONOMY_UNIGENE = 'taxonomy_unigene'
TAXONOMY_UNISTS = 'taxonomy_unists'
UNIGENE_GENE = 'unigene_gene'
UNIGENE_GENSAT = 'unigene_gensat'
UNIGENE_GEO = 'unigene_geo'
UNIGENE_HOMOLOGENE = 'unigene_homologene'
UNIGENE_NUCCORE = 'unigene_nuccore'
UNIGENE_NUCCORE_MGC = 'unigene_nuccore_mgc'
UNIGENE_NUCEST = 'unigene_nucest'
UNIGENE_NUCEST_MGC = 'unigene_nucest_mgc'
UNIGENE_NUCGSS = 'unigene_nucgss'
UNIGENE_NUCGSS_MGC = 'unigene_nucgss_mgc'
UNIGENE_NUCLEOTIDE = 'unigene_nucleotide'
UNIGENE_NUCLEOTIDE_MGC = 'unigene_nucleotide_mgc'
UNIGENE_NUCLEOTIDE_MGC_URL = 'unigene_nucleotide_mgc_url'
UNIGENE_OMIA = 'unigene_omia'
UNIGENE_OMIM = 'unigene_omim'
UNIGENE_PROTEIN = 'unigene_protein'
UNIGENE_PUBMED = 'unigene_pubmed'
UNIGENE_SNP = 'unigene_snp'
UNIGENE_SNP_GENEGENOTYPE = 'unigene_snp_genegenotype'
UNIGENE_SNP_GENEVIEW = 'unigene_snp_geneview'
UNIGENE_TAXONOMY = 'unigene_taxonomy'
UNIGENE_UNIGENE_EXPRESSION = 'unigene_unigene_expression'
UNIGENE_UNIGENE_HOMOLOGOUS = 'unigene_unigene_homologous'
UNIGENE_UNISTS = 'unigene_unists'
UNISTS_GENE = 'unists_gene'
UNISTS_NUCCORE = 'unists_nuccore'
UNISTS_NUCEST = 'unists_nucest'
UNISTS_NUCGSS = 'unists_nucgss'
UNISTS_NUCLEOTIDE = 'unists_nucleotide'
UNISTS_OMIA = 'unists_omia'
UNISTS_OMIM = 'unists_omim'
UNISTS_PMC = 'unists_pmc'
UNISTS_PUBMED = 'unists_pubmed'
UNISTS_SNP = 'unists_snp'
UNISTS_TAXONOMY = 'unists_taxonomy'
UNISTS_UNIGENE = 'unists_unigene'

linklist = (
    BOOKS_GENE,
    BOOKS_OMIM,
    BOOKS_PCSUBSTANCE,
    BOOKS_PMC_REFS,
    BOOKS_PUBMED_REFS,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CASECELL,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CELLCASE,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOCGH,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOCLINCGH,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOCLINSKY,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTODIAGCGH,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTODIAGSKY,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_CYTOSKY,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_DIAG,
    CANCERCHROMOSOMES_CANCERCHROMOSOMES_TEXTUAL,
    CANCERCHROMOSOMES_PMC,
    CANCERCHROMOSOMES_PUBMED,
    CDD_CDD_RELATED,
    CDD_GENE,
    CDD_HOMOLOGENE,
    CDD_PMC,
    CDD_PROTEIN,
    CDD_PROTEIN_SUMMARY,
    CDD_PUBMED,
    CDD_STRUCTURE,
    CDD_TAXONOMY,
    DOMAINS_DOMAINS_NEW,
    DOMAINS_PMC,
    DOMAINS_PROTEIN,
    DOMAINS_PUBMED,
    DOMAINS_STRUCTURE,
    DOMAINS_TAXONOMY,
    DOMAINS_VAST,
    GDS_GDS,
    GDS_GEO,
    GDS_GEO_URL,
    GDS_PMC,
    GDS_PUBMED,
    GDS_TAXONOMY,
    GENE_BOOKS,
    GENE_CDD,
    GENE_GENOME,
    GENE_GENSAT,
    GENE_GEO,
    GENE_HOMOLOGENE,
    GENE_MAPVIEW,
    GENE_NUCCORE,
    GENE_NUCCORE_MGC,
    GENE_NUCEST,
    GENE_NUCEST_MGC,
    GENE_NUCGSS,
    GENE_NUCGSS_MGC,
    GENE_NUCLEOTIDE,
    GENE_NUCLEOTIDE_MGC,
    GENE_NUCLEOTIDE_MGC_URL,
    GENE_OMIA,
    GENE_OMIM,
    GENE_PCASSAY,
    GENE_PCCOMPOUND,
    GENE_PCSUBSTANCE,
    GENE_PMC,
    GENE_PROBE,
    GENE_PROTEIN,
    GENE_PROTEINCLUSTERS,
    GENE_PUBMED,
    GENE_PUBMED_RIF,
    GENE_SNP,
    GENE_SNP_GENEGENOTYPE,
    GENE_SNP_GENEVIEW,
    GENE_TAXONOMY,
    GENE_UNIGENE,
    GENE_UNISTS,
    GENOME_ASSEMBLY,
    GENOME_GENE,
    GENOME_GENOMEPRJ,
    GENOME_NUCCORE,
    GENOME_NUCCORE_COMP,
    GENOME_NUCCORE_COMP_MRNA,
    GENOME_NUCCORE_MRNA,
    GENOME_NUCCORE_SAMESPECIES,
    GENOME_NUCEST_COMP_MRNA,
    GENOME_NUCGSS_COMP_MRNA,
    GENOME_NUCLEOTIDE_COMP,
    GENOME_NUCLEOTIDE_COMP_MRNA,
    GENOME_NUCLEOTIDE_COMP_PROTEIN,
    GENOME_NUCLEOTIDE_MRNA,
    GENOME_OMIM,
    GENOME_PMC,
    GENOME_PROTEIN,
    GENOME_PROTEINCLUSTERS,
    GENOME_PUBMED,
    GENOME_STRUCTURE,
    GENOME_TAXONOMY,
    GENOME_TRACE,
    GENOMEPRJ_GENOME,
    GENOMEPRJ_GENOMEPRJ,
    GENOMEPRJ_NUCCORE,
    GENOMEPRJ_NUCCORE_INSDC,
    GENOMEPRJ_NUCCORE_INSDC_WGS,
    GENOMEPRJ_NUCCORE_MRNA,
    GENOMEPRJ_NUCCORE_ORGANELLA,
    GENOMEPRJ_NUCCORE_ORGANELLE_SCAFFOLD,
    GENOMEPRJ_NUCCORE_SCAFFOLD,
    GENOMEPRJ_NUCCORE_WGS,
    GENOMEPRJ_NUCEST,
    GENOMEPRJ_NUCEST_EST,
    GENOMEPRJ_NUCEST_INSDC,
    GENOMEPRJ_NUCEST_INSDC_WGS,
    GENOMEPRJ_NUCEST_MRNA,
    GENOMEPRJ_NUCEST_ORGANELLA,
    GENOMEPRJ_NUCEST_ORGANELLE_SCAFFOLD,
    GENOMEPRJ_NUCEST_SCAFFOLD,
    GENOMEPRJ_NUCEST_WGS,
    GENOMEPRJ_NUCGSS,
    GENOMEPRJ_NUCGSS_INSDC,
    GENOMEPRJ_NUCGSS_INSDC_WGS,
    GENOMEPRJ_NUCGSS_MRNA,
    GENOMEPRJ_NUCGSS_ORGANELLA,
    GENOMEPRJ_NUCGSS_ORGANELLE_SCAFFOLD,
    GENOMEPRJ_NUCGSS_SCAFFOLD,
    GENOMEPRJ_NUCGSS_WGS,
    GENOMEPRJ_NUCLEOTIDE,
    GENOMEPRJ_NUCLEOTIDE_EST,
    GENOMEPRJ_NUCLEOTIDE_INSDC,
    GENOMEPRJ_NUCLEOTIDE_INSDC_WGS,
    GENOMEPRJ_NUCLEOTIDE_MRNA,
    GENOMEPRJ_NUCLEOTIDE_ORGANELLA,
    GENOMEPRJ_NUCLEOTIDE_ORGANELLE_SCAFFOLD,
    GENOMEPRJ_NUCLEOTIDE_SCAFFOLD,
    GENOMEPRJ_NUCLEOTIDE_WGS,
    GENOMEPRJ_PMC,
    GENOMEPRJ_POPSET,
    GENOMEPRJ_PROTEIN,
    GENOMEPRJ_PROTEIN_INSDC,
    GENOMEPRJ_PUBMED,
    GENOMEPRJ_TAXONOMY,
    GENOMEPRJ_TRACE,
    GENSAT_GENE,
    GENSAT_GENSAT,
    GENSAT_GEO,
    GENSAT_NUCCORE,
    GENSAT_NUCEST,
    GENSAT_NUCGSS,
    GENSAT_NUCLEOTIDE,
    GENSAT_PMC,
    GENSAT_PUBMED,
    GENSAT_TAXONOMY,
    GENSAT_UNIGENE,
    GEO_GDS,
    GEO_GENE,
    GEO_GENSAT,
    GEO_GEO_CHR,
    GEO_GEO_HOMOLOGS,
    GEO_GEO_PROF,
    GEO_GEO_SEQ,
    GEO_HOMOLOGENE,
    GEO_NUCCORE,
    GEO_NUCEST,
    GEO_NUCGSS,
    GEO_NUCLEOTIDE,
    GEO_OMIM,
    GEO_PMC,
    GEO_PUBMED,
    GEO_TAXONOMY,
    GEO_UNIGENE,
    HOMOLOGENE_CDD,
    HOMOLOGENE_GENE,
    HOMOLOGENE_GEO,
    HOMOLOGENE_HOMOLOGENE,
    HOMOLOGENE_NUCCORE,
    HOMOLOGENE_NUCEST,
    HOMOLOGENE_NUCGSS,
    HOMOLOGENE_NUCLEOTIDE,
    HOMOLOGENE_OMIA,
    HOMOLOGENE_OMIM,
    HOMOLOGENE_PMC,
    HOMOLOGENE_PROTEIN,
    HOMOLOGENE_PUBMED,
    HOMOLOGENE_SNP,
    HOMOLOGENE_SNP_GENEGENOTYPE,
    HOMOLOGENE_TAXONOMY,
    HOMOLOGENE_UNIGENE,
    JOURNALS_GENOME,
    JOURNALS_NUCCORE,
    JOURNALS_NUCEST,
    JOURNALS_NUCGSS,
    JOURNALS_PMC,
    JOURNALS_PMC_ARCHIVE,
    JOURNALS_POPSET,
    JOURNALS_PROTEIN,
    JOURNALS_PUBMED,
    MESH_PCCOMPOUND_EXPANDED,
    MESH_PCSUBSTANCE_EXPANDED,
    MESH_TAXONOMY,
    NCBISEARCH_NCBISEARCH,
    NUCCORE_ASSEMBLY,
    NUCCORE_COMP_NUCCORE,
    NUCCORE_GENE,
    NUCCORE_GENOME,
    NUCCORE_GENOME_COMP,
    NUCCORE_GENOME_MRNA,
    NUCCORE_GENOME_SAMESPECIES,
    NUCCORE_GENOMEPRJ,
    NUCCORE_GENOMEPRJ_INSDC,
    NUCCORE_GENOMEPRJ_INSDC_WGS,
    NUCCORE_GENOMEPRJ_ORGANELLE_SCAFFOLD,
    NUCCORE_GENOMEPRJ_SCAFFOLD,
    NUCCORE_GENSAT,
    NUCCORE_GEO,
    NUCCORE_HOMOLOGENE,
    NUCCORE_MAPVIEW,
    NUCCORE_MRNA_COMP_GENOME,
    NUCCORE_MRNA_GENOMEPRJ,
    NUCCORE_MRNA_NUCCORE,
    NUCCORE_NUCCORE,
    NUCCORE_NUCCORE_COMP,
    NUCCORE_NUCCORE_MGC_REFSEQ,
    NUCCORE_NUCCORE_MRNA,
    NUCCORE_OMIM,
    NUCCORE_ORGANELLA_GENOMEPRJ,
    NUCCORE_PCASSAY,
    NUCCORE_PCASSAY_DNA_TARGET,
    NUCCORE_PCASSAY_RNA_TARGET,
    NUCCORE_PCCOMPOUND,
    NUCCORE_PCSUBSTANCE,
    NUCCORE_PMC,
    NUCCORE_POPSET,
    NUCCORE_PROBE,
    NUCCORE_PROTEIN,
    NUCCORE_PROTEIN_MGC_URL,
    NUCCORE_PROTEIN_WGS,
    NUCCORE_PROTEINCLUSTERS,
    NUCCORE_PUBMED,
    NUCCORE_PUBMED_REFSEQ,
    NUCCORE_SNP,
    NUCCORE_SNP_GENEGENOTYPE,
    NUCCORE_SNP_GENEVIEW,
    NUCCORE_STRUCTURE,
    NUCCORE_TAXONOMY,
    NUCCORE_TRACE,
    NUCCORE_UNIGENE,
    NUCCORE_UNISTS,
    NUCCORE_WGS_GENOMEPRJ,
    NUCEST_ASSEMBLY,
    NUCEST_GENE,
    NUCEST_GENOMEPRJ_EST,
    NUCEST_GENOMEPRJ_INSDC,
    NUCEST_GENOMEPRJ_INSDC_WGS,
    NUCEST_GENOMEPRJ_ORGANELLE_SCAFFOLD,
    NUCEST_GENOMEPRJ_SCAFFOLD,
    NUCEST_GENSAT,
    NUCEST_GEO,
    NUCEST_HOMOLOGENE,
    NUCEST_MAPVIEW,
    NUCEST_MRNA_COMP_GENOME,
    NUCEST_MRNA_GENOMEPRJ,
    NUCEST_OMIM,
    NUCEST_ORGANELLA_GENOMEPRJ,
    NUCEST_PCASSAY,
    NUCEST_PCASSAY_DNA_TARGET,
    NUCEST_PCASSAY_RNA_TARGET,
    NUCEST_PCCOMPOUND,
    NUCEST_PCSUBSTANCE,
    NUCEST_PMC,
    NUCEST_POPSET,
    NUCEST_PROBE,
    NUCEST_PROTEIN_MGC_URL,
    NUCEST_PROTEINCLUSTERS,
    NUCEST_PUBMED,
    NUCEST_PUBMED_REFSEQ,
    NUCEST_SNP,
    NUCEST_SNP_GENEGENOTYPE,
    NUCEST_SNP_GENEVIEW,
    NUCEST_STRUCTURE,
    NUCEST_TAXONOMY,
    NUCEST_TRACE,
    NUCEST_UNIGENE,
    NUCEST_UNISTS,
    NUCEST_WGS_GENOMEPRJ,
    NUCGSS_ASSEMBLY,
    NUCGSS_GENE,
    NUCGSS_GENOMEPRJ,
    NUCGSS_GENOMEPRJ_INSDC,
    NUCGSS_GENOMEPRJ_INSDC_WGS,
    NUCGSS_GENOMEPRJ_ORGANELLE_SCAFFOLD,
    NUCGSS_GENOMEPRJ_SCAFFOLD,
    NUCGSS_GENSAT,
    NUCGSS_GEO,
    NUCGSS_HOMOLOGENE,
    NUCGSS_MAPVIEW,
    NUCGSS_MRNA_COMP_GENOME,
    NUCGSS_MRNA_GENOMEPRJ,
    NUCGSS_OMIM,
    NUCGSS_ORGANELLA_GENOMEPRJ,
    NUCGSS_PCASSAY,
    NUCGSS_PCASSAY_DNA_TARGET,
    NUCGSS_PCASSAY_RNA_TARGET,
    NUCGSS_PCCOMPOUND,
    NUCGSS_PCSUBSTANCE,
    NUCGSS_PMC,
    NUCGSS_POPSET,
    NUCGSS_PROBE,
    NUCGSS_PROTEIN,
    NUCGSS_PROTEIN_MGC_URL,
    NUCGSS_PROTEINCLUSTERS,
    NUCGSS_PUBMED,
    NUCGSS_PUBMED_REFSEQ,
    NUCGSS_SNP,
    NUCGSS_SNP_GENEGENOTYPE,
    NUCGSS_SNP_GENEVIEW,
    NUCGSS_STRUCTURE,
    NUCGSS_TAXONOMY,
    NUCGSS_TRACE,
    NUCGSS_UNIGENE,
    NUCGSS_UNISTS,
    NUCGSS_WGS_GENOMEPRJ,
    OMIA_GENE,
    OMIA_HOMOLOGENE,
    OMIA_OMIM,
    OMIA_PROTEIN,
    OMIA_PUBMED,
    OMIA_TAXONOMY,
    OMIA_UNIGENE,
    OMIA_UNISTS,
    OMIM_BOOKS,
    OMIM_GENE,
    OMIM_GENOME,
    OMIM_GEO,
    OMIM_HOMOLOGENE,
    OMIM_MAPVIEW,
    OMIM_NUCCORE,
    OMIM_NUCEST,
    OMIM_NUCGSS,
    OMIM_NUCLEOTIDE,
    OMIM_OMIA,
    OMIM_OMIM,
    OMIM_PCASSAY,
    OMIM_PCCOMPOUND,
    OMIM_PCSUBSTANCE,
    OMIM_PMC,
    OMIM_PROTEIN,
    OMIM_PUBMED_CALCULATED,
    OMIM_PUBMED_CITED,
    OMIM_SNP,
    OMIM_SNP_GENEGENOTYPE,
    OMIM_SNP_GENEVIEW,
    OMIM_STRUCTURE,
    OMIM_UNIGENE,
    OMIM_UNISTS,
    PCASSAY_GENE,
    PCASSAY_NUCCORE,
    PCASSAY_NUCCORE_DNA_TARGET,
    PCASSAY_NUCCORE_RNA_TARGET,
    PCASSAY_NUCEST,
    PCASSAY_NUCEST_DNA_TARGET,
    PCASSAY_NUCEST_RNA_TARGET,
    PCASSAY_NUCGSS,
    PCASSAY_NUCGSS_DNA_TARGET,
    PCASSAY_NUCGSS_RNA_TARGET,
    PCASSAY_NUCLEOTIDE,
    PCASSAY_NUCLEOTIDE_DNA_TARGET,
    PCASSAY_NUCLEOTIDE_RNA_TARGET,
    PCASSAY_OMIM,
    PCASSAY_PCASSAY_ACTIVITYNEIGHBOR,
    PCASSAY_PCASSAY_ACTIVITYNEIGHBOR_FIVE,
    PCASSAY_PCASSAY_NEIGHBOR,
    PCASSAY_PCASSAY_NEIGHBOR_FIVE,
    PCASSAY_PCASSAY_TARGETNEIGHBOR,
    PCASSAY_PCASSAY_TARGETNEIGHBOR_FIVE,
    PCASSAY_PCCOMPOUND,
    PCASSAY_PCCOMPOUND_ACTIVE,
    PCASSAY_PCCOMPOUND_FIVE,
    PCASSAY_PCCOMPOUND_INACTIVE,
    PCASSAY_PCCOMPOUND_INCONCLUSIVE,
    PCASSAY_PCSUBSTANCE,
    PCASSAY_PCSUBSTANCE_ACTIVE,
    PCASSAY_PCSUBSTANCE_FIVE,
    PCASSAY_PCSUBSTANCE_INACTIVE,
    PCASSAY_PCSUBSTANCE_INCONCLUSIVE,
    PCASSAY_PMC,
    PCASSAY_PROTEIN,
    PCASSAY_PROTEIN_TARGET,
    PCASSAY_PUBMED,
    PCASSAY_STRUCTURE,
    PCASSAY_TAXONOMY,
    PCCOMPOUND_GENE,
    PCCOMPOUND_MESH,
    PCCOMPOUND_NUCCORE,
    PCCOMPOUND_NUCEST,
    PCCOMPOUND_NUCGSS,
    PCCOMPOUND_NUCLEOTIDE,
    PCCOMPOUND_OMIM,
    PCCOMPOUND_PCASSAY,
    PCCOMPOUND_PCASSAY_ACTIVE,
    PCCOMPOUND_PCASSAY_INACTIVE,
    PCCOMPOUND_PCASSAY_INCONCLUSIVE,
    PCCOMPOUND_PCCOMPOUND,
    PCCOMPOUND_PCCOMPOUND_MIXTURE,
    PCCOMPOUND_PCCOMPOUND_PARENT_CONNECTIVITY_POPUP,
    PCCOMPOUND_PCCOMPOUND_PARENT_CONNECTIVITY_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_PARENT_ISOTOPES_POPUP,
    PCCOMPOUND_PCCOMPOUND_PARENT_ISOTOPES_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_PARENT_POPUP,
    PCCOMPOUND_PCCOMPOUND_PARENT_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_PARENT_STEREO_POPUP,
    PCCOMPOUND_PCCOMPOUND_PARENT_STEREO_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_PARENT_TAUTOMER_POPUP,
    PCCOMPOUND_PCCOMPOUND_PARENT_TAUTOMER_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_SAMEANYTAUTOMER_POPUP,
    PCCOMPOUND_PCCOMPOUND_SAMEANYTAUTOMER_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_SAMECONNECTIVITY_POPUP,
    PCCOMPOUND_PCCOMPOUND_SAMECONNECTIVITY_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_SAMEISOTOPIC_POPUP,
    PCCOMPOUND_PCCOMPOUND_SAMEISOTOPIC_PULLDOWN,
    PCCOMPOUND_PCCOMPOUND_SAMESTEREOCHEM_POPUP,
    PCCOMPOUND_PCCOMPOUND_SAMESTEREOCHEM_PULLDOWN,
    PCCOMPOUND_PCSUBSTANCE,
    PCCOMPOUND_PCSUBSTANCE_SAME,
    PCCOMPOUND_PMC,
    PCCOMPOUND_PROBE,
    PCCOMPOUND_PROTEIN,
    PCCOMPOUND_PUBMED,
    PCCOMPOUND_PUBMED_MESH,
    PCCOMPOUND_PUBMED_PUBLISHER,
    PCCOMPOUND_STRUCTURE,
    PCCOMPOUND_TAXONOMY,
    PCSUBSTANCE_BOOKS,
    PCSUBSTANCE_GENE,
    PCSUBSTANCE_MESH,
    PCSUBSTANCE_NUCCORE,
    PCSUBSTANCE_NUCEST,
    PCSUBSTANCE_NUCGSS,
    PCSUBSTANCE_NUCLEOTIDE,
    PCSUBSTANCE_OMIM,
    PCSUBSTANCE_PCASSAY,
    PCSUBSTANCE_PCASSAY_ACTIVE,
    PCSUBSTANCE_PCASSAY_INACTIVE,
    PCSUBSTANCE_PCASSAY_INCONCLUSIVE,
    PCSUBSTANCE_PCCOMPOUND,
    PCSUBSTANCE_PCCOMPOUND_SAME,
    PCSUBSTANCE_PCSUBSTANCE,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_CONNECTIVITY_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_CONNECTIVITY_PULLDO,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_ISOTOPES_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_ISOTOPES_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_STEREO_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_STEREO_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_TAUTOMER_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_PARENT_TAUTOMER_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_SAME_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_SAME_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_SAMEANYTAUTOMER_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_SAMEANYTAUTOMER_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_SAMECONNECTIVITY_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_SAMECONNECTIVITY_PULLDOW,
    PCSUBSTANCE_PCSUBSTANCE_SAMEISOTOPIC_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_SAMEISOTOPIC_PULLDOWN,
    PCSUBSTANCE_PCSUBSTANCE_SAMESTEREOCHEM_POPUP,
    PCSUBSTANCE_PCSUBSTANCE_SAMESTEREOCHEM_PULLDOWN,
    PCSUBSTANCE_PMC,
    PCSUBSTANCE_PROBE,
    PCSUBSTANCE_PROTEIN,
    PCSUBSTANCE_PUBMED,
    PCSUBSTANCE_PUBMED_MESH,
    PCSUBSTANCE_PUBMED_PUBLISHER,
    PCSUBSTANCE_STRUCTURE,
    PCSUBSTANCE_TAXONOMY,
    PMC_BOOKS_REFS,
    PMC_CANCERCHROMOSOMES,
    PMC_CDD,
    PMC_DOMAINS,
    PMC_GDS,
    PMC_GENE,
    PMC_GENOME,
    PMC_GENOMEPRJ,
    PMC_GENSAT,
    PMC_GEO,
    PMC_HOMOLOGENE,
    PMC_NUCCORE,
    PMC_NUCEST,
    PMC_NUCGSS,
    PMC_NUCLEOTIDE,
    PMC_OMIM,
    PMC_PCASSAY,
    PMC_PCCOMPOUND,
    PMC_PCSUBSTANCE,
    PMC_PMC_REFS,
    PMC_POPSET,
    PMC_PROTEIN,
    PMC_PUBMED,
    PMC_REFS_PUBMED,
    PMC_SNP,
    PMC_STRUCTURE,
    PMC_TAXONOMY,
    PMC_UNISTS,
    POPSET_GENOMEPRJ,
    POPSET_NUCCORE,
    POPSET_PMC,
    POPSET_PROTEIN,
    POPSET_PUBMED,
    POPSET_TAXONOMY,
    PROBE_GENE,
    PROBE_NUCCORE,
    PROBE_NUCEST,
    PROBE_NUCGSS,
    PROBE_NUCLEOTIDE,
    PROBE_PCCOMPOUND,
    PROBE_PCSUBSTANCE,
    PROBE_PROBE,
    PROBE_PUBMED,
    PROBE_SNP,
    PROBE_TAXONOMY,
    PROTEIN_CDD,
    PROTEIN_CDD_SUMMARY,
    PROTEIN_DOMAINS,
    PROTEIN_GENE,
    PROTEIN_GENOME,
    PROTEIN_GENOMEPRJ,
    PROTEIN_GENOMEPRJ_INSDC,
    PROTEIN_HOMOLOGENE,
    PROTEIN_MAPVIEW,
    PROTEIN_NUCCORE,
    PROTEIN_NUCCORE_MGC,
    PROTEIN_NUCCORE_WGS,
    PROTEIN_NUCEST_MGC,
    PROTEIN_NUCGSS,
    PROTEIN_NUCGSS_MGC,
    PROTEIN_NUCLEOTIDE_COMP_GENOME,
    PROTEIN_NUCLEOTIDE_MGC,
    PROTEIN_NUCLEOTIDE_MGC_URL,
    PROTEIN_NUCLEOTIDE_WGS,
    PROTEIN_OMIA,
    PROTEIN_OMIM,
    PROTEIN_PCASSAY,
    PROTEIN_PCASSAY_TARGET,
    PROTEIN_PCCOMPOUND,
    PROTEIN_PCSUBSTANCE,
    PROTEIN_PMC,
    PROTEIN_POPSET,
    PROTEIN_PROTEIN,
    PROTEIN_PROTEIN_CDART_SUMMARY,
    PROTEIN_PROTEIN_REFSEQ2UNIPROT,
    PROTEIN_PROTEIN_UNIPROT2REFSEQ,
    PROTEIN_PROTEINCLUSTERS,
    PROTEIN_PUBMED,
    PROTEIN_PUBMED_REFSEQ,
    PROTEIN_SNP,
    PROTEIN_SNP_GENEGENOTYPE,
    PROTEIN_SNP_GENEVIEW,
    PROTEIN_STRUCTURE,
    PROTEIN_STRUCTURE_RELATED,
    PROTEIN_TAXONOMY,
    PROTEIN_UNIGENE,
    PROTEINCLUSTERS_GENE,
    PROTEINCLUSTERS_GENOME,
    PROTEINCLUSTERS_NUCCORE,
    PROTEINCLUSTERS_NUCEST,
    PROTEINCLUSTERS_NUCGSS,
    PROTEINCLUSTERS_NUCLEOTIDE,
    PROTEINCLUSTERS_PROTEIN,
    PROTEINCLUSTERS_PUBMED_CDD,
    PROTEINCLUSTERS_PUBMED_CURATED,
    PROTEINCLUSTERS_PUBMED_GENERIF,
    PROTEINCLUSTERS_PUBMED_HOMOLOGY,
    PROTEINCLUSTERS_PUBMED_REFSEQ,
    PROTEINCLUSTERS_PUBMED_STRUCTURE,
    PROTEINCLUSTERS_PUBMED_SWISSPROT,
    PUBMED_BOOKS_REFS,
    PUBMED_CANCERCHROMOSOMES,
    PUBMED_CDD,
    PUBMED_DOMAINS,
    PUBMED_GDS,
    PUBMED_GENE,
    PUBMED_GENE_RIF,
    PUBMED_GENOME,
    PUBMED_GENOMEPRJ,
    PUBMED_GENSAT,
    PUBMED_GEO,
    PUBMED_HOMOLOGENE,
    PUBMED_NUCCORE,
    PUBMED_NUCCORE_REFSEQ,
    PUBMED_NUCEST,
    PUBMED_NUCEST_REFSEQ,
    PUBMED_NUCGSS,
    PUBMED_NUCGSS_REFSEQ,
    PUBMED_NUCLEOTIDE,
    PUBMED_NUCLEOTIDE_REFSEQ,
    PUBMED_OMIA,
    PUBMED_OMIM_CALCULATED,
    PUBMED_OMIM_CITED,
    PUBMED_PCASSAY,
    PUBMED_PCCOMPOUND,
    PUBMED_PCCOMPOUND_MESH,
    PUBMED_PCCOMPOUND_PUBLISHER,
    PUBMED_PCSUBSTANCE,
    PUBMED_PCSUBSTANCE_MESH,
    PUBMED_PCSUBSTANCE_PUBLISHER,
    PUBMED_PMC,
    PUBMED_PMC_LOCAL,
    PUBMED_PMC_REFS,
    PUBMED_POPSET,
    PUBMED_PROBE,
    PUBMED_PROTEIN,
    PUBMED_PROTEIN_REFSEQ,
    PUBMED_PROTEINCLUSTERS,
    PUBMED_PUBMED,
    PUBMED_PUBMED_REFS,
    PUBMED_SNP,
    PUBMED_STRUCTURE,
    PUBMED_TAXONOMY_ENTREZ,
    PUBMED_UNIGENE,
    PUBMED_UNISTS,
    SNP_GENE,
    SNP_HAPVARSET,
    SNP_HOMOLOGENE,
    SNP_NUCCORE,
    SNP_NUCEST,
    SNP_NUCGSS,
    SNP_NUCLEOTIDE,
    SNP_OMIM,
    SNP_PMC,
    SNP_PROBE,
    SNP_PROTEIN,
    SNP_PUBMED,
    SNP_SNP_GENEGENOTYPE,
    SNP_STRUCTURE,
    SNP_TAXONOMY,
    SNP_TRACE,
    SNP_UNIGENE,
    SNP_UNISTS,
    STRUCTURE_CDD,
    STRUCTURE_DOMAINS,
    STRUCTURE_GENOME,
    STRUCTURE_MMDB,
    STRUCTURE_NUCCORE,
    STRUCTURE_NUCEST,
    STRUCTURE_NUCGSS,
    STRUCTURE_NUCLEOTIDE,
    STRUCTURE_OMIM,
    STRUCTURE_PCASSAY,
    STRUCTURE_PCCOMPOUND,
    STRUCTURE_PCSUBSTANCE,
    STRUCTURE_PMC,
    STRUCTURE_PROTEIN,
    STRUCTURE_PUBMED,
    STRUCTURE_SNP,
    STRUCTURE_TAXONOMY,
    TAXONOMY_CDD,
    TAXONOMY_DOMAINS,
    TAXONOMY_GDS,
    TAXONOMY_GENE_EXP,
    TAXONOMY_GENOME_EXP,
    TAXONOMY_GENOMEPRJ,
    TAXONOMY_GENSAT,
    TAXONOMY_GEO_EXP,
    TAXONOMY_HOMOLOGENE,
    TAXONOMY_MESH,
    TAXONOMY_NUCCORE,
    TAXONOMY_NUCEST,
    TAXONOMY_NUCGSS,
    TAXONOMY_NUCLEOTIDE_EXP,
    TAXONOMY_OMIA,
    TAXONOMY_PCASSAY,
    TAXONOMY_PCCOMPOUND,
    TAXONOMY_PCSUBSTANCE,
    TAXONOMY_PMC,
    TAXONOMY_POPSET,
    TAXONOMY_PROBE,
    TAXONOMY_PROTEIN_EXP,
    TAXONOMY_PUBMED,
    TAXONOMY_PUBMED_ENTREZ,
    TAXONOMY_SNP_EXP,
    TAXONOMY_STRUCTURE_EXP,
    TAXONOMY_UNIGENE,
    TAXONOMY_UNISTS,
    UNIGENE_GENE,
    UNIGENE_GENSAT,
    UNIGENE_GEO,
    UNIGENE_HOMOLOGENE,
    UNIGENE_NUCCORE,
    UNIGENE_NUCCORE_MGC,
    UNIGENE_NUCEST,
    UNIGENE_NUCEST_MGC,
    UNIGENE_NUCGSS,
    UNIGENE_NUCGSS_MGC,
    UNIGENE_NUCLEOTIDE,
    UNIGENE_NUCLEOTIDE_MGC,
    UNIGENE_NUCLEOTIDE_MGC_URL,
    UNIGENE_OMIA,
    UNIGENE_OMIM,
    UNIGENE_PROTEIN,
    UNIGENE_PUBMED,
    UNIGENE_SNP,
    UNIGENE_SNP_GENEGENOTYPE,
    UNIGENE_SNP_GENEVIEW,
    UNIGENE_TAXONOMY,
    UNIGENE_UNIGENE_EXPRESSION,
    UNIGENE_UNIGENE_HOMOLOGOUS,
    UNIGENE_UNISTS,
    UNISTS_GENE,
    UNISTS_NUCCORE,
    UNISTS_NUCEST,
    UNISTS_NUCGSS,
    UNISTS_NUCLEOTIDE,
    UNISTS_OMIA,
    UNISTS_OMIM,
    UNISTS_PMC,
    UNISTS_PUBMED,
    UNISTS_SNP,
    UNISTS_TAXONOMY,
    UNISTS_UNIGENE,
    )


# constants for field descriptor arguments; used in dictionary lookups
AFFILIATION = 'AFFILIATION' 
ARTICLE_IDENTIFIER = 'ARTICLE_IDENTIFIER' 
ACCESSION = 'ACCESSION' 
ALL_FIELDS = 'ALL_FIELDS' 
AUTHOR = 'AUTHOR' 
CORPORATE_AUTHOR = 'CORPORATE_AUTHOR' 
EC_RN_NUMBER = 'EC/RN_NUMBER' 
ENTREZ_DATE = 'ENTREZ_DATE' 
FEATURE_KEY = 'FEATURE_KEY' 
FILTER = 'FILTER' 
FIRST_AUTHOR_NAME = 'FIRST_AUTHOR_NAME' 
FULL_AUTHOR_NAME = 'FULL_AUTHOR_NAME' 
FULL_INVESTIGATOR_NAME = 'FULL_INVESTIGATOR_NAME' 
GENE_NAME = 'GENE_NAME' 
GRANT_NUMBER = 'GRANT_NUMBER' 
INVESTIGATOR = 'INVESTIGATOR' 
ISSUE = 'ISSUE' 
JOURNAL_NAME = 'JOURNAL_NAME' 
JOURNAL_TITLE = 'JOURNAL_TITLE' 
KEYWORD = 'KEYWORD' 
LANGUAGE = 'LANGUAGE' 
LAST_AUTHOR = 'LAST_AUTHOR' 
LOCATION_ID = 'LOCATION_ID' 
MESH_DATE = 'MESH_DATE' 
MESH_MAJOR_TOPIC = 'MESH_MAJOR_TOPIC' 
MESH_SUBHEADINGS = 'MESH_SUBHEADINGS' 
MESH_TERMS = 'MESH_TERMS' 
MODIFICATION_DATE = 'MODIFICATION_DATE' 
MOLECULAR_WEIGHT = 'MOLECULAR_WEIGHT' 
NLM_UNIQUE_ID = 'NLM_UNIQUE_ID' 
ORGANISM = 'ORGANISM' 
OTHER_TERM = 'OTHER_TERM' 
OWNER = 'OWNER' 
PAGE_NUMBER = 'PAGE_NUMBER' 
PAGINATION = 'PAGINATION' 
PERSONAL_NAME_AS_SUBJECT = 'PERSONAL_NAME_AS_SUBJECT' 
PHARMACOLOGICAL_ACTION_MESH_TERMS = 'PHARMACOLOGICAL_ACTION_MESH_TERMS' 
PLACE_OF_PUBLICATION = 'PLACE_OF_PUBLICATION' 
PRIMARY_ACCESSION = 'PRIMARY_ACCESSION' 
PROPERTIES = 'PROPERTIES' 
PROTEIN_NAME = 'PROTEIN_NAME' 
PUBLICATION_DATE = 'PUBLICATION_DATE' 
PUBLICATION_TYPE = 'PUBLICATION_TYPE' 
SEQID_STRING = 'SEQID_STRING' 
SEQUENCE_LENGTH = 'SEQUENCE_LENGTH' 
SECONDARY_SOURCE_ID = 'SECONDARY_SOURCE_ID' 
SUBSET = 'SUBSET' 
SUBSTANCE_NAME = 'SUBSTANCE_NAME' 
TEXT_WORD = 'TEXT_WORD' 
TEXT_WORDS = 'TEXT_WORDS' 
TITLE = 'TITLE' 
TITLE_WORD = 'TITLE_WORD' 
TITLE_ABSTRACT = 'TITLE/ABSTRACT' 
TRANSLITERATED_TITLE = 'TRANSLITERATED_TITLE' 
UID = 'UID' 
VOLUME = 'VOLUME' 


# search field tags
tagsdict = {
    AFFILIATION : '[AD]',
    ARTICLE_IDENTIFIER : '[AID]',
    ACCESSION : '[ACCN]',
    ALL_FIELDS : '[ALL]',
    AUTHOR : '[AUTH]',
    CORPORATE_AUTHOR : '[CN]',
    EC_RN_NUMBER : '[RN]',
    ENTREZ_DATE : '[EDAT]',
    FEATURE_KEY : '[FKEY]',
    FILTER : '[FILT]',
    FIRST_AUTHOR_NAME : '[1AU]',
    FULL_AUTHOR_NAME : '[FAU]',
    FULL_INVESTIGATOR_NAME : '[FIR]',
    GENE_NAME : '[GENE]',
    GRANT_NUMBER : '[GR]',
    INVESTIGATOR : '[IR]',
    ISSUE : '[ISS]',
    JOURNAL_NAME : '[JOUR]',
    JOURNAL_TITLE : '[TA]',
    KEYWORD : '[KYWD]',
    LANGUAGE : '[LA]',
    LAST_AUTHOR : '[LASTAU]',
    LOCATION_ID : '[LID]',
    MESH_DATE : '[MHDA]',
    MESH_MAJOR_TOPIC : '[MAJR]',
    MESH_SUBHEADINGS : '[SH]',
    MESH_TERMS : '[MH]',
    MODIFICATION_DATE : '[MDAT]',
    MOLECULAR_WEIGHT : '[MOLWT]',
    NLM_UNIQUE_ID : '[JID]',
    ORGANISM : '[ORGN]',
    OTHER_TERM : '[OT]',
    OWNER : '[OWNER]',
    PAGE_NUMBER : '[PAGE]',
    PAGINATION : '[PG]',
    PERSONAL_NAME_AS_SUBJECT : '[PS]',
    PHARMACOLOGICAL_ACTION_MESH_TERMS : '[PA]',
    PLACE_OF_PUBLICATION : '[PL]',
    PRIMARY_ACCESSION : '[PACC]',
    PROPERTIES : '[PROP]',
    PROTEIN_NAME : '[PROT]',
    PUBLICATION_DATE : '[PDAT]',
    PUBLICATION_TYPE : '[PT]',
    SEQID_STRING : '[SQID]',
    SEQUENCE_LENGTH : '[SLEN]',
    SECONDARY_SOURCE_ID : '[SI]',
    SUBSET : '[SB]',
    SUBSTANCE_NAME : '[NM]',
    TEXT_WORD : '[WORD]',
    TEXT_WORDS : '[TW]',
    TITLE : '[TI]',
    TITLE_WORD : '[TITL]',
    TITLE_ABSTRACT : '[TIAB]',
    TRANSLITERATED_TITLE : '[TT]',
    UID : '[PMID]',
    VOLUME : '[VI]',
}        

def ConcatDBNames(dblist):
    str = ''
    first = True
    for db in dblist:
        if not first:
            str = str + ','
        else:
            first = False
        str = str + db
    return str
