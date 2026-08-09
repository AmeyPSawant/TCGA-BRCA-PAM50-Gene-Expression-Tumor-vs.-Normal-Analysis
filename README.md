# TCGA-BRCA-PAM50-Gene-Expression-Tumor-vs.-Normal-Analysis

A reproducible Python pipeline analyzing differential gene expression of the PAM50 breast cancer gene panel in TCGA breast cancer (BRCA) RNA-seq data, comparing primary tumor vs. solid tissue normal samples.

## Overview

This project asks: **which genes in the PAM50 breast cancer panel show the strongest and most statistically significant difference in expression between tumor and normal breast tissue?**

For each of the 50 PAM50 genes, the pipeline computes:
- Mean expression in tumor vs. normal samples
- Effect size (difference in mean expression)
- Statistical significance via Welch's two-sample t-test

Results are exported to CSV and visualized in an interactive Tableau dashboard (linked below).

## Data Source
Cohort: GDC TCGA Breast Cancer (BRCA), accessed via UCSC Xena
Expression data: STAR - FPKM (GDC Hub), n = 1,226 samples
Sample metadata: GDC TCGA Breast Cancer (BRCA) phenotype/clinical matrix, used to classify samples as Primary Tumor vs. Solid Tissue Normal
Gene panel: PAM50, the 50-gene breast cancer intrinsic subtyping panel (Parker et al., 2009, J Clin Oncol)