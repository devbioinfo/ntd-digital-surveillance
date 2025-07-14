# NTD Digital Surveillance Pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15883324.svg)](https://doi.org/10.5281/zenodo.15883324)

A reproducible **Snakemake + Docker** pipeline for analyzing social media (YouTube) and news (Google News) discussions on dengue, chikungunya, lymphatic filariasis, and kala-azar in India using sentiment analysis, topic modeling, and epidemiological comparisons.

---

## 🚀 Quick Start

### 1. Clone the repository
\`\`\`bash
git clone git@github.com:devbioinfo/ntd-digital-surveillance.git
cd ntd-digital-surveillance
\`\`\`

### 2. Run the pipeline

#### a) Using Snakemake + Conda:
\`\`\`bash
snakemake --use-conda --cores 4
\`\`\`

#### b) Using Docker:
\`\`\`bash
docker build -t ntd-pipeline .
docker run --rm -v "\$(pwd)":/data ntd-pipeline snakemake --use-conda --cores 4
\`\`\`

Once complete, pipeline outputs—cleaned data, analysis results, and visualizations—will appear in the \`data/\` directory.

---

## 🔍 Pipeline Structure

\`\`\`
ntd-digital-surveillance/
├── Snakefile             # Workflow definition
├── workflow/scripts/     # Python & R scripts for each step
├── data/                 # Input data (raw/processed) and outputs
├── Dockerfile            # Environment setup
├── CITATION.cff          # Citation metadata
└── README.md             # This documentation
\`\`\`

**Key analysis scripts:**
- \`google_news_scraper.py\` – Fetches Google News headlines  
- \`clean_google_news.py\`, \`clean_youtube_comments.py\` – Data cleaning  
- \`plot_sentiment_by_topic.py\`, \`wordcloud_pos_neg.py\`, \`yt_cooccurrence.py\` – Sentiment/topic analysis and visualization  
- \`run_all_pipeline.py\` – Runs the full pipeline with a single command

Each script includes comments with usage instructions.

---

## 📄 Citation

Please cite this tool as:

\`\`\`
Biswal D.K., Konhar R., Lalsanga J.K. (2025). *NTD Digital Surveillance Pipeline*. Zenodo. https://doi.org/10.5281/zenodo.15883324
\`\`\`

Use the badge above for easy citation in documentation or publications.

---

## 📜 License

This project is licensed under the **MIT License**. See \`LICENSE\` for details.

---

## 🤝 Contributing

Contributions are welcome! Please fork, make changes, and open a pull request. Include tests or example outputs where relevant, and reference this DOI in your updates.

---

## 📬 Contact

For assistance or queries, open an issue on GitHub or contact **Devendra K. Biswal** at devbioinfo@gmail.com
