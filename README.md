# TCGA-BRCA-PAM50-Gene-Expression-Tumor-vs.-Normal-Analysis

An end-to-end bioinformatics and data analysis project using TCGA-BRCA RNA-seq data to evaluate differential expression across the 50-gene PAM50 breast cancer panel.

## 📊 Interactive Dashboard

**[View the Tableau Dashboard →](https://public.tableau.com/app/profile/ameypsawant/viz/PAM50GenePanelDifferentialExpressioninTCGABreastCancer/Dashboard)**

The interactive dashboard lets you explore:

* **Ranked effect-size comparison** across all 50 PAM50 genes
* **Volcano plot** showing effect size vs. statistical significance
* **Per-gene expression distributions** comparing tumor and normal tissue
* Individual gene-level results and underlying statistical measures

> **Key finding:** MMP11 showed the largest tumor-vs-normal expression difference in this cohort, followed by UBE2C, MYBL2, CDC20, and BIRC5.

---

## 🔬 Project Overview

This project analyzes publicly available TCGA breast cancer RNA-seq data to answer a focused question:

**Across the PAM50 gene panel, which genes show the strongest and most statistically supported differences in expression between primary tumor and solid tissue normal samples?**

The analysis separates two concepts that are often conflated:

* **Effect size:** How large is the observed expression difference?
* **Statistical significance:** How strong is the evidence that the observed difference is unlikely to be due to chance?

Both are reported for every PAM50 gene. Genes that do not show a strong difference are retained rather than filtered out, providing a complete view of the panel.

## 🧬 The Problem

Cancer research generates enormous public genomic datasets, but raw expression data alone does not answer the question that actually matters: **which genes show meaningful biological differences, and which may simply reflect statistical noise?**

The PAM50 panel is a clinically established set of 50 genes used to classify breast cancer intrinsic subtypes (Parker et al., 2009). However, inclusion in a curated clinical panel does not indicate how strongly a gene differs between tumor and normal tissue.

In large cohorts such as TCGA, sample sizes can make relatively small differences statistically significant. This makes it important to evaluate **effect size alongside statistical significance** rather than relying on p-values alone.

## 🛠️ How It Was Built

### Data

* **Expression data:** GDC TCGA Breast Cancer (BRCA), STAR-FPKM pipeline, n = 1,226 samples, accessed via [UCSC Xena](https://xenabrowser.net)
* **Sample metadata:** GDC TCGA Breast Cancer (BRCA) phenotype/clinical matrix, n = 1,255
* **Gene ID mapping:** Gencode probeMap, mapping Ensembl gene IDs to gene symbols
* **Gene panel:** PAM50, consisting of 50 breast cancer-related genes

### Analysis Pipeline

1. Load the TCGA-BRCA expression matrix indexed by Ensembl gene ID
2. Map Ensembl gene IDs to gene symbols using the Gencode probeMap
3. Filter the expression matrix to the 50 PAM50 genes
4. Classify samples as **Primary Tumor** or **Solid Tissue Normal**
5. Calculate mean expression for each group
6. Calculate the difference in mean expression as the effect size
7. Perform Welch's two-sample t-test for each gene
8. Export gene-level summary statistics
9. Export sample-level long-format data for visualization
10. Visualize the results through an interactive Tableau dashboard

The workflow is implemented in Python using **pandas** and **scipy** and is version-controlled so the analysis can be reproduced or adapted to another gene panel or dataset.

## 📈 Results

The analysis successfully identified all **50 of 50 PAM50 genes** in the expression dataset.

The five genes with the largest tumor-vs-normal expression differences were:

| Gene      | Mean Tumor | Mean Normal | Difference |       P-value |
| --------- | ---------: | ----------: | ---------: | ------------: |
| **MMP11** |      5.768 |       1.034 |  **4.735** | 6.71 × 10⁻²¹² |
| **UBE2C** |      4.557 |       1.329 |  **3.227** |  1.53 × 10⁻⁸⁸ |
| **MYBL2** |      3.872 |       1.192 |  **2.680** |  3.22 × 10⁻⁸⁰ |
| **CDC20** |      3.976 |       1.389 |  **2.587** |  7.05 × 10⁻⁷⁹ |
| **BIRC5** |      3.413 |       0.922 |  **2.491** |  1.65 × 10⁻⁷⁴ |

Importantly, the analysis also retains genes such as **PTEN** and **PIK3CA** that did not show similarly strong differences in this cohort.

## 📊 Dashboard

The Tableau dashboard provides three complementary views:

**Effect Size Ranking**
Ranks the PAM50 genes by the difference in mean expression between tumor and normal samples.

**Volcano Plot**
Combines expression difference with statistical significance to distinguish genes with both large effects and strong statistical evidence.

**Gene-Level Distributions**
Allows individual genes to be examined through their sample-level expression distributions.

**[Open the Interactive Tableau Dashboard →](https://public.tableau.com/app/profile/ameypsawant/viz/PAM50GenePanelDifferentialExpressioninTCGABreastCancer/Dashboard)**

## ⚠️ Limitations

* Sample sizes are imbalanced, with substantially more tumor samples than normal samples. This increases statistical power and makes effect size particularly important when interpreting significance.
* This is a descriptive/exploratory analysis using per-gene Welch's t-tests rather than a dedicated differential-expression framework such as DESeq2 or edgeR.
* No multiple-testing correction was applied.
* Samples were not paired between tumor and normal tissue.
* Clinical covariates and potential confounders were not adjusted for.
* FPKM values were used as provided by the GDC bioinformatics pipeline. No additional normalization was performed.

## 👤 Author

**Amey Sawant**

## 📚 References

Parker, J.S., Mullins, M., Cheang, M.C., et al. (2009). Supervised risk predictor of breast cancer based on intrinsic subtypes. *Journal of Clinical Oncology*, 27(8), 1160-1167.

The Cancer Genome Atlas Research Network. (2012). Comprehensive molecular portraits of human breast tumours. *Nature*, 490, 61–70.

Goldman, M.J., Craft, B., Hastie, M., et al. (2020). Visualizing and interpreting cancer genomics data via the Xena platform. *Nature Biotechnology*, 38, 675–678.
