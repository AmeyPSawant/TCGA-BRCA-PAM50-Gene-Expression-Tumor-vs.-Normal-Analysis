# TCGA-BRCA-PAM50-Gene-Expression-Tumor-vs.-Normal-Analysis

A reproducible Python pipeline analyzing differential gene expression of the PAM50 breast cancer gene panel in TCGA breast cancer (BRCA) RNA-seq data, comparing primary tumor vs. solid tissue normal samples.

# TCGA-BRCA PAM50 Differential Expression Analysis

### The Problem

Cancer research generates enormous public genomic datasets, but raw expression data alone doesn't answer the question that actually matters to researchers and clinicians: **which genes are biologically meaningful drivers of disease, and which are just noise?**

The PAM50 panel is a clinically established set of 50 genes used to classify breast cancer intrinsic subtypes (Parker et al., 2009). But a gene's inclusion in a curated clinical panel doesn't, by itself, tell you how strongly — or how reliably — it differs between diseased and healthy tissue. In large cohorts like TCGA, where sample sizes are big enough that nearly any difference can register as "statistically significant," it becomes easy to either overstate a weak signal or overlook the genes that actually carry the strongest evidence. Distinguishing genuine biological signal from an artifact of sample size is a basic but essential step before any of this data is useful for further research, subtype classification, or hypothesis generation.

### What This Project Solves

This project takes public TCGA breast cancer RNA-seq data and answers a concrete question: **across the PAM50 gene panel, which genes show a real, defensible difference in expression between tumor and normal tissue — and which don't?**

The analysis deliberately separates two things that are often conflated: **effect size** (how large the expression difference actually is) and **statistical significance** (how confident we can be that the difference isn't due to chance). Genes are evaluated on both axes, and — importantly — genes that fail to show a meaningful difference (e.g., PTEN, PIK3CA in this cohort) are reported alongside the strong hits rather than filtered out, since knowing what *doesn't* differ is as informative as knowing what does.

### How It Was Built

**Data source:**
- Expression data: GDC TCGA Breast Cancer (BRCA), STAR-FPKM pipeline, n = 1,226 samples, accessed via [UCSC Xena](https://xenabrowser.net)
- Sample metadata: GDC TCGA Breast Cancer (BRCA) phenotype/clinical matrix, n = 1,255, used to classify samples as Primary Tumor vs. Solid Tissue Normal
- Gene ID mapping: Gencode probeMap (Ensembl gene ID → gene symbol)
- Gene panel: PAM50 (Parker et al., 2009, *Journal of Clinical Oncology*)

**Method:**
1. Load the full TCGA-BRCA expression matrix (indexed by Ensembl gene ID) and phenotype/clinical metadata
2. Map Ensembl gene IDs to gene symbols via the Gencode probeMap
3. Filter the expression matrix to the 50 PAM50 genes
4. Split samples into Primary Tumor and Solid Tissue Normal groups
5. For each gene, compute mean expression per group, the difference in means (effect size), and a Welch's two-sample t-test p-value (does not assume equal variance between groups — appropriate here given the large imbalance in group sizes)
6. Export a per-gene summary table and a long-format table of individual sample-level values

The entire workflow is scripted in Python (pandas, scipy) and version-controlled, making the analysis reproducible and auditable rather than a one-off spreadsheet exercise — it can be re-run against updated data or a different gene panel with minimal changes.

**Dashboard:** results are visualized in an interactive Tableau dashboard — a ranked effect-size comparison, a volcano plot combining effect size and significance, and per-gene expression distributions — designed to let a viewer draw their own conclusions from the underlying data rather than accept a single summary number at face value.

**Dashboard link:** [Click Here for Dashboard](https://public.tableau.com/app/profile/ameypsawant/viz/PAM50GenePanelDifferentialExpressioninTCGABreastCancer/Dashboard)

### Limitations

- Sample sizes are imbalanced (far more tumor samples than matched normal samples), a known characteristic of TCGA, which increases statistical power to detect even small differences as "significant" — effect size should be read alongside p-value, not in isolation
- This is a descriptive/exploratory statistical analysis (per-gene t-tests), not a batch-corrected differential expression pipeline (e.g. DESeq2, edgeR); it does not apply multiple-testing correction, sample pairing, or clinical covariate adjustment
- FPKM values are used as provided by the GDC bioinformatics pipeline; no additional normalization was applied

### Author

Amey Sawant

### References

Parker, J.S., Mullins, M., Cheang, M.C., et al. (2009). Supervised risk predictor of breast cancer based on intrinsic subtypes. *Journal of Clinical Oncology*, 27(8), 1160-1167.

The Cancer Genome Atlas Research Network. Comprehensive molecular portraits of human breast tumours. *Nature* 490, 61–70 (2012).

Goldman, M.J., Craft, B., Hastie, M. et al. Visualizing and interpreting cancer genomics data via the Xena platform. *Nature Biotechnology* 38, 675–678 (2020).