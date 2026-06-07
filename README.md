# Grow--Mutual-Fund-FAQ-Assistant-

An intelligent FAQ assistant powered by LLMs to answer questions about mutual funds and investment guidance.

## Overview

This project leverages advanced language models and semantic search to provide accurate, context-aware answers to frequently asked questions about mutual funds. The assistant uses RAG (Retrieval-Augmented Generation) to ensure responses are grounded in reliable financial information.

## Features

- **Intelligent Question Answering**: Uses LangChain and Groq LLM for accurate responses
- **Semantic Search**: Powered by ChromaDB and sentence-transformers for relevant document retrieval
- **Web Scraping**: BeautifulSoup4 for collecting mutual fund information
- **User-Friendly Interface**: Streamlit web application
- **Scheduled Updates**: Automatic information refresh using schedule module

## Installation

```bash
# Clone the repository
git clone https://github.com/Sowjanyakaki/Grow--Mutual-Fund-FAQ-Assistant-.git
cd Grow--Mutual-Fund-FAQ-Assistant-

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
echo "GROQ_API_KEY=your_key_here" > .env
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - langchain==0.1.16
  - langchain-community==0.0.34
  - beautifulsoup4==4.12.3
  - chromadb==0.4.24
  - sentence-transformers==2.7.0
  - huggingface-hub==0.23.0
  - langchain-experimental==0.0.57
  - langchain-groq==0.1.3
  - python-dotenv==1.0.1
  - streamlit==1.35.0
  - schedule==1.2.1

## Usage

```bash
# Run the Streamlit application
streamlit run app.py
```

## Sample Q&A

### Q: What is a mutual fund?
**A:** A mutual fund is an investment fund managed by professionals that pools money from multiple investors to purchase securities like stocks and bonds.

### Q: What are the different types of mutual funds?
**A:** Common types include equity funds (stocks), bond funds (fixed income), money market funds, balanced funds, and index funds.

### Q: What is the difference between active and passive mutual funds?
**A:** Active funds are managed by professionals who try to outperform the market, while passive funds track market indices with lower fees.

### Q: How often can I withdraw from my mutual fund?
**A:** Most mutual funds allow daily redemptions during market hours, though some have specific redemption schedules or lock-in periods.

### Q: What are the fees associated with mutual funds?
**A:** Common fees include expense ratios, load fees (entry or exit charges), and redemption fees. Always check the fund's prospectus for details.

## Sources

This project utilizes information from the following sources:

- [Investopedia - Mutual Funds](https://www.investopedia.com/terms/m/mutualfund.asp)
- [AMFI India](https://www.amfiindia.com/)
- [SEBI - Securities and Exchange Board of India](https://www.sebi.gov.in/)
- [NSE - National Stock Exchange](https://www.nseindia.com/)
- [BSE - Bombay Stock Exchange](https://www.bseindia.com/)
- Official mutual fund house websites and prospectuses
- Financial news portals and publications

## Disclaimer

**IMPORTANT LEGAL NOTICE:**

This Mutual Fund FAQ Assistant is provided for educational and informational purposes only. It is NOT financial advice and should not be construed as such.

- **No Professional Advice**: The information provided by this assistant does not constitute professional financial advice, investment recommendations, or legal counsel. Users should not rely solely on this tool for making investment decisions.

- **No Liability**: The creators and maintainers of this tool are not responsible for any financial losses, damages, or consequences arising from the use of information provided by this assistant.

- **Consult Professionals**: Before making any investment decisions, please consult with qualified financial advisors, investment professionals, or legal experts who can assess your individual financial situation and risk tolerance.

- **Market Risk**: Mutual fund investments carry market risk and are subject to various factors including economic conditions, market fluctuations, and regulatory changes.

- **Past Performance**: Historical performance of mutual funds does not guarantee future results. All investments carry the potential for loss.

- **Accuracy**: While we strive to provide accurate information, we do not warrant the completeness, accuracy, or timeliness of the information contained herein. Market conditions and fund details change frequently.

- **User Responsibility**: Users are solely responsible for their investment decisions and should verify all information independently before acting upon it.

By using this Mutual Fund FAQ Assistant, you acknowledge that you have read and agree to this disclaimer.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open-source and available under the MIT License.

---

**Last Updated**: June 2026
