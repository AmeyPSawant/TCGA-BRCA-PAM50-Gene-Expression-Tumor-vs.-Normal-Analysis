import pandas as pd
from scipy import stats

# Load PAM50 gene list
with open("pam50_genes.txt") as f:
    pam50_genes = f.read().split()

# Load bulk expression matrix (genes x samples)
expr = pd.read_csv("expression_matrix.tsv", sep="\t", index_col=0)

# Load ID-to-gene-symbol mapping
probemap = pd.read_csv("probemap_file.tsv", sep="\t")  # use your actual filename

# Build mapping dictionary: Ensembl ID -> gene symbol
id_to_gene = dict(zip(probemap["id"], probemap["gene"]))

# Remap expr's index from Ensembl ID to gene symbol
expr.index = expr.index.map(id_to_gene)

# Drop rows that didn't find a match (returns NaN)
expr = expr[expr.index.notna()]

print(f"Expression matrix now has {expr.shape[0]} genes with symbols mapped")

# Check for duplicate gene symbols
dupes = expr.index[expr.index.duplicated()].unique()
if len(dupes) > 0:
    print(f"Warning: {len(dupes)} duplicate gene symbols found, keeping first occurrence")
    expr = expr[~expr.index.duplicated(keep="first")]

# Load phenotype data (has sample_type per sample)
pheno = pd.read_csv("phenotype_matrix.tsv", sep="\t")
pheno = pheno.set_index(pheno.columns[0])  # adjust if sample ID column isn't first

# Filter to genes present in PAM50 list
available_genes = [g for g in pam50_genes if g in expr.index]
print(f"Found {len(available_genes)} of 50 PAM50 genes in the dataset")

tumor_samples = pheno[pheno["sample_type.samples"] == "Primary Tumor"].index
normal_samples = pheno[pheno["sample_type.samples"] == "Solid Tissue Normal"].index

tumor_samples = [s for s in tumor_samples if s in expr.columns]
normal_samples = [s for s in normal_samples if s in expr.columns]

results = []
long_rows = []

for gene in available_genes:
    tumor_vals = expr.loc[gene, tumor_samples].dropna()
    normal_vals = expr.loc[gene, normal_samples].dropna()

    if len(tumor_vals) < 2 or len(normal_vals) < 2:
        continue

    t_stat, p_val = stats.ttest_ind(tumor_vals, normal_vals, equal_var=False)

    results.append({
        "gene": gene,
        "mean_tumor": tumor_vals.mean(),
        "mean_normal": normal_vals.mean(),
        "difference": tumor_vals.mean() - normal_vals.mean(),
        "n_tumor": len(tumor_vals),
        "n_normal": len(normal_vals),
        "p_value": p_val
    })

    for sid, val in tumor_vals.items():
        long_rows.append({"sample": sid, "sample_type": "Primary Tumor", "gene": gene, "expression_value": val})
    for sid, val in normal_vals.items():
        long_rows.append({"sample": sid, "sample_type": "Solid Tissue Normal", "gene": gene, "expression_value": val})

summary_df = pd.DataFrame(results).sort_values("difference", ascending=False)
long_df = pd.DataFrame(long_rows)

summary_df.to_excel("gene_summary_stats.xlsx", index=False, sheet_name="Summary")
long_df.to_excel("gene_expression_long.xlsx", index=False, sheet_name="Long")

print("Done. Top 5 genes by effect size:")
print(summary_df.head())